

import xml.etree.ElementTree as ET
from jsonschema import validate
import json
from datetime import datetime
import uuid
import random
import string
import logging
import copy

from .validation_schema import wzdx_v3_1_feed


# NOTE: Info object for reference
# info = {}
# info['feed_info_id'] = feed_info_id
# info['license'] = "https://creativecommons.org/publicdomain/zero/1.0/"
# info['road_name'] = roadName
# info['description'] = wzDesc
# info['direction'] = direction
# info['beginning_cross_street'] = beginningCrossStreet
# info['ending_cross_street'] = endingCrossStreet
# info['beginning_milepost'] = beginningMilepost
# info['ending_milepost'] = endingMilepost
# info['issuing_organization'] = issuingOrganization
# info['creation_date'] = creationDate
# info['update_date'] = updateDate
# info['event_status'] = eventStatus
# info['beginning_accuracy'] = beginingAccuracy
# info['ending_accuracy'] = endingAccuracy
# info['start_date_accuracy'] = startDateAccuracy
# info['end_date_accuracy'] = endDateAccuracy

# info['metadata'] = {}
# info['metadata']['wz_location_method'] = wzLocationMethod
# info['metadata']['lrs_type'] = lrsType
# info['metadata']['location_verify_method'] = locationVerifyMethod
# if dataFeedFrequencyUpdate:
#   info['metadata']['datafeed_frequency_update'] = dataFeedFrequencyUpdate
# info['metadata']['timestamp_metadata_update'] = timestampMetadataUpdate
# info['metadata']['contact_name'] = contactName
# info['metadata']['contact_email'] = contactEmail
# info['metadata']['issuing_organization'] = issuingOrganization

# info['types_of_work'] = typeOfWork
# info['lanes_obj'] = lanes_obj


# Translator
def wzdx_creator(messages, dataLane, info):
    wzd = {}
    wzd['road_event_feed_info'] = {}
    wzd['road_event_feed_info']['feed_info_id'] = info['feed_info_id']
    wzd['road_event_feed_info']['update_date'] = datetime.now().strftime(
        "%Y-%m-%dT%H:%M:%SZ")
    wzd['road_event_feed_info']['publisher'] = 'POC Work Zone Integrated Mapping'
    wzd['road_event_feed_info']['contact_name'] = 'Tony English'
    wzd['road_event_feed_info']['contact_email'] = 'tony@neaeraconsulting.com'
    if info['metadata'].get('datafeed_frequency_update', False):
        # Verify data type
        wzd['road_event_feed_info']['update_frequency'] = info['metadata']['datafeed_frequency_update']
    wzd['road_event_feed_info']['version'] = '3.1'
    wzd['road_event_feed_info']['license'] = info['license']

    data_source = {}
    data_source['data_source_id'] = str(uuid.uuid4())
    data_source['feed_info_id'] = info['feed_info_id']
    data_source['organization_name'] = info['metadata']['issuing_organization']
    data_source['contact_name'] = info['metadata']['contact_name']
    data_source['contact_email'] = info['metadata']['contact_email']
    if info['metadata'].get('datafeed_frequency_update', False):
        data_source['update_frequency'] = info['metadata']['datafeed_frequency_update']
    data_source['update_date'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    data_source['location_verify_method'] = info['metadata']['location_verify_method']
    data_source['location_method'] = info['metadata']['wz_location_method']
    data_source['lrs_type'] = info['metadata']['lrs_type']
    # data_source['lrs_url'] = "basic url"

    wzd['road_event_feed_info']['data_sources'] = [data_source]

    wzd['type'] = 'FeatureCollection'
    wzdxMessages = []

    for rsmMessage in messages:
        rsm = rsmMessage['RoadsideSafetyMessage']

        numLanes = len(rsm['commonContainer']['regionInfo'].get(
            'approachRegion', {}).get('paths', {}).get('path', []))

        initialLaneStatus = []
        restrictions = []
        for i in range(numLanes):
            lane_num = i + 1
            lane = {
                'order': lane_num,
                'type': get_lane_type(lane_num, numLanes),
                'status': 'open',
                'lane_number': lane_num,
                'restrictions': [],
            }
            # Overwrite lane_type and restrictions if in info
            lane, restrictions = get_lane_restrictions(
                info, lane, restrictions)
            initialLaneStatus.append(lane)

        # nodes, indices = getNodesAndIndices(containers, numLanes, dataLane, initialLaneStatus)

        # Create one WZDx message for one RSM message. Ignore gometry from all containers except reduced speed zone
        wzdxMessages.append(createIndividualWzdxMessage(numLanes, dataLane, initialLaneStatus, restrictions, info,
                                                        rsm['commonContainer'],
                                                        rszContainer=rsm.get(
                                                            'rszContainer'),
                                                        laneClosureContainer=rsm.get(
                                                            'laneClosureContainer'),
                                                        situationalContainer=rsm.get('situationalContainer')))

    wzd['features'] = wzdxMessages
    wzd = add_ids(wzd, True)
    # This will throw an exception if the message is invalid
    validate(schema=wzdx_v3_1_feed.WZDX_VALIDATION_SCHEMA, instance=wzd)
    return wzd


# Add ids to message
def add_ids(message, add_ids):
    if add_ids:
        feed_info_id = message['road_event_feed_info']['feed_info_id']
        data_source_id = message['road_event_feed_info']['data_sources'][0]['data_source_id']

        road_event_length = len(message['features'])
        road_event_ids = []
        for i in range(road_event_length):
            road_event_ids.append(str(uuid.uuid4()))

        for i in range(road_event_length):
            feature = message['features'][i]
            road_event_id = road_event_ids[i]
            feature['properties']['id'] = road_event_id
            # feature['properties']['feed_info_id'] = feed_info_id
            feature['properties']['data_source_id'] = data_source_id
            # feature['properties']['relationship'] = {}
            feature['properties']['relationship']['relationship_id'] = str(
                uuid.uuid4())
            feature['properties']['relationship']['road_event_id'] = road_event_id
            if i == 0:
                feature['properties']['relationship']['first'] = road_event_ids
            else:
                feature['properties']['relationship']['next'] = road_event_ids
    return message


# 0 pad times to 2 digits (2 -> 02)
def form_len(string):
    num = int(string)
    return format(num, '02d')


def convertLatLong(num):
    return float(num)/10000000


def reformatNodePoint(node):
    return [convertLatLong(node['long']), convertLatLong(node['lat']), node['elevation']]


def reformatGeometry(pathPoints):
    nodes = []
    for nodePoint in pathPoints:
        node = nodePoint['nodePoint']['node-3Dabsolute']
        nodes.append(reformatNodePoint(node))

    return nodes


def transformLaneStatus(numLanes, initialLaneStatus, laneStatus):
    currLaneStatus = copy.deepcopy(initialLaneStatus)
    for index, status in enumerate(laneStatus):
        if status['laneClosed'] == {'true': None}:
            currLaneStatus[index]['status'] = 'closed'

    return currLaneStatus


def getNodesAndIndices(containers, numLanes, dataLane, initialLaneStatus):
    datalaneIndex = dataLane - 1

    nodes = []

    indices = {
        'speedLimits': [],
        'workersPresent': [],
        'laneClosures': []
    }

    rszContainers = containers['rszContainers']['rszContainer']
    for rsz in rszContainers:
        speedLimit = rsz['speedLimit']['speed']

        currIndex = len(nodes)
        indices['speedLimits'].append(
            {'speedLimit': speedLimit, 'startIndex': currIndex})

        path = rsz['rszRegion']['paths']['path'][datalaneIndex]
        geometry = reformatGeometry(path['pathPoints']['pathPoint'])

        for i in geometry:
            nodes.append(i)

    laneClosureContainers = containers['laneClosureContainers']['laneClosureContainer']
    for lc in laneClosureContainers:
        laneStatus = transformLaneStatus(
            numLanes, initialLaneStatus, lc['laneStatus']['laneStatus'])

        firstLane = lc['closureRegion']['paths']['path'][datalaneIndex]['pathPoints']['pathPoint']

        firstNode = reformatNodePoint(
            firstLane[0]['nodePoint']['node-3Dabsolute'])
        lastNode = reformatNodePoint(
            firstLane[-1]['nodePoint']['node-3Dabsolute'])

        firstIndex = nodes.index(firstNode)
        lastIndex = nodes.index(lastNode)
        indices['laneClosures'].append(
            {'laneStatus': laneStatus, 'startIndex': firstIndex, 'endIndex': lastIndex})

    # situationalContainers = containers['situationalContainers']['situationalContainer']
    # for sit in situationalContainers:

    return nodes, indices


def convertGeometry(nodes, dataLane=None):
    print(nodes)
    try:
        dataIndex = dataLane - 1
        if dataLane:
            lanes = nodes['paths']['path']
            data = lanes[dataIndex]
        else:
            data = nodes
        geometry = []
        for node in data['pathPoints']['pathPoint']:
            lat = convertLatLong(node['nodePoint']['node-3Dabsolute']['lat'])
            lon = convertLatLong(node['nodePoint']['node-3Dabsolute']['long'])
            elev = node['nodePoint']['node-3Dabsolute'].get('elevation')
            if elev:
                geometry.append([lon, lat, elev])
            else:
                geometry.append([lon, lat])
        return geometry

    except Exception as e:
        print(e)
        return []


def createIndividualWzdxMessage(numLanes, dataLane, initialLaneStatus, restrictions, info, commonContainer, rszContainer=None, laneClosureContainer=None, situationalContainer=None):
    speedLimit = None if not rszContainer else rszContainer.get(
        'speedLimit', {}).get('speed')
    laneStatus = initialLaneStatus if not laneClosureContainer else transformLaneStatus(
        numLanes, initialLaneStatus, laneClosureContainer['laneStatus']['laneStatus'])
    workersPresent = None
    if situationalContainer and situationalContainer.get('peoplePresent'):
        workersPresent = situationalContainer.get(
            'peoplePresent') == {'true': None}
    restrictions = []

    nodes = []
    if rszContainer:
        nodes = rszContainer.get('rszRegion', [])
    elif laneClosureContainer:
        nodes = laneClosureContainer.get('closureRegion', [])
    geometry = convertGeometry(nodes, dataLane)

    return createFeature(geometry, numLanes, laneStatus, speedLimit, restrictions, commonContainer, workersPresent, info)


def createConnectedWzdxMessages(nodes, indices, numLanes, initialLaneStatus, restrictions, commonContainer, workersPresent, info):
    prevSpeedlimit = 0
    prevLaneStatus = initialLaneStatus
    restrictions = []

    features = []

    for index, node in enumerate(nodes):
        currSpeedLimit = prevSpeedlimit
        for speedLimit in indices['speedLimits']:
            if speedLimit['startIndex'] == index:
                currSpeedLimit = speedLimit['speedLimit']

        currLaneStatus = prevLaneStatus
        for laneStatus in indices['laneClosures']:
            if index >= laneStatus['startIndex'] and index <= laneStatus['endIndex']:
                currLaneStatus = laneStatus['laneStatus']
            else:
                currLaneStatus = initialLaneStatus

        if currSpeedLimit != prevSpeedlimit or currLaneStatus != prevLaneStatus or index == 0:

            if (index != 0):
                features[-1]['geometry']['coordinates'].append(node)

            features.append(createFeature(node, numLanes, currLaneStatus,
                            currSpeedLimit, restrictions, commonContainer, workersPresent, info))

            prevSpeedlimit = currSpeedLimit
            prevLaneStatus = currLaneStatus

        else:
            features[-1]['geometry']['coordinates'].append(node)
    return features


def createFeature(geometry, numLanes, lanes, speedLimit, restrictions, commonContainer, workersPresent, info):
    if not geometry:
        return None
    properties = setFeatureProperties(commonContainer, info)

    num_closed_lanes = 0
    for lane in lanes:
        if lane['status'] == 'closed' or lane['status'] == 'merge-left' or lane['status'] == 'merge-right':
            num_closed_lanes = num_closed_lanes + 1
    if num_closed_lanes == 0:
        properties['vehicle_impact'] = 'all-lanes-open'
    elif num_closed_lanes == numLanes:
        properties['vehicle_impact'] = 'all-lanes-closed'
    else:
        properties['vehicle_impact'] = 'some-lanes-closed'

    # workser_present
    if workersPresent:
        properties['workers_present'] = workersPresent

    # reduced_speed_limit
    if speedLimit:
        properties['reduced_speed_limit'] = speedLimit

    # description
    properties['description'] = info['description']

    # restrictions
    if restrictions:
        properties['restrictions'] = restrictions

    # Lanes object
    if lanes:
        properties['lanes'] = lanes

    # properties
    feature = {}
    feature['type'] = 'Feature'
    feature['properties'] = properties
    if type(geometry) == list:
        feature['geometry'] = {'type': 'LineString', 'coordinates': geometry}
    else:
        feature['geometry'] = {'type': 'LineString', 'coordinates': [geometry]}

    return feature


def get_lane_restrictions(info, lane, restrictions):
    # no-trucks, travel-peak-hours-only, hov-3, hov-2, no-parking
    lane['restrictions'] = []
    #reduced-width, reduced-height, reduced-length, reduced-weight, axle-load-limit, gross-weight-limit, towing-prohibited, permitted-oversize-loads-prohibited

    # Overwrite lane_type if present in configuration file
    for lane_obj in info['lanes_obj']:
        if lane_obj['LaneNumber'] == lane['lane_number']:
            lane['type'] = lane_obj['LaneType']
            for lane_restriction_info in lane_obj['LaneRestrictions']:
                lane_restriction = {}
                lane_restriction['lane_restriction_id'] = ''
                lane_restriction['lane_id'] = ''
                lane_restriction['restriction_type'] = lane_restriction_info['RestrictionType']
                if not lane_restriction_info['RestrictionType'] in restrictions:
                    restrictions.append(
                        lane_restriction_info['RestrictionType'])
                if lane_restriction['restriction_type'] in ['reduced-width', 'reduced-height', 'reduced-length', 'reduced-weight', 'axle-load-limit', 'gross-weight-limit']:
                    lane_restriction['restriction_value'] = lane_restriction_info['RestrictionValue']
                    lane_restriction['restriction_units'] = lane_restriction_info['RestrictionUnits']
                lane['restrictions'].append(lane_restriction)

    return lane, restrictions


def get_lane_type(lane_number, num_lanes):
    # Lane Type
    # left-lane, right-lane, middle-lane, right-exit-lane, left-exit-lane, ... (exit lanes, merging lanes, turning lanes)
    lane_type = 'middle-lane'
    if lane_number == 1:
        lane_type = 'left-lane'
    elif lane_number == num_lanes:
        lane_type = 'right-lane'

    return lane_type


def setFeatureProperties(commonContainer, info):
    feature = {}
    feature['road_event_id'] = ''
    feature['data_source_id'] = ''

    # Event Type ['work-zone', 'detour']
    feature['event_type'] = 'work-zone'

    # Relationship
    feature['relationship'] = {}

    # road_name
    feature['road_names'] = [info['road_name']]

    # direction
    feature['direction'] = info['direction']

    # beginning_cross_street
    if info['beginning_cross_street']:
        feature['beginning_cross_street'] = info['beginning_cross_street']

    # beginning_cross_street
    if info['ending_cross_street']:
        feature['ending_cross_street'] = info['ending_cross_street']

    # beginning_milepost
    if info['beginning_milepost']:
        feature['beginning_milepost'] = info['beginning_milepost']

    # ending_milepost
    if info['ending_milepost']:
        feature['ending_milepost'] = info['ending_milepost']

    # beginning_accuracy
    feature['beginning_accuracy'] = info['beginning_accuracy']

    # ending_accuracy
    feature['ending_accuracy'] = info['ending_accuracy']

    # start_date
    # Offset is in minutes from UTC (-5 hours, ET), unused
    start_date = commonContainer['eventInfo']['startDateTime']
    feature['start_date'] = str(start_date['year']+'-'+form_len(start_date['month'])+'-'+form_len(
        start_date['day'])+'T'+form_len(start_date['hour'])+':'+form_len(start_date['minute'])+':00Z')

    # end_date
    end_date = commonContainer['eventInfo']['endDateTime']
    feature['end_date'] = str(end_date['year']+'-'+form_len(end_date['month'])+'-'+form_len(
        end_date['day'])+'T'+form_len(end_date['hour'])+':'+form_len(end_date['minute'])+':00Z')

    # start_date_accuracy
    feature['start_date_accuracy'] = info['start_date_accuracy']

    # end_date_accuracy
    feature['end_date_accuracy'] = info['end_date_accuracy']

    # event status
    if info['event_status']:
        feature['event_status'] = info['event_status']
        if info['event_status'] == 'planned':
            feature['start_date_accuracy'] = 'estimated'
            feature['end_date_accuracy'] = 'estimated'

    # issuing_organization
    if info['issuing_organization']:
        feature['issuing_organization'] = info['issuing_organization']

    # creation_date
    if info['creation_date']:
        feature['creation_date'] = info['creation_date']

    # update_date
    feature['update_date'] = info['update_date']

    # creation_date
    feature['creation_date'] = info['update_date']

    # type_of_work
    #maintenance, minor-road-defect-repair, roadside-work, overhead-work, below-road-work, barrier-work, surface-work, painting, roadway-relocation, roadway-creation
    feature['types_of_work'] = []
    for types_of_work in info['types_of_work']:
        type_of_work = {}
        type_of_work['types_of_work_id'] = ''
        type_of_work['road_event_id'] = ''
        type_of_work['type_name'] = types_of_work['WorkType']
        if types_of_work.get('Is_Architectural_Change', '') != '':
            type_of_work['is_architectural_change'] = types_of_work['Is_Architectural_Change']
        feature['types_of_work'].append(type_of_work)

    return feature
