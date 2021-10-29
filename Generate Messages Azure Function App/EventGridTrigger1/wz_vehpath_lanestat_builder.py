#!/usr/bin/env python3
###
#
#   This module was originally in the WZ_MapBuilder.py main module
#
#   Separated as callable module
#
#   August 22, 2018
#
###
#   Function: Read vehicle path data file and build following:
#
#       Input:
#           vehPathDataFile - collected vehicle path data file
#           totLanes        - total number lanes in WZ
#           sampleFreq      - GPS data sampling frequency used for computing distance traveled and locations of LC/LO/WP, etc.
#
#       Output:
#           pathPt          - array containing vehicle path data points used for determining lane geometry node points
#                             speed,lat,lon,alt,heading
#           laneStat        - array consisting of lane status indicating lane closures and openings
#           wpStat          - array consisting of workers presence status
#           refPoint        - reference point indicating start of event (lat,lon,alt)
#           refPtIdx        - index in pathPt array for reference point
#           wzLen           - computed WZ length
#
#
###


import csv  # csv file processor

# def buildVehPathData_LaneStat (vehPathDataFile,totalLanes,pathPt,laneStat,wpStat,refPoint,refPtIdx,appHeading,wzLen,sampleFreq):


def buildVehPathData_LaneStat(vehPathDataFile, totalLanes, pathPt, laneStat, wpStat, refPoint, atRefPoint, sampleFreq):

    newFormat = True  # set new data format to true...

    gotRefPt = False  # default
    laneStatIdx = 0  # laneStat + lcOffset array index
    wpStatIdx = 0  # wpStat array index
    rowKt = 0  # input record processing counter

    refPtIdx = 0  # ref point index
    wzLen = 0  # wz length in meters
    appHeading = 0  # applicable heading angle

    maxHDOP = 0

###
#   Following variables are modified in this function and the modified value is available only if they are declared
#   as global for it's value to be available in the calling main function. Otherwise, it remains as local and updated value
#   is not affacted in the calling routine.
####

#    global  refPtIdx
#    global  wzLen

###
#   Store total lanes in laneStat list at the first location
#   Following for total lanes added on Nov. 2, 2017
###

    # Total lanes is stored in the first(0) location in array, rest values are set to zero
    laneStat.insert(laneStatIdx, list((totalLanes, 0, 0, 0)))
    laneStatIdx += 1  # Incr the index for next set of values

###
#   Read input file as csv and process each record...
###

    with open(vehPathDataFile, newline='') as csvFile:
        csvReader = csv.reader(csvFile)
        next(csvReader)  # skip the first header line
        prevMarker = (None, None)

        for row in csvReader:
            if float(row[2]) > maxHDOP:
                maxHDOP = float(row[2])
#       *** CSV FORMAT ***
#
#       Input Data:   ---- This is NEW CSV file format for RSZW/LC Mapping Application ----
#       row[0]  =   GPSTime/GPSDate
#       row[1]  =   # of Satellites
#       row[2]  =   HDOP
#       row[3]  =   Latitude (Decimal Degrees)
#       row[4]  =   Longitude (Decimal Degrees)
#       row[5]  =   Altitude (meters)
#       row[6]  =   Speed (m/s)
#       row[7]  =   Heading (angle degrees)
#       row[8,9]=   Indicates a marker
#                   "RP" Reference Point - Use lat,lon,alt from the same line
#                   "LC" Lane Closed - followed by lane number
#                   "LC+RP" Lane Closed + Ref. Point - followed by lane number (if ref. point not indicated)
#                   "LO" Lane Opened - followed by lane number
#                   "WP" Workers Present" - followed by TRUE/FALSE
#                   "WP+RP" Workers lcwpStatPresent + Ref. Point - WP + Ref. Point (if Ref. Pt is not indicated)
#                   "Data Log" followed by TRUE (When FALSE, no data is logged. Previous record time shows when logging stopped)
#                   "Application Ended", followed by null
#
#
#       pathPt  =   An array to hold following for creating map points for approach and wz lanes with indications for WP and LC/LO
#                   index, speed, lat, lon, alt, heading, wp status, lane# and status

###
#               Ref point marker. All lat/lon are represented in micro degrees. The collected lat/lon are in degrees.
#               The values are multiplied by 10000000 in the function where xml is being created...
#
###
            marker = row[8].upper()

            # ref pt marker support for old and new marker
            if gotRefPt == False and (marker == "RP" or marker == "LC+RP" or marker == "WP+RP"):
                refPoint[0] = row[3]  # lat
                refPoint[1] = row[4]  # lon
                refPoint[2] = row[5]  # alt
                # applicableHeading for XML file. Currently taken from the mapping vehilce heading at ref. point
                appHeading = row[7]
                refPtIdx = rowKt  # current input line (starts with 0)
                gotRefPt = True
                if marker == "LC+RP" or marker == "WP+RP":
                    prevMarker = (marker.replace("+RP", ""), row[9])

                #print ("\n --- Reference Point @ data point",refPtIdx,"(lat,Lon,Alt):",row[3], ",", row[4], ",", row[5])
                    # end of reference point

###
#               Lane closed marker
###
            # lane closed marker
            # or marker == "LC+RP" handled by prevMarker
            elif marker == "LC" or prevMarker[0] == "LC":
                if prevMarker[0] == "LC":
                    lc = int(prevMarker[1])
                    if marker != "":
                        prevMarker = (marker, row[9])
                    else:
                        prevMarker = (None, None)
                else:
                    lc = int(row[9])
                # LC location, lane number, status flag, and offset from ref. pt.
                laneStat.insert(laneStatIdx, list((rowKt, lc, 1, int(wzLen))))
                laneStatIdx += 1  # incr array index

###
#               Lane opened marker
###
            elif marker == "LO" or prevMarker[0] == "LO":  # lane opened marker
                if prevMarker[0] == "LO":
                    lc = int(prevMarker[1])
                    if marker != "":
                        prevMarker = (marker, row[9])
                    else:
                        prevMarker = (None, None)
                else:
                    lc = int(row[9])
                lc = int(row[9])  # lane number starts from 0
                # LO location, lane number, status flag and offset from ref. pt.
                laneStat.insert(laneStatIdx, list((rowKt, lc, 0, int(wzLen))))
                laneStatIdx += 1  # incr array index

###
#               Workers present / not present Marker
###
            elif marker == "WP" or prevMarker == "WP":  # WP Flag
                # wp = 1
                if prevMarker[0] == "WP":
                    if marker != "":
                        prevMarker = (marker, row[9])
                    else:
                        prevMarker = (None, None)
                    wp = 0 if prevMarker[1].upper() == "FALSE" else 1
                else:
                    wp = 0 if row[9].upper() == "FALSE" else 1
                # WP Status flag (converted from boolean to 0/1), location and offset from Ref Point
                wpStat.insert(wpStatIdx, list((rowKt, wp, int(wzLen))))
                wpStatIdx += 1  # incr index
###
#               Insert(save) vehicle path data point to pathPt array ...
###
            pathPt.insert(rowKt, list((round(float(row[6]), 4), round(float(row[3]), 8),
                                       round(float(row[4]), 8), round(float(row[5]), 2), round(float(row[7]), 4))))
            # print(rowKt,pathPt[rowKt])
            rowKt += 1  # incr array pointer
###
#                   add veh. speed. from Ref. Point till end of WZ to compute WZ Length...
###
            if (refPtIdx != 0):
                # add distance travel to wzLen
                wzLen = wzLen + float(row[6])/sampleFreq
                # end of input file = for loop


# totDataPt = len(list(pathPt))                               #total data points THIS VARIABLE IS NOT USED...

###
#   close the collected veh path data file
###
    csvFile.close()  # close the vehicle path data file

    atRefPoint[0] = refPtIdx
    atRefPoint[1] = int(wzLen)
    atRefPoint[2] = float(appHeading)
    atRefPoint[3] = maxHDOP

    ###print ("in Func...", atRefPoint)

    return
