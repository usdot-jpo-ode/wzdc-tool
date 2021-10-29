def buildCommonContainer(eventId, startDateTime, endDateTime, timeOffset, wzDaysOfWeek, causeCodes, refPoint, heading,
                         laneWidth, rW, numlanes, geometry, descName, linkedEventIdList):

    ###
    #       Following data are passed from the caller for constructing Common Container...
    ###
    #       eventId     = message ID
    #       eDateTime   = event start date & time [yyyy,mm,dd,hh,mm,ss]
    #       durDateTime = event duration date & time [yyyy,mm,dd,hh,mm,ss]
    #       timeOffset  = offset in minutes from UTC -300 minutes
    #       causeCodes  = cause and subcause codes [c,sc]
    #       refPoint    = reference point [lat,lon,alt]
    #       rW          = roadWidth (m)
    #       appMapPt    = array containing approach map points constructed earlier before calling this function
    #
    ###
    laneWidth = round(laneWidth * 10)  # define laneWidth in dm (10 cm)

    commonContainer = {}

    commonContainer['eventInfo'] = {}
    commonContainer['eventInfo']['eventID'] = eventId

    commonContainer['eventInfo']['eventCancellation'] = False

    ###
    #   WZ start date and time are required. If not specified, use current date and 00h:00m
    #   WZ end date and time are optional, if not present, skip it
    ###

    commonContainer['eventInfo']['startDateTime'] = {}
    commonContainer['eventInfo']['startDateTime']['year'] = startDateTime[2]
    commonContainer['eventInfo']['startDateTime']['month'] = startDateTime[0]
    commonContainer['eventInfo']['startDateTime']['day'] = startDateTime[1]
    commonContainer['eventInfo']['startDateTime']['hour'] = startDateTime[3]
    commonContainer['eventInfo']['startDateTime']['minute'] = startDateTime[4]
    commonContainer['eventInfo']['startDateTime']['offset'] = timeOffset

    ###
    #       Event duration - End date & time can be optional...
    ###

    if str(endDateTime[0]) != "":
        commonContainer['eventInfo']['endDateTime'] = {}
        commonContainer['eventInfo']['endDateTime']['year'] = endDateTime[2]
        commonContainer['eventInfo']['endDateTime']['month'] = endDateTime[0]
        commonContainer['eventInfo']['endDateTime']['day'] = endDateTime[1]
        commonContainer['eventInfo']['endDateTime']['hour'] = endDateTime[3]
        commonContainer['eventInfo']['endDateTime']['minute'] = endDateTime[4]

    ###
    #       Event Recurrence...
    ###

    commonContainer['eventInfo']['eventRecurrence'] = {}
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence'] = {}
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence']['startTime'] = {}
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence']['startTime']['hour'] = startDateTime[3]
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence']['startTime']['minute'] = startDateTime[4]
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence']['startTime']['second'] = 0
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence']['endTime'] = {}
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence']['endTime']['hour'] = endDateTime[3]
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence']['endTime']['minute'] = endDateTime[4]
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence']['endTime']['second'] = 0
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence']['startDate'] = {}
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence']['startDate']['year'] = startDateTime[2]
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence']['startDate']['month'] = startDateTime[0]
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence']['startDate']['day'] = startDateTime[1]
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence']['endDate'] = {}
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence']['endDate']['year'] = endDateTime[2]
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence']['endDate']['month'] = endDateTime[0]
    commonContainer['eventInfo']['eventRecurrence']['EventRecurrence']['endDate']['day'] = endDateTime[1]
    days_of_week = ['monday', 'tuesday', 'wednesday',
                    'thursday', 'friday', 'saturday', 'sunday']
    days_of_week_convert = {'monday': 'Mon', 'tuesday': 'Tue', 'wednesday': 'Wen',
                            'thursday': 'Thu', 'friday': 'Fri', 'saturday': 'Sat', 'sunday': 'Sun'}
    for day in days_of_week:
        commonContainer['eventInfo']['eventRecurrence']['EventRecurrence'][day] = {
            str(days_of_week_convert[day] in wzDaysOfWeek).lower(): None}

    ###
    #       Cause and optional subcause codes...
    ###
    commonContainer['eventInfo']['causeCode'] = causeCodes[0]
    commonContainer['eventInfo']['subCauseCode'] = causeCodes[1]

    # TODO: commonContainer['eventInfo']['affectedVehicles'] (optional)

    commonContainer['regionInfo'] = {}

    commonContainer['regionInfo']['applicableHeading'] = {}
    commonContainer['regionInfo']['applicableHeading']['heading'] = round(
        float(heading['heading']))
    commonContainer['regionInfo']['applicableHeading']['tolerance'] = heading['tolerance']

    lat = int(float(refPoint[0]) * 10000000)
    lon = int(float(refPoint[1]) * 10000000)
    elev = round(float(refPoint[2]))  # in meters no fraction

    commonContainer['regionInfo']['referencePoint'] = {}
    commonContainer['regionInfo']['referencePoint']['lat'] = lat
    commonContainer['regionInfo']['referencePoint']['long'] = lon
    commonContainer['regionInfo']['referencePoint']['elevation'] = elev

    # TODO: commonContainer['regionInfo']['locationUncertainty'] (optional)

    commonContainer['regionInfo']['referencePointType'] = {
        "startOfEvent": None}
    commonContainer['regionInfo']['descriptiveName'] = descName

    alScale = 1  # default approach lane scale factor

    commonContainer['regionInfo']['approachRegion'] = {}
    commonContainer['regionInfo']['approachRegion']['paths'] = {}

    commonContainer['regionInfo']['approachRegion']['paths']['path'] = []

    for lane in geometry:
        Path = {}
        Path['pathWidth'] = laneWidth
        Path['pathPoints'] = {}
        Path['pathPoints']['pathPoint'] = []

        for node in lane:
            lat = int(node[0] * 10000000)
            lon = int(node[1] * 10000000)
            elev = round(node[2])  # in full meters

            NodePoint = {}
            NodePoint['nodePoint'] = {}
            NodePoint['nodePoint']['node-3Dabsolute'] = {}
            NodePoint['nodePoint']['node-3Dabsolute']['lat'] = lat
            NodePoint['nodePoint']['node-3Dabsolute']['long'] = lon
            NodePoint['nodePoint']['node-3Dabsolute']['elevation'] = elev

            Path['pathPoints']['pathPoint'].append(NodePoint)

        commonContainer['regionInfo']['approachRegion']['paths']['path'].append(
            Path)

    if linkedEventIdList:
        commonContainer['crossLinking'] = {}
        commonContainer['crossLinking']['rsmLinks'] = {}
        commonContainer['crossLinking']['rsmLinks']['rsmLink'] = linkedEventIdList

    return commonContainer


def buildLaneClosureContainer(laneStat, laneStatusVaries, geometry, laneWidth):
    laneClosureContainer = {}

    laneClosureContainer['laneStatus'] = {}
    laneClosureContainer['laneStatus']['laneStatus'] = []
    for index, status in enumerate(laneStat):
        laneStatus = {}
        laneStatus['lanePosition'] = index + 1
        laneStatus['laneClosed'] = {str(status).lower(): None}
        # laneStatus['laneCloseOffset'] = obstacleDistance # NOT IMPLEMENTED
        laneClosureContainer['laneStatus']['laneStatus'].append(laneStatus)

    if laneStatusVaries is not None:
        laneClosureContainer['laneStatusVaries'] = {
            str(laneStatusVaries).lower(): None}

    laneClosureContainer['closureRegion'] = {}
    laneClosureContainer['closureRegion']['paths'] = {}
    laneClosureContainer['closureRegion']['paths']['path'] = []

    laneWidth = round(laneWidth * 100)  # in cms

    for lane in geometry:
        Path = {}
        Path['pathWidth'] = laneWidth
        Path['pathPoints'] = {}
        Path['pathPoints']['pathPoint'] = []

        for node in lane:
            lat = int(node[0] * 10000000)
            lon = int(node[1] * 10000000)
            elev = round(node[2])  # in full meters

            NodePoint = {}
            NodePoint['nodePoint'] = {}
            NodePoint['nodePoint']['node-3Dabsolute'] = {}
            NodePoint['nodePoint']['node-3Dabsolute']['lat'] = lat
            NodePoint['nodePoint']['node-3Dabsolute']['long'] = lon
            NodePoint['nodePoint']['node-3Dabsolute']['elevation'] = elev

            Path['pathPoints']['pathPoint'].append(NodePoint)

        laneClosureContainer['closureRegion']['paths']['path'].append(Path)

    return laneClosureContainer


def buildRszContainer(speedLimit, geometry, laneWidth):
    rszContainer = {}

    rszContainer['speedLimit'] = {}
    rszContainer['speedLimit']['type'] = {speedLimit['type']: None}
    rszContainer['speedLimit']['speed'] = speedLimit['value']

    rszContainer['rszRegion'] = {}
    rszContainer['rszRegion']['paths'] = {}
    rszContainer['rszRegion']['paths']['path'] = []

    laneWidth = round(laneWidth * 100)  # in cms

    for lane in geometry:
        Path = {}
        Path['pathWidth'] = laneWidth
        Path['pathPoints'] = {}
        Path['pathPoints']['pathPoint'] = []

        for node in lane:
            lat = int(node[0] * 10000000)
            lon = int(node[1] * 10000000)
            elev = round(node[2])  # in full meters

            NodePoint = {}
            NodePoint['nodePoint'] = {}
            NodePoint['nodePoint']['node-3Dabsolute'] = {}
            NodePoint['nodePoint']['node-3Dabsolute']['lat'] = lat
            NodePoint['nodePoint']['node-3Dabsolute']['long'] = lon
            NodePoint['nodePoint']['node-3Dabsolute']['elevation'] = elev

            Path['pathPoints']['pathPoint'].append(NodePoint)

        rszContainer['rszRegion']['paths']['path'].append(Path)
    # End iterating over lanes

    return rszContainer


def buildSituationalContainer(obstructions, visibility, peoplePresent, anomalousTraffic):
    situationalContainer = {}

    if obstructions is not None:
        situationalContainer['obstructions'] = obstructions

    if visibility is not None:
        situationalContainer['visibility'] = visibility

    if peoplePresent is not None:
        situationalContainer['peoplePresent'] = {
            str(peoplePresent).lower(): None}

    if anomalousTraffic is not None:
        situationalContainer['anomalousTraffic'] = {
            str(anomalousTraffic).lower(): None}

    return situationalContainer
