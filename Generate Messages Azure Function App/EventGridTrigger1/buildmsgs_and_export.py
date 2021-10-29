#!/usr/bin/env python3
###
#   This software module to:
#   A. Parse the vehicle path data collected through traversing WZ lanes
#       A.1 construct node points for representing lane geometry for both approach and WZ lanes
#           a. WZ map - Read collected vehicle path data file - lat,lon,elev,heading,speed,time, and few other elements
#           a. reference point - start of WZ
#           b. approach lane geometry
#           b. WZ lane geometry
#       A.2 Lane attributes
#           a. Lane closures (both offset from RP and nodeAttributeXYlist of taperToLeft and taperToRight
#           b. Support of opening of the closed lane up to 4 times
#           c.Presence of workers at designated area (zone) support of up to 4 zones
#       A.3 WZ length
#       A.4 eventID, Duration, speed limits. etc.
#
#   B. Construct .exer (XML Format) file for WZ as prescribed in ASN.1 for RSM (SAE J2945/4 WIP) including:
#   C. Construct .js (javaScript) file containing several arrays for visualization overlay on Google Satellite map

#
#   By J. Parikh / Nov, 2017
#   Revised June 2018
#   Revised Aug  2018
#
#   Ver 2.0 -   Proposed new RSM/XML(EXER) for ASN.1 and map visualization
#
###

import os.path
import sys
import subprocess
import urllib
import requests
import base64
import copy
import tempfile
import uuid

###
#     Open and read csv file...
###

import logging
import re
import csv  # csv file processor
import datetime  # Date and Time methods...
import time  # do I need time???
import math  # math library for math functions
import random  # random number generator
import xmltodict  # dict to xml converter
import json  # json manipulation
import zipfile
import requests

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from . import wz_vehpath_lanestat_builder

from . import wz_map_constructor

from . import wz_xml_builder

from . import rsm_2_wzdx_translator

# import wz_vehpath_lanestat_builder

# import wz_map_constructor

# import wz_xml_builder

# import rsm_2_wzdx_translator


###
#   Following to get user input for WZ config file name and display output for user...
# ---------------------------------------------------------------------------------------------------------------------

###
#   User input/output for work zone map builder is created using 'Tkinter' (TK Interface) module. The  Tkinter
#   is the standard Python interface to the Tk GUI toolkit from Scriptics (formerly developed by Sun Labs).
#
#   The public interface is provided through a number of Python modules. The most important interface module is the
#   Tkinter module itself.
#
#   Just import the Tkinter module to use
#
###

connect_str_env_var = 'neaeraiotstorage_storage'
connect_str = os.getenv(connect_str_env_var)

logger = logging.getLogger("logger_name")
logger.disabled = True

blob_service_client = BlobServiceClient.from_connection_string(
    connect_str, logger=logger)

APPROADH_REGION_TIME = 10  # seconds
MPS_PER_MPH = 0.44704
MAX_NUM_NODES = 63
OPERATOR_ID = "acb6a93b-c9e7-4c67-b90e-c88ecbe5a0ac"


logging.getLogger().setLevel(logging.DEBUG)


def configRead(file):
    global wzConfig
    if os.path.exists(file):
        try:
            cfg = open(file)
            wzConfig = json.loads(cfg.read())
            cfg.close()
            getConfigVars()

        except Exception as e:
            logging.info('ERROR: Configuration file read failed: ' +
                         file + '\n' + str(e))
            raise e
    else:
        logging.error('Configuration file NOT FOUND')
        raise RuntimeError('Configuration file does not exist')

###
# ----------------- End of config_read --------------------
###
#
#   Following user specified values are read from the WZ config file specified by user in WZ_Config_UI.pyw...
#
#   WZ Configuration file is parsed here to get the user input values for used by different modules/functions...
#
#   Added: Aug. 2018
#
# -------------------------------------------------------------------------------------------------------

# Read configuration file


def getConfigVars():

    ###
    #   Following are global variables are later used by other functions/methods...
    ###

    # WZDx Feed Info ID
    global feed_info_id

    # General Information
    global wzDesc  # WZ Description
    global roadName
    global direction
    global beginningCrossStreet
    global endingCrossStreet
    global beginningMilepost
    global endingMilepost
    global eventStatus
    global creationDate
    global updateDate

    # Types of Work
    global typeOfWork

    # Lane Information
    global totalLanes  # total number of lanes in wz
    global laneWidth  # average lane width in meters
    global lanePadApp  # approach lane padding in meters
    global lanePadWZ  # WZ lane padding in meters
    global dataLane  # lane used for collecting veh path data
    global lanes_obj

    # Speed Limits
    global speedList  # speed limits

    # Cause Codes
    global c_sc_codes  # cause/subcause code

    # Schedule
    global startDateTime
    global wzStartDate  # wz start date
    global wzStartTime  # wz start time
    global startDateAccuracy
    global endDateTime
    global wzEndDate  # wz end date
    global wzEndTime  # wz end time
    global endDateAccuracy
    global wzDaysOfWeek  # wz active days of week

    # Location
    global wzStartLat  # wz start date
    global wzStartLon  # wz start time
    global beginningAccuracy
    global wzEndLat  # wz end date
    global wzEndLon  # wz end time
    global endingAccuracy

    # WZDx Metadata
    global wzLocationMethod
    global lrsType
    global locationVerifyMethod
    global dataFeedFrequencyUpdate
    global timestampMetadataUpdate
    global contactName
    global contactEmail
    global issuingOrganization

    # Image Info
    global mapImageZoom
    global mapImageCenterLat
    global mapImageCenterLon
    global mapImageMarkers
    global marker_list
    global mapImageMapType
    global mapImageHeight
    global mapImageWidth
    global mapImageFormat
    global mapImageString

    global mapFailed

    try:

        feed_info_id = wzConfig['FeedInfoID']

        wzDesc = wzConfig['GeneralInfo']['Description']
        roadName = wzConfig['GeneralInfo']['RoadName']
        direction = wzConfig['GeneralInfo']['Direction']
        beginningCrossStreet = wzConfig['GeneralInfo']['BeginningCrossStreet']
        endingCrossStreet = wzConfig['GeneralInfo']['EndingCrossStreet']
        beginningMilepost = wzConfig['GeneralInfo']['BeginningMilePost']
        endingMilepost = wzConfig['GeneralInfo']['EndingMilePost']
        eventStatus = wzConfig['GeneralInfo']['EventStatus']
        creationDate = wzConfig['GeneralInfo'].get('CreationDate', '')
        updateDate = wzConfig['GeneralInfo'].get(
            'UpdateDate', datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))

        typeOfWork = wzConfig['TypesOfWork']
        if not typeOfWork:
            typeOfWork = []

        # total number of lanes in wz
        totalLanes = int(wzConfig['LaneInfo']['NumberOfLanes'])
        # average lane width in meters
        laneWidth = float(wzConfig['LaneInfo']['AverageLaneWidth'])
        # approach lane padding in meters
        lanePadApp = float(wzConfig['LaneInfo']['ApproachLanePadding'])
        # WZ lane padding in meters
        lanePadWZ = float(wzConfig['LaneInfo']['WorkzoneLanePadding'])
        # lane used for collecting veh path data
        dataLane = int(wzConfig['LaneInfo']['VehiclePathDataLane'])
        lanes_obj = list(wzConfig['LaneInfo']['Lanes'])

        speedList = wzConfig['SpeedLimits']['NormalSpeed'], wzConfig['SpeedLimits']['ReferencePointSpeed'], \
            wzConfig['SpeedLimits']['WorkersPresentSpeed']

        c_sc_codes = [int(wzConfig['CauseCodes']['CauseCode']),
                      int(wzConfig['CauseCodes']['SubCauseCode'])]

        startDateTime = wzConfig['Schedule']['StartDate']
        wzStartDate = datetime.datetime.strptime(
            startDateTime, "%Y-%m-%dT%H:%M:%SZ").strftime("%m/%d/%Y")
        wzStartTime = datetime.datetime.strptime(
            startDateTime, "%Y-%m-%dT%H:%M:%SZ").strftime("%H:%M")
        startDateAccuracy = wzConfig['Schedule'].get(
            'StartDateAccuracy', 'estimated')
        endDateTime = wzConfig['Schedule']['EndDate']
        wzEndDate = datetime.datetime.strptime(
            endDateTime, "%Y-%m-%dT%H:%M:%SZ").strftime("%m/%d/%Y")
        wzEndTime = datetime.datetime.strptime(
            endDateTime, "%Y-%m-%dT%H:%M:%SZ").strftime("%H:%M")
        endDateAccuracy = wzConfig['Schedule'].get(
            'EndDateAccuracy', 'estimated')
        wzDaysOfWeek = wzConfig['Schedule']['DaysOfWeek']

        wzStartLat = wzConfig['Location']['BeginningLocation']['Lat']
        wzStartLon = wzConfig['Location']['BeginningLocation']['Lon']
        beginningAccuracy = wzConfig['Location']['BeginningAccuracy']
        wzEndLat = wzConfig['Location']['EndingLocation']['Lat']
        wzEndLon = wzConfig['Location']['EndingLocation']['Lon']
        endingAccuracy = wzConfig['Location']['EndingAccuracy']

        wzLocationMethod = wzConfig['metadata']['wz_location_method']
        lrsType = wzConfig['metadata']['lrs_type']
        locationVerifyMethod = wzConfig['metadata']['location_verify_method']
        dataFeedFrequencyUpdate = wzConfig['metadata']['datafeed_frequency_update']
        timestampMetadataUpdate = wzConfig['metadata']['timestamp_metadata_update']
        contactName = wzConfig['metadata']['contact_name']
        contactEmail = wzConfig['metadata']['contact_email']
        issuingOrganization = wzConfig['metadata']['issuing_organization']
    except KeyError as e:
        logging.error("Invalid Configuration File. Missing field " + str(e))
        raise RuntimeError(
            "Invalid Configuration File. Missing field " + str(e)) from e

    try:
        mapImageZoom = wzConfig.get('ImageInfo', {}).get('Zoom', 0)
        mapImageCenterLat = wzConfig.get(
            'ImageInfo', {}).get('Center', {}).get('Lat', 0.0)
        mapImageCenterLon = wzConfig.get(
            'ImageInfo', {}).get('Center', {}).get('Lon', 0.0)
        # Markers:List of {Name, Color, Location {Lat, Lon, ?Elev}}
        mapImageMarkers = wzConfig.get('ImageInfo', {}).get('Markers', [])
        marker_list = []
        for marker in mapImageMarkers:
            marker_list.append("markers=color:" + marker['Color'].lower() + "|label:" + marker['Name'] + "|" + str(
                marker['Location']['Lat']) + "," + str(marker['Location']['Lon']) + "|")
        mapImageMapType = wzConfig.get('ImageInfo', {}).get('MapType', '')
        mapImageHeight = wzConfig.get('ImageInfo', {}).get('Height', 0)
        mapImageWidth = wzConfig.get('ImageInfo', {}).get('Width', 0)
        mapImageFormat = wzConfig.get('ImageInfo', {}).get('Format', '')
        mapImageString = wzConfig.get('ImageInfo', {}).get('ImageString', '')
    except KeyError:
        pass


def getApproachRegionGeometry(appMapPt, wzMapPt, numLanes, speedLimits, currIndex):
    print(currIndex)
    laneIndex = numLanes - 1
    approachDistance = APPROADH_REGION_TIME * (speedLimits[0] * MPS_PER_MPH)
    currDistance = wzMapPt[currIndex][(numLanes - 1)*5 + 7]
    startDistance = currDistance - approachDistance
    logging.info(str(startDistance) + ', ' +
                 str(currDistance) + ', ' + str(approachDistance))
    if startDistance < 0 and currIndex < 63:
        # Need to use approach region points
        appTotalDistance = appMapPt[-1][(numLanes - 1)*5 + 7]
        currAppDistance = appTotalDistance + startDistance  # startDistance is negative

        maxApproachNumNodes = currIndex - MAX_NUM_NODES
        startIndex = max(findNodeByDistance(appMapPt, numLanes,
                         currAppDistance), len(appMapPt) + maxApproachNumNodes)

        geometry = getMapPointsBetweenIndexes(
            appMapPt, numLanes, startIndex, -1, [])
        geometry = getMapPointsBetweenIndexes(
            wzMapPt, numLanes, 0, currIndex, geometry)

        return geometry
    else:
        startIndex = max(findNodeByDistance(wzMapPt, numLanes,
                         startDistance), currIndex - MAX_NUM_NODES)
        print(startIndex)
        geometry = getMapPointsBetweenIndexes(
            wzMapPt, numLanes, startIndex, currIndex, [])

        return geometry


def findNodeByDistance(arr, numLanes, targetDistance):
    for index, node in enumerate(arr):
        distance = node[(numLanes - 1)*5 + 7]
        if distance > targetDistance:
            return max(index - 1, 0)


def getMapPointsBetweenIndexes(arr, numLanes, startIndex, endIndex, points):
    points = []
    for lane in range(numLanes):
        lane_points = []
        for node in arr[startIndex:endIndex]:
            lane_points.append(
                [node[lane*5 + 0], node[lane*5 + 1], node[lane*5 + 2]])
        points.append(lane_points)
    return points


def segmentToContainers(appMapPt, wzMapPt, numLanes, speedLimits):
    reducedSpeedZones = []
    workersPresentZones = []
    laneClosureZones = []

    reducedSpeedLimitActive = False
    lanesClosureActive = False
    workersPresentActive = False

    allOpenLaneStat = [False] * numLanes
    prevLaneStat = [False] * numLanes

    prevWpStat = False

    defaultSpeedLimit = speedLimits[0]
    prevSpeedLimit = speedLimits[0]

    initialGeometry = []
    for i in range(numLanes):
        initialGeometry.append(copy.deepcopy([]))

    for index, node in enumerate(wzMapPt):
        # 0: latitude
        # 1: longitude
        # 2: altitude
        # 3: lane closure stat
        # 4: lane taper stat
        # repeated for n lanes...

        # 5: bearing
        # 6: wp stat
        # 7: distance
        # 8: speed limit

        lane = 0

        latitude = node[lane*5 + 0]
        longitude = node[lane*5 + 1]
        altitude = node[lane*5 + 2]
        laneStat = []
        for i in range(numLanes):
            laneStat.append(node[i*5 + 3] == 1)
        # laneTaperStat   = node[lane*5 + 4]
        bearing = node[(numLanes-1)*5 + 5]
        wpStat = node[(numLanes-1)*5 + 6] == 1
        distance = node[(numLanes-1)*5 + 7]
        speedLimit = node[(numLanes-1)*5 + 8]

        if wpStat != prevWpStat:
            logging.debug("wpStat change: " +
                          str(wpStat) + ", at " + str(index))
            prevWpStat = wpStat
            if wpStat == False:
                workersPresentActive = False
            else:
                workersPresentActive = True

        if speedLimit != prevSpeedLimit or (reducedSpeedZones and len(reducedSpeedZones[-1]['geometry']) >= MAX_NUM_NODES - 1):
            logging.debug("speed limit change or reset: " +
                          str(speedLimit) + ", at node number " + str(index))

            if reducedSpeedZones:
                for i in range(numLanes):
                    nodeGeometry = [node[i*5 + 0],
                                    node[i*5 + 1], node[i*5 + 2]]
                    reducedSpeedZones[-1]['geometry'][i].append(nodeGeometry)

            prevSpeedLimit = speedLimit
            if speedLimit == defaultSpeedLimit:
                reducedSpeedLimitActive = False
            else:
                reducedSpeedLimitActive = True
                reducedSpeedZones.append({
                    'speedLimit': speedLimits[0],
                    'geometry': copy.deepcopy(initialGeometry),
                    'approachGeometry': getApproachRegionGeometry(appMapPt, wzMapPt, numLanes, speedLimits, index),
                    'workersPresent': workersPresentActive})

        logging.info("laneStat: " +
                     str(laneStat) + ", at node number " + str(index))

        if laneStat != prevLaneStat or (laneClosureZones and len(laneClosureZones[-1]['geometry']) >= MAX_NUM_NODES - 1):
            logging.info("laneStat change or reset: " +
                         str(laneStat) + ", at node number " + str(index))

            if laneClosureZones:
                for i in range(numLanes):
                    nodeGeometry = [node[i*5 + 0],
                                    node[i*5 + 1], node[i*5 + 2]]
                    laneClosureZones[-1]['geometry'][i].append(nodeGeometry)

            prevLaneStat = laneStat
            if laneStat == allOpenLaneStat:
                lanesClosureActive = False
            else:
                lanesClosureActive = True
                laneClosureZones.append({
                    'laneStat': laneStat,
                    'geometry': copy.deepcopy(initialGeometry),
                    'approachGeometry': getApproachRegionGeometry(appMapPt, wzMapPt, numLanes, speedLimits, index),
                    'workersPresent': workersPresentActive})

        if reducedSpeedLimitActive:
            if workersPresentActive and not reducedSpeedZones[-1]['workersPresent']:
                reducedSpeedZones[-1]['workersPresent'] = True
            for i in range(numLanes):
                nodeGeometry = [node[i*5 + 0], node[i*5 + 1], node[i*5 + 2]]
                reducedSpeedZones[-1]['geometry'][i].append(nodeGeometry)

        if lanesClosureActive:
            if workersPresentActive and not reducedSpeedZones[-1]['workersPresent']:
                reducedSpeedZones[-1]['workersPresent'] = True
            for i in range(numLanes):
                nodeGeometry = [node[i*5 + 0], node[i*5 + 1], node[i*5 + 2]]
                laneClosureZones[-1]['geometry'][i].append(nodeGeometry)

    return (reducedSpeedZones, workersPresentZones, laneClosureZones)


def getReferencePoint(node):
    p1 = node[0]
    p2 = node[-1]
    return [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, (p1[2] + p2[2]) / 2]


def getIds(Ids, index):
    if index >= 4:
        return {'operatorId': OPERATOR_ID, 'uniqueId': str(uuid.uuid4())}
    else:
        return Ids[index]


def build_messages():
    global files_list

    wzStart = wzStartDate.split('/') + wzStartTime.split(':')
    wzEnd = wzEndDate.split('/') + wzEndTime.split(':')

    timeOffset = 0  # UTC time offset in minutes for Eastern Time Zone
    # applicable heading tolerance set to 20 degrees (+/- 20deg?)
    hTolerance = 20

    roadWidth = totalLanes*laneWidth*100  # roadWidth in cm
    eventLength = wzLen  # WZ length in meters, computed earlier

    speedLimit = ['vehicleMaxSpeed', speedList[0], speedList[1],
                  speedList[2]]

# -------------------------------------------------
#
#   BUILD XML (exer) file for 'Common Container'...
#
# -------------------------------------------------

###
#
#   Build multiple .exer (XML) files for segmented message.
#   Build one file for each message segment
#
#   Created June, 2018
#
####

    rsmSegments = []

    wzdx_outFile = tempfile.gettempdir() + '/WZDx_File-' + ctrDT + '.geojson'
    logging.debug('WZDx output file path: ' + wzdx_outFile)
    wzdxFile = open(wzdx_outFile, 'w')
    files_list.append(wzdx_outFile)

    devnull = open(os.devnull, 'w')

    reducedSpeedZones, workersPresentZones, laneClosureZones = segmentToContainers(
        appMapPt, wzMapPt, laneStat[0][0], speedLimit[1:])

###
# Create and open output xml file...
###
    if noRSM:
        logging.warning('Accuracy too low, not adding RSM files to files_list')

    heading = {'heading': appHeading, 'tolerance': hTolerance}

###
#   Build xml for common container...
###

    # commonContainer = wz_xml_builder.build_xml_CC(idList, wzStart, wzEnd, timeOffset, wzDaysOfWeek, c_sc_codes, newRefPt, appHeading, hTolerance,
    #                                                   speedLimit, laneWidth, roadWidth, eventLength, laneStat, appMapPt, msgSegList, currSeg, wzDesc)

###
#       WZ length, LC characteristic, workers present, etc.
###

    # Workers present flag, 0=no, 1=yes   NOT Used in RSM (was for BIM)
    # wpFlag = 0
    # RN = False  # Boolean - True: Generate reduced nodes for closed lanes
    #        - False: Generate all nodes for closed lanes
###
#   Build WZ containers
###

    eventIdList = []

    numRsms = 0

    initialGeometry = []
    if reducedSpeedZones:
        for i in range(len(reducedSpeedZones[0]['geometry'])):
            initialGeometry.append([])

        for rsz in reducedSpeedZones:
            numRsms += 1
    else:
        for lc in laneClosureZones:
            numRsms += 1

    for i in range(min(numRsms, 4)):
        eventIdList.append(
            {'operatorId': OPERATOR_ID, 'uniqueId': str(uuid.uuid4())})

    idIndex = 0

    # reducedSpeedZones, workersPresentZones, laneClosureZones
    if reducedSpeedZones:
        for rsz in reducedSpeedZones:
            eventId = getIds(eventIdList, idIndex)

            rsm = {}
            rsm['RoadsideSafetyMessage'] = {}
            commonContainer = wz_xml_builder.buildCommonContainer(eventId, wzStart, wzEnd, timeOffset, wzDaysOfWeek, c_sc_codes, getReferencePoint(rsz['geometry'][0]),
                                                                  heading, laneWidth, roadWidth, laneStat[0][0], rsz['approachGeometry'], wzDesc, eventIdList)
            rsm['RoadsideSafetyMessage']['commonContainer'] = commonContainer

            speedLimit = {
                'type': 'vehicleMaxSpeed',
                'value': rsz['speedLimit']
            }
            rszContainer = wz_xml_builder.buildRszContainer(
                speedLimit, rsz['geometry'], laneWidth)
            rsm['RoadsideSafetyMessage']['rszContainer'] = rszContainer

            for laneClosure in laneClosureZones:
                geometry = copy.deepcopy(initialGeometry)
                for index, node in enumerate(laneClosure['geometry'][0]):
                    if node in rsz['geometry'][0]:
                        for lane, obj in enumerate(laneClosure['geometry']):
                            geometry[lane].append(obj[index])
                if geometry != initialGeometry:
                    laneClosureContainer = wz_xml_builder.buildLaneClosureContainer(
                        laneClosure['laneStat'], None, geometry, laneWidth)
                    rsm['RoadsideSafetyMessage']['laneClosureContainer'] = laneClosureContainer

            if rsz['workersPresent']:
                situationalContainer = wz_xml_builder.buildSituationalContainer(
                    None, None, True, None)
                rsm['RoadsideSafetyMessage']['situationalContainer'] = situationalContainer

            rsmSegments.append(rsm)
            idIndex += 1
    else:
        for laneClosure in laneClosureZones:
            eventId = getIds(eventIdList, idIndex)

            rsm = {}
            rsm['RoadsideSafetyMessage'] = {}
            commonContainer = wz_xml_builder.buildCommonContainer(eventId, wzStart, wzEnd, timeOffset, wzDaysOfWeek, c_sc_codes, getReferencePoint(laneClosure['geometry'][0]),
                                                                  heading, laneWidth, roadWidth, laneStat[0][0], laneClosure['approachGeometry'], wzDesc, eventIdList)
            rsm['RoadsideSafetyMessage']['commonContainer'] = commonContainer

            laneClosureContainer = wz_xml_builder.buildLaneClosureContainer(
                laneClosure['laneStat'], None, laneClosure['geometry'], laneWidth)
            rsm['RoadsideSafetyMessage']['laneClosureContainer'] = laneClosureContainer

            if laneClosure['workersPresent']:
                situationalContainer = wz_xml_builder.buildSituationalContainer(
                    None, None, True, None)
                rsm['RoadsideSafetyMessage']['situationalContainer'] = situationalContainer

            if len(eventIdList) < 4:
                eventIdList.append(eventId)

            rsmSegments.append(rsm)
            idIndex += 1

    if not noRSM:
        numSegments = len(rsmSegments)
        for index, rsm in enumerate(rsmSegments):
            xml_outFile = tempfile.gettempdir() + '/RSZW_MAP_xml_File-' + ctrDT + '-' + \
                str(index + 1)+'_of_'+str(numSegments)+'.xml'
            logging.debug('RSM XML output file path: ' + xml_outFile)

            uper_outFile = tempfile.gettempdir() + '/RSZW_MAP_xml_File-' + ctrDT + '-' + \
                str(index + 1)+'_of_'+str(numSegments)+'.uper'
            logging.debug('RSM UPER output file path: ' + uper_outFile)

            files_list.append(xml_outFile)
            # files_list.append(uper_outFile)

            with open(xml_outFile, 'w') as xmlFile:
                rsm_xml = xmltodict.unparse(
                    rsm, short_empty_elements=True, pretty=True, indent='  ')
                xmlFile.write(rsm_xml)

                xmlFile.close()

        # linux = subprocess.check_output(
        #     ['uname', '-a'], stderr=subprocess.STDOUT).decode('utf-8')
        # logging.debug("Linux Installation Information: " + str(linux))
        # try:
        #     p = subprocess.Popen(['./EventGridTrigger1/jvm/bin/java', '-jar', './EventGridTrigger1/CVMsgBuilder_xmltouper_v8.jar', str(
        #         xml_outFile), str(uper_outFile)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #     output, err = p.communicate(
        #         b"input data that is passed to subprocess' stdin")
        #     # rc = p.returncode
        #     logging.error(
        #         'ERROR: RSM UPER conversion FAILED. Output: ' + str(output))
        #     logging.error(
        #         'ERROR: RSM UPER conversion FAILED. Error: ' + str(err))
        # except Exception as e:
        #     logging.error(
        #         'ERROR: RSM UPER conversion FAILED. Message: ' + str(e))
        # # subprocess.call(['./EventGridTrigger1/jvm/bin/java', '-jar', './EventGridTrigger1/CVMsgBuilder_xmltouper_v8.jar', str(xml_outFile), str(uper_outFile)]) #,stdout=devnull

        # if not os.path.exists(uper_outFile) or os.stat(uper_outFile).st_size == 0:
        #     logging.error('ERROR: UPER FILE DOES NOT EXIST OR HAS SIZE 0')
        #     logging.error('ERROR: RSM UPER conversion FAILED')

    # currSeg = currSeg+1
    # pass
    info = {}
    info['feed_info_id'] = feed_info_id
    info['license'] = "https://creativecommons.org/publicdomain/zero/1.0/"
    info['road_name'] = roadName
    info['description'] = wzDesc
    info['direction'] = direction
    info['beginning_cross_street'] = beginningCrossStreet
    info['ending_cross_street'] = endingCrossStreet
    info['beginning_milepost'] = beginningMilepost
    info['ending_milepost'] = endingMilepost
    info['issuing_organization'] = issuingOrganization
    info['creation_date'] = creationDate
    info['update_date'] = updateDate
    info['event_status'] = eventStatus
    info['beginning_accuracy'] = beginningAccuracy
    info['ending_accuracy'] = endingAccuracy
    info['start_date_accuracy'] = startDateAccuracy
    info['end_date_accuracy'] = endDateAccuracy

    info['metadata'] = {}
    info['metadata']['wz_location_method'] = wzLocationMethod
    info['metadata']['lrs_type'] = lrsType
    info['metadata']['location_verify_method'] = locationVerifyMethod
    if dataFeedFrequencyUpdate:
        info['metadata']['datafeed_frequency_update'] = dataFeedFrequencyUpdate
    info['metadata']['timestamp_metadata_update'] = timestampMetadataUpdate
    info['metadata']['contact_name'] = contactName
    info['metadata']['contact_email'] = contactEmail
    info['metadata']['issuing_organization'] = issuingOrganization

    info['types_of_work'] = typeOfWork
    info['lanes_obj'] = lanes_obj
    logging.info('Converting RSM XMl to WZDx message')
    wzdx = {}
    try:
        wzdx = rsm_2_wzdx_translator.wzdx_creator(
            rsmSegments, int(dataLane), info)
        logging.info("WZDx message generated and validated successfully")
    except Exception as e:
        logging.error("WZDx Message Generation Failed: " + str(e))
        raise e
    wzdxFile.write(json.dumps(wzdx, indent=2))
    wzdxFile.close()


###
#   > > > > > > > > > > > START MAIN PROCESS < < < < < < < < < < < < < < <
###


def startMainProcess(vehPathDataFile):

    # global  vehPathDataFile                                         #collected vehicle path data file name
    global refPtIdx  # data point number where reference point is set
    global wzLen  # work zone length in meters
    global wzMapLen  # Mapped approach and wz lane length in meters
    global appHeading  # approach heading
    global sampleFreq
    global noRSM  # If accuracy is too low, do not generate RSM message
    global msgSegList  # WZ message segmentation list
# global  wzMapBuiltSuccess                                       #WZ map built successful or not flag
# wzMapBuiltSuccess = False                                       #Default set to False

    csvList = []
    csvList = list(csv.reader(open(vehPathDataFile)))

    timeRegex = '[0-9]{2}(:[0-9]{2}){3}'
    lastIndex = len(csvList) - 1
    logging.debug('Length of CSV data: ' + str(lastIndex))
    time1 = re.search(timeRegex, str(csvList[1])).group(0).split(':')
    time2 = re.search(timeRegex, str(csvList[lastIndex])).group(0).split(':')

    deltaTime = (int(time2[0])-int(time1[0]))*3600 + (int(time2[1])-int(time1[1])) * \
        60 + (int(time2[2])-int(time1[2])) + (int(time2[3])-int(time1[3]))/100
    if (deltaTime) != 0:
        sampleFreq = lastIndex/deltaTime
    else:
        sampleFreq = 10
    if sampleFreq < 1 or sampleFreq > 10:
        sampleFreq = 10

    logging.debug('Sample Frequency: ' + str(sampleFreq))

    totRows = len(csvList) - 1  # total records or lines in file

###
#
#   Call function to read and parse the vehicle path data file created by the 'vehPathDataAcq.pyw'
#   to build vehicle path data array, lane status and workers presence status arrays.
#
#   refPtIdx, wzLen and appHeading values are returned in atRefPoint list...
#
#   Updated on Aug. 23, 2018
#
###
    logging.debug('Length of Path Point Before: ' + str(len(pathPt)))

    # temporary list to hold return values from function below
    atRefPoint = [0, 0, 0, 0]
    wz_vehpath_lanestat_builder.buildVehPathData_LaneStat(
        vehPathDataFile, totalLanes, pathPt, laneStat, wpStat, refPoint, atRefPoint, sampleFreq)
    logging.debug('Length of Path Points After: ' + str(len(pathPt)))
    refPtIdx = atRefPoint[0]
    wzLen = atRefPoint[1]
    appHeading = atRefPoint[2]
    maxHDOP = atRefPoint[3]
    maxAllowableHDOP = 2        # meters
    if maxHDOP > maxAllowableHDOP:
        logging.info('GPS Accuracy too low, max value of HDOP: ' + str(maxHDOP) +
                     ' is greater than the limit of ' + str(maxAllowableHDOP) + '. Cannot upload RSM messages')
        noRSM = True
    else:
        noRSM = False
        logging.info('GPS Accuracy high enough, max value of HDOP: ' + str(maxHDOP) +
                     ' is greater than the limit of ' + str(maxAllowableHDOP) + '. RSM messages will be uploaded')
    noRSM = False


###
#   ====================================================================================================
###
#    -----  Read and processed vehPathDataFile
#           Compiled pathPt, reference point and lane closures  -----
###
###
#   Function to populate Approach Lane Map points...
#
#   refPtIdx determined in the above function...
###

###
#   'laneType'              1 = Approach lanes, 2 = wz Lanes for mapping
#   'pathPt'                contains list of data points collected by driving the vehicle on one open WZ lane
#   'appMapPt/wzMapPt'      constructed node list for lane map for BIM (RSM)
#                           contains lat,lon,alt,lcloStat for each node, each lane + heading + WP flag + distVec (dist from prev. node)
#   'lanePadApp/lanePadWz'  lane padding in addition to laneWidth
#   'refPtIdx'              Data location of the reference point in pathPt array
#   'laneStat'              A two-dimensional list to hold lane status, 0=open, 1=closed.
#                               Generated from lane closed/opened marker from collected data
#                               List location [0,0,0] provides total number of lanes
#                               It holds for each lane closed/opened instance, data point index, lane number and lane status (1/0)
#   'wpStat'                list containing location where 'workers present' is set/unset
#   'dataLane'              Lane on which the vehicle path data for wz mapping was collected.
#                               'dataLane' is used to derive map data for the adjacent lanes. One lane to the left of the 'dataLane' and one to right in
#                               case of total 3 lanes. For more than 5 lanes, data from multiple lanes to be collected to create map for adjascent lanes
#   'laneWidth'             lane width in meters
#
#   For approach lanes, map for all lanes are created
#
#   For wz lanes, node points for map for all lanes including closed lanes are created.
#
###

    wzMapLen = [0, 0]  # both approach and wz mapped length
    laneType = 1  # approach lanes
    logging.debug(str(laneType) + ', ' + str(len(pathPt)) + ', ' + str(len(appMapPt)) + ', ' +
                  str(laneWidth) + ', ' + str(lanePadApp) + ', ' + str(refPtIdx) + ', ' + str(appMapPtDist))
    logging.debug(str(laneStat) + ',' + str(wpStat) + ', ' + str(dataLane) +
                  ', ' + str(wzMapLen) + ', ' + str(speedList) + ', ' + str(sampleFreq))
    wz_map_constructor.getLanePt(laneType, pathPt, appMapPt, laneWidth, lanePadApp,
                                 refPtIdx, appMapPtDist, laneStat, wpStat, dataLane, wzMapLen, speedList, sampleFreq)
    logging.debug('Length of Approach Points: ' + str(len(appMapPt)))
    logging.debug('Length of Path Point: ' + str(len(pathPt)))


###
#
#   Now repeat the above for WZ map data point array starting from the ref point until end of the WZ
#   First WZ map point closest to the reference point is the next point after the ref. point.
#
###

    laneType = 2  # wz lanes

    logging.debug('Length of Work Zone Points Before: ' + str(len(wzMapPt)))

    print(laneStat)
    print(pathPt)
    print(dataLane)

    # Append all nodes to wzMapPt
    wz_map_constructor.getLanePt(laneType, pathPt, wzMapPt, laneWidth, lanePadWZ, refPtIdx,
                                 wzMapPtDist, laneStat, wpStat, dataLane, wzMapLen, speedList, sampleFreq)
    logging.debug('Length of Work Zone Points After: ' + str(len(wzMapPt)))
    logging.debug('Length of Path Point: ' + str(len(pathPt)))


###
#   print/log lane status and workers present/not present status...
###

    laneStatIdx = len(laneStat)
    if laneStatIdx > 1:  # have lane closures...NOTE: Index 0 location is dummy value...
        for L in range(1, laneStatIdx):
            stat = 'Start'
            if laneStat[L][2] == 0:
                stat = 'End'
        pass
    pass

    wpStatIdx = len(wpStat)
    if wpStatIdx > 0:  # have workers present/not present
        for w in range(0, wpStatIdx):
            stat = 'End'
            if wpStat[w][1] == 1:
                stat = 'Start'
        pass
    pass
    build_messages()


##############################################################################################
#
# ----------------------------- END of startMainProcess --------------------------------------
#
###############################################################################################

def openLog():
    global logFile
    if os.path.exists(logFileName):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not
    logFile = open(logFileName, append_write)


def uploadArchive(zip_name, container_name):
    logging.debug('Creating blob in azure: ' + zip_name +
                  ', in container: ' + container_name)
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=zip_name.split('/')[-1])
    logging.debug('Uploading zip archive to blob')
    with open(zip_name, 'rb') as data:
        blob_client.upload_blob(data, overwrite=True)

    logging.info('Data upload successful! Please navigate to\nhttp://www.neaeraconsulting.com/V2x_Verification\nto view and verify the mapped workzone.\nYou will find your data under\n' + name_id)


logFileName = tempfile.gettempdir() + '/data_collection_log.txt'
local_updated_config_path = tempfile.gettempdir() + '/updatedConfig.json'
# logFile = ''
mapFileName = tempfile.gettempdir() + '/mapImage.png'


def updateConfigImage(vehPathDataFile):
    global needsImage
    global wzConfig
    global center
    global wzStartLat
    global wzStartLon
    global wzEndLat
    global wzEndLon

    try:

        got_rp = False
        with open(vehPathDataFile, 'r') as f:
            headers = f.readline()
            data = f.readline().rstrip('\n')
            while data:
                fields = data.split(',')
                nextData = f.readline().rstrip('\n')
                if not got_rp and (fields[8] == 'RP' or fields[8] == 'WP+RP' or fields[8] == 'LC+RP'):
                    # Starting location found
                    wzConfig['Location']['BeginningLocation']['Lat'] = float(
                        fields[3])
                    wzStartLat = float(fields[3])
                    wzConfig['Location']['BeginningLocation']['Lon'] = float(
                        fields[4])
                    wzStartLon = float(fields[4])
                elif (fields[8] == 'Data Log' and fields[9] == 'False') or not nextData:
                    # Ending location found
                    wzConfig['Location']['EndingLocation']['Lat'] = float(
                        fields[3])
                    wzEndLat = float(fields[3])
                    wzConfig['Location']['EndingLocation']['Lon'] = float(
                        fields[4])
                    wzEndLon = float(fields[4])

                data = nextData

        centerLat = (float(wzStartLat) + float(wzEndLat))/2
        centerLon = (float(wzStartLon) + float(wzEndLon))/2
        center = str(centerLat) + ',' + str(centerLon)

        north = max(float(wzStartLat), float(wzEndLat))
        south = min(float(wzStartLat), float(wzEndLat))
        east = max(float(wzStartLon), float(wzEndLon))
        west = min(float(wzStartLon), float(wzEndLon))
        calcZoomLevel(north, south, east, west, mapImageWidth, mapImageHeight)

        marker_list = []
        marker_list.append("markers=color:green|label:Start|" +
                           str(wzStartLat) + "," + str(wzStartLon) + "|")
        marker_list.append("markers=color:red|label:End|" +
                           str(wzEndLat) + "," + str(wzEndLon) + "|")

        encoded_string = ''
        get_static_google_map(mapFileName, center=center, zoom=zoom, imgsize=(
            mapImageWidth, mapImageHeight), imgformat="png", markers=marker_list)
        with open(mapFileName, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        needsImage = False

        wzConfig['ImageInfo'] = {}
        wzConfig['ImageInfo']['Zoom'] = zoom
        wzConfig['ImageInfo']['Center']['Lat'] = centerLat
        wzConfig['ImageInfo']['Center']['Lon'] = centerLon

        markers = []
        markers.append({'Name': 'Start', 'Color': 'Green', 'Location': {
            'Lat': wzStartLat, 'Lon': wzStartLon, 'Elev': None}})
        markers.append({'Name': 'End', 'Color': 'Red', 'Location': {
            'Lat': wzEndLat, 'Lon': wzEndLon, 'Elev': None}})
        wzConfig['ImageInfo']['Markers'] = markers

        wzConfig['ImageInfo']['MapType'] = mapImageMapType
        wzConfig['ImageInfo']['Height'] = mapImageHeight
        wzConfig['ImageInfo']['Width'] = mapImageWidth
        wzConfig['ImageInfo']['Format'] = mapImageFormat

        wzConfig['ImageInfo']['ImageString'] = encoded_string

        cfg = open(local_updated_config_path, 'w')
        cfg.write(json.dumps(wzConfig, indent='  '))
        cfg.close()
    except KeyError as e:
        logging.error("Invalid configuration file (Missing " +
                      str(e) + "). Not updating image")
    except Exception as e:
        logging.error(
            "Error during generation of configuration file image. Not updating image")


def get_static_google_map(filename_wo_extension, center=None, zoom=None, imgsize="640x640", imgformat="png",
                          maptype="roadmap", markers=None):
    """retrieve a map (image) from the static google maps server 

     See: http://code.google.com/apis/maps/documentation/staticmaps/

        Creates a request string with a URL like this:
        http://maps.google.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=14&size=512x512&maptype=roadmap
&markers=color:blue|label:S|40.702147,-74.015794&sensor=false"""

    # assemble the URL
    # base URL, append query params, separated by &
    request = "http://maps.google.com/maps/api/staticmap?"
    apiKey = os.getenv('GOOGLE_MAPS_API_KEY')
    # if center and zoom  are not given, the map will show all marker locations
    request += "key=%s&" % apiKey
    if center != None:
        request += "center=%s&" % center
    if zoom != None:
        # zoom 0 (all of the world scale ) to 22 (single buildings scale)
        request += "zoom=%i&" % zoom

    request += "size=%ix%i&" % (imgsize)  # tuple of ints, up to 640 by 640
    request += "format=%s&" % imgformat
    request += "bearing=90&"
    # request += "maptype=%s&" % maptype  # roadmap, satellite, hybrid, terrain

    # add markers (location and style)
    if markers != None:
        for marker in markers:
            request += "%s&" % marker

    request = request.rstrip('&')
    # #request += "mobile=false&"  # optional: mobile=true will assume the image is shown on a small screen (mobile device)
    # request += "sensor=false"   # must be given, deals with getting loction from mobile device
    # try:
    urllib.request.urlretrieve(request, filename_wo_extension)


# Calculate google maps zoom level to fit a rectangle
def calcZoomLevel(north, south, east, west, pixelWidth, pixelHeight):
    global zoom
    global centerLat

    GLOBE_WIDTH = 256
    ZOOM_MAX = 21
    angle = east - west
    if angle < 0:
        angle += 360
    zoomHoriz = round(math.log(pixelWidth * 360 / angle /
                      GLOBE_WIDTH) / math.log(2)) - 1

    angle = north - south
    centerLat = (north + south) / 2
    if angle < 0:
        angle += 360
    zoomVert = round(math.log(pixelHeight * 360 / angle / GLOBE_WIDTH *
                     math.cos(centerLat*math.pi/180)) / math.log(2)) - 1

    zoom = max(min(zoomHoriz, zoomVert, ZOOM_MAX), 0)


def initVars():
    global wzConfig
    global cDT
    global pathPt
    global appMapPt
    global wzMapPt
    global refPoint
    global appHeading
    global refPtIdx
    global gotRefPt
    global appMapPtDist
    global wzMapPtDist
    global laneStat
    global laneStatIdx
    global wpStat
    global wpStatIdx
    global wzLen
    global msgSegList
    global files_list
    global ctrDT

    wzConfig = {}

    ###
    #   --------------------------------------------------------------------------------------------------
    ###
    #   Get current date and time...
    ###

    cDT = datetime.datetime.now().strftime('%m/%d/%Y - ') + \
        time.strftime('%H:%M:%S')

    ###
    #   Map builder output log file...
    ###

    # --------------------------------------------------------------------------------------------------
    #       Following are local variables with set default values...
    #
    #	Setup array for collected data for mapping, construcyed node points for approach and WZ lanes, and
    #       reference point
    # --------------------------------------------------------------------------------------------------

    pathPt = []  # test vehicle path data points generated by WZ_VehPathDataAcq.py module
    appMapPt = []  # array to hold approach lanes map node points
    wzMapPt = []  # array to hold wz lanes map node points
    # Ref. point (lat, lon, alt), initial value... ONLY ONE reference point...
    refPoint = [0, 0, 0]
    appHeading = 0  # applicable Heading to the WZ event at the ref. point. Needed for XML for RSM Message

    ###
    #	Variables for book keeping...
    ###

    refPtIdx = 0  # index into pathPt array where the reference point is...
    gotRefPt = False  # default

    ###
    #	For fixed equidistant node selection for approach and WZ lanes
    #
    #       As of Feb. 2018 --  Node point selection based on equidistant is NO LONGER in use...
    #                           Replace by dynamic node point selection based on right triangle using change in heading angle method...
    ###

    # set distance in meters between map data points for approach lanes - not used in the algo.
    appMapPtDist = 50
    # set distance in meters between map data point for WZ map - not used in the algo.
    wzMapPtDist = 200

    ###
    #	Keep track of lane status such as point where lane closed or open is marked within WZ for each lane
    #       including offset from ref. pt.
    #
    #       Contains 4 elements - [data point#, lane#, lane status (0-open/1-closed), offset from ref. point)
    ###

    # contains lane status, data point#, lane #, 0/1 0=open, 1=closed and offset from ref point.
    laneStat = []
    # Generated from lane closed/opened marker from colleted data
    laneStatIdx = 0  # laneStat + lcOffset array index

    ###
    #	Keep track of workers present status such as point where they are present and then not present at **road level**
    #       including offset from the reference point
    ###

    wpStat = []  # array to hold WP location, WP status and offset from ref. point default - no workers present
    wpStatIdx = 0  # wpStat array index

    ###
    #       Work zone length
    ###

    wzLen = 0  # init WZ length

    msgSegList = []  # WZ message node segmentation list

    files_list = []

    ctrDT = datetime.datetime.now().strftime('%Y%m%d-') + time.strftime('%H%M%S')


def build_messages_and_export(wzID, vehPathDataFile, local_config_path, updateImage):
    global blob_service_client
    global name_id
    global files_list

    initVars()

    configRead(local_config_path)

    description = wzDesc.lower().strip().replace(' ', '-')
    road_name = roadName.lower().strip().replace(' ', '-')
    name_id = description + '--' + road_name
    logging.info('WZID: ' + str(name_id))

    if not mapImageString:
        updateImage = True

    if updateImage:
        updateConfigImage(vehPathDataFile)
        files_list.append(local_updated_config_path)
    else:
        files_list.append(local_config_path)
    startMainProcess(vehPathDataFile)
    files_list.append(vehPathDataFile)
    files_list.append(local_config_path)

    zip_name = tempfile.gettempdir() + '/wzdc-exports--' + name_id + '.zip'
    logging.info('Creating zip archive: ' + zip_name)

    zipObj = zipfile.ZipFile(zip_name, 'w')
    names = []
    for filename in files_list:
        if not os.path.exists(filename):
            logging.info(
                "File does not exist. not adding to archive: " + filename)
            continue
        name = filename.split('/')[-1]
        name_orig = name
        name_wo_ext = name[:name.rfind('.')]
        if '.csv' in filename.lower():
            name = 'path-data--' + name_id + '.csv'
        elif '.json' in filename.lower():
            if updateImage:
                name = 'config--' + name_id + '-updated.json'
            else:
                name = 'config--' + name_id + '.json'
        elif '.xml' in filename.lower():
            number = name[name.rfind('-')+1:name.rfind('.')]
            name = 'rsm-xml--' + name_id + '--' + number + '.xml'
        elif '.uper' in filename.lower():
            number = name[name.rfind('-')+1:name.rfind('.')]
            name = 'rsm-uper--' + name_id + '--' + number + '.uper'
        elif '.geojson' in filename.lower():
            name = 'wzdx--' + name_id + '.geojson'
        else:
            logging.info(f'File not caught. path: {filename}, name: {name}')
            continue
        logging.info('Adding file to archive: ' + filename + ', as: ' + name)
        if name not in names:
            names.append(name)
            zipObj.write(filename, name)

    # close the Zip File
    zipObj.close()

    container_name = 'workzonedatauploads'

    uploadArchive(zip_name, container_name)


def main():
    wzID = 'demo-test-1-south--i-25'
    vehPathDataFile = './sample_files/path-data--' + wzID + '.csv'
    local_config_path = './sample_files/config--' + wzID + '.json'
    build_messages_and_export(wzID, vehPathDataFile,
                              local_config_path, False)


if __name__ == "__main__":
    main()
