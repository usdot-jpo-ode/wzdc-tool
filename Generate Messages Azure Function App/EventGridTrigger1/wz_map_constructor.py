#!/usr/bin/env python3
###
#   Python functions do the following:
#
#   A. getLanePt    - Parse the vehicle path data array mapPt(appMapPt array for approach lanes and wzMapPt array for WZ lanes) to
#                     generate node points for lane geometry using right triangle method
#
#   A.1 getEndPoint - Calculates lat/lon for the end points from origin lat/lon, distance and bearing
#   A.2 getDist     - Compute distance between two lat/lon points in meters
###
#
#   By J. Parikh / Dec., 2017
#   Initial Ver 1.0
#
###

###
#   Import math library for computation
###

import math
import logging


###
#   The following function computes lat and lon for a point distance "d" meters and bearing (heading)from an origin
#   with known lat1, lat2.
#
#   See https://www.movable-type.co.uk/scripts/latlong.html for more detail.
#
#   The function computes node point lat/lon for the adjacent lane's lane width (d) apart and 90 degree bearing
#   from the vehicle path data lane.
#
#   lat1    = Latitude of origin
#   lon1    = Longitude of origin
#   bearing = Destination direction in degree
#   dist    = Destination distance in km
###

def getEndPoint(lat1,lon1,bearing,d):
    R = 6371.0*1000              #Radius of the Earth in meters
    brng = math.radians(bearing) #convert degrees to radians
    dist = d                     #convert distance in meters
    lat1 = math.radians(lat1)    #Current lat point converted to radians
    lon1 = math.radians(lon1)    #Current long point converted to radians
    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return lat2,lon2

### ------------------------------------------------------------------------------------

###
#   Following function computes distance between two lat/lon points in meters...
#   Added on - 8-28-2017...
###

def getDist(origin, destination):
    lat1, lon1 = origin                     #lat/lon of origin
    lat2, lon2 = destination                #lat/lon of dest    
    radius = 6371.0*1000                    #meters

    dlat = math.radians(lat2-lat1)          #in radians
    dlon = math.radians(lon2-lon1)
    
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

def getChordLength(pt1, pt2):
    lat1 = math.radians(pt1[1])
    lon1 = math.radians(pt1[2])
    lat2 = math.radians(pt2[1])
    lon2 = math.radians(pt2[2])
    # lat1, lon1 = origin                     #lat/lon of origin
    # lat2, lon2 = destination                #lat/lon of dest    
    radius = 6371.0*1000                    #meters
    try:
        # This line very occasionally fails, out of range exception for math.acos
        d = radius*math.acos( math.cos(lat1)*math.cos(lat2)*math.cos(lon1-lon2) + math.sin(lat1)*math.sin(lat2) )
    except:
        dlat = lat2-lat1          #in radians
        dlon = lon2-lon1
        
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
    return d

### ------------------------------------------------------------------------------------


###
#   For Approach Lanes: starting from the ref. point go back upto 1st data point and construct map points for approach lane
#   For WZ lanes: starting from the ref. point process all points in pathPt array until the end
#
#   Equidistant Method: *** NOT USED *** -  Select data point for building the array by computing specified distance (for equidistance)
#                       between points for both approach and wz maps. This method does not work for map matching for curved lanes since the
#                       the data points may fall outside the map matching bounding box on curved lanes.
#
#   Rt. Triangle Method: *** IN USE *** - Points are selected based on change in heading angle which forms a rectangle triangle.
#                       A rt. angle triangle is formulated between two points. If the computed height is > half the lane width,
#                       the node point is selected for map node point and so on. This technique of selecting node point provides
#                       better map matching. 
#
###


###
#   laneType    1=Approach Lanes, 2=WZ Lanes
#   pathPt      Array containing vehicle path data points
#   mapPt       Constructed array of node points
#   laneWidth   from user input in meters
#   lanePad     lane padding in meterslaneStat
#   refPtIdx    location index in pathPt array for reference point
#   mapPtDist   distance between node point - used for generating node points based on equidistance method
#               not used in the algorithm any more, right triangle method is used
#   laneStat    array to indicate lane closed/open status different locations
#   wpStat      array to indicate workers present/not present statatus
#   dataLane    lane on which the vehicle was driven for collecting vehicle path data
###

def insertMapPt(mapPt, pathPt, elementPos, tLanes, laneWidth, dL, lcwpStat, distVec, laneTaperStat, currSpeedLimit):
    
    lla_ls_hwp  = [0]*((5*(tLanes))+4)                  #define llah list - 4 elements per node data point (lat,lon,alt,lo/lc)+heading+dist
                                                        #LO/LC (0/1), WP (0/1) status added on 11/13/2017

    bearingPP = pathPt[elementPos][4]            #bearing (heading) of the path point
    latPP     = pathPt[elementPos][1]            #lat/lon    
    lonPP     = pathPt[elementPos][2]
    altPP     = pathPt[elementPos][3]

###
#           now loop through all lanes as specified by the total number of lanes in the WZ for constructing node points for
#           adjacent lanes...
#
#           It is assumed that number of approach lanes are the same as WZ lanes.
###

    ln = 0
    while ln < tLanes:                      #loop through all lanes - Tot lanes are tLanes
        lW = abs(ln-dL)*laneWidth           #calculate next lane offset from the lane for which data is collected
        ##print (ln, lW)

        if ln == dL:                        #ln same as lane on which data was collected
            lla_ls_hwp[ln*5+0] = latPP      #lat, lon, alt, lcloStat for the lane
            lla_ls_hwp[ln*5+1] = lonPP
            lla_ls_hwp[ln*5+2] = altPP
            lla_ls_hwp[ln*5+3] = lcwpStat[ln]
            lla_ls_hwp[ln*5+4] = laneTaperStat[ln]
        pass

        if ln != dL:                        #Adjacent lanes only - not the data collected lane...
            if ln < dL:
                bearing = bearingPP - 90    #lane left to dataLane
            else:
                bearing = bearingPP + 90    #lane right to the dataLane
            pass

            ll = getEndPoint(latPP,lonPP,bearing,lW)    #get lat/lon for the point which is laneWidth apart from the data collected lane
            lla_ls_hwp[ln*5+0] = round(ll[0],8)         #computed lat of the adjacent lane...
            lla_ls_hwp[ln*5+1] = round(ll[1],8)         #computed lon of the adjacent lane   
            lla_ls_hwp[ln*5+2] = pathPt[elementPos][3]       #same altitude
            lla_ls_hwp[ln*5+3] = lcwpStat[ln]           #lc/lo Status of the lane at the node point                       
            lla_ls_hwp[ln*5+4] = laneTaperStat[ln]           #lc/lo Status of the lane at the node point                       
                                                        #end of if lineType
        pass                                                #end of if ln!= dL   
###
#            
#           Add current heading (bearing) in the last column for use in 
#           drawing rectangular bounding polygon on Google map in javaScript application for visualization...
#
#           Added: distance of selected nodepoint from previous node for future use...
#                  May 21, 2018
#
#           Note:   Old method was calculating "dist" as distance traversed by the vehicle.
#                   New method computes "distVec" as distance vector (produces very minor difference...)
#
###
        if ln == tLanes - 1:                        #if the current ln same as the last lane
            lla_ls_hwp[ln*5+5] = bearingPP          #add heading in the table
            lla_ls_hwp[ln*5+6] = lcwpStat[tLanes]   #add WP Status for the node in the table
            lla_ls_hwp[ln*5+7] = int(distVec)       #add computed distVec, distance in meters from prev. node point in the table for future use
            lla_ls_hwp[ln*5+8] = currSpeedLimit     #add current speed limit in mph
            ##print ("bearingPP: ", refPt, bearingPP)
        pass                                        #end of if ln
                
        ln = ln + 1                                 #next lane
    pass                                            #end of while loop

###
#           Store computed lat,lon,alt,lcloStat, for each node for each lane + last two elements in table heading and WP flag + distVec (dist from prev. node)
###
    print(list(lla_ls_hwp))
    mapPt.append(list(lla_ls_hwp))               #insert constructed lla_ls_hwp list for each node for each lane in mapPt array

def getLanePt(laneType,pathPt,mapPt,laneWidth,lanePad,refPtIdx,mapPtDist,laneStat,wpStat,dataLane,wzMapLen,speedList,dataFreq):

    
###
#   Total number of lanes are in loc [0][0] in laneStat array
###
    if len(pathPt) <= 3:
        logging.error("Work zone is too short")
        return None

    totDataPt = (len(list(pathPt)))                     #total data points (till end of array)
    tLanes  = laneStat[0][0]                            #total number of lanes...

    lcwpStat    = [0]*(tLanes+1)                        #Temporary list to store status of each node for each lane + WP state for the node
    laneTaperStat = [0]*(tLanes)                        #0 = no taper, 1 = taper-right, 2 = taper-left, 3=none, 4=either
    dL      = dataLane - 1                              #set lane number starting 0 as the left most lane                             
    distVec = 0
    stopIndex = 0
    startIndex = 0
    actualError = 0
    distFromLC = 0
    incrDistLC = False
    taperLength = speedList[0]*(laneWidth + lanePad)*3.28084
    currSpeedLimit = speedList[1]

    if speedList[0] <= 40:
        taperLength = ((laneWidth + lanePad)*3.28084*(speedList[0]**2)) / 60

    ALLOWABLEERROR = 1
    SMALLDELTAPHI = 0.01
    CHORDLENGTHTHRESHOLD = 500
    MAXESTIMATEDRADIUS = 8388607 #7FFFFF
    if laneType == 1:
        if refPtIdx < 3:
            for i in range(0, refPtIdx):
                insertMapPt(mapPt, pathPt, i, tLanes, laneWidth, dL, lcwpStat, distVec, laneTaperStat, currSpeedLimit)
                distVec += pathPt[i][0]/dataFreq
                # Rework to use actualChordLength
                return
        else:
            stopIndex = refPtIdx
    else:
        stopIndex = totDataPt
        startIndex = refPtIdx

    # Step 1
    i = startIndex + 2
    Pstarting = pathPt[i-2]
    Pprevious = pathPt[i-1]
    Pnext = pathPt[i]
    totalDist = 0
    incrementDist = 0
    taperingLane = 0
    insertMapPt(mapPt, pathPt, i-2, tLanes, laneWidth, dL, lcwpStat, distVec, laneTaperStat, currSpeedLimit)

    while i < stopIndex:
    # Step A
        requiredNode  = False                                 #set to False
        if laneType == 2:                                   #WZ Lane
            for lnStat in range(1, len(laneStat)):          #total number of lc/lo/wp are length of laneStat-1
                if laneStat[lnStat][0] == i-1:            #got LC/LO location
                    ln = laneStat[lnStat][1]-1
                    requiredNode = True                       #set to True
                    if incrDistLC: #other lane taper active, end other lane closure
                        laneTaperStat[taperingLane] = 0
                    incrDistLC = True
                    distFromLC = 0
                    taperingLane = ln
                    lcwpStat[taperingLane] = laneStat[lnStat][2]       #get value from laneStat 
                    laneTaperVal = 3
                    if tLanes != 1:
                        if lcwpStat[ln] == 1: #Lane closure
                            if ln == 0 and lcwpStat[1] == 0: #Left lane, lane to right open
                                laneTaperVal = 1
                            elif ln == tLanes - 1 and lcwpStat[tLanes - 2] == 0: #Right lane, lane to left open
                                laneTaperVal = 2
                            elif ln != 0 and ln != tLanes - 1:
                                leftLaneOpen = False
                                if lcwpStat[ln-1] == 0: leftLaneOpen = True
                                rightLaneOpen = False
                                if lcwpStat[ln+1] == 0: rightLaneOpen = True

                                if rightLaneOpen and leftLaneOpen: laneTaperVal = 4
                                elif leftLaneOpen: laneTaperVal = 2
                                elif rightLaneOpen: laneTaperVal = 1
                        else:
                            if ln == 0 and lcwpStat[1] == 0: #Left lane, lane to right open
                                laneTaperVal = 2
                            elif ln == tLanes - 1 and lcwpStat[tLanes - 2] == 0: #Right lane, lane to left open
                                laneTaperVal = 1
                            elif ln != 0 and ln != tLanes - 1:
                                leftLaneOpen = False
                                if lcwpStat[ln-1] == 0: leftLaneOpen = True
                                rightLaneOpen = False
                                if lcwpStat[ln+1] == 0: rightLaneOpen = True

                                if rightLaneOpen and leftLaneOpen: laneTaperVal = 4
                                elif leftLaneOpen: laneTaperVal = 1
                                elif rightLaneOpen: laneTaperVal = 2
                    laneTaperStat[taperingLane] = laneTaperVal

                    #laneTaperStat[laneStat[lnStat][1]-1] = 1       #get value from laneStat 
                elif distFromLC >= taperLength:
                    requiredNode = True                       #set to True
                    incrDistLC = False
                    distFromLC = 0
                    laneTaperStat[taperingLane] = 0       #get value from laneStat 
                pass
            pass

            for wpZone in range(0, len(wpStat)):
                if wpStat[wpZone][0] == i-1:                      #got WP Zone True/False
                    requiredNode = True                               #set to True 
                    lcwpStat[tLanes] = wpStat[wpZone][1]   #update WP Zone status
                    if wpStat[wpZone][1] == 1:
                        currSpeedLimit = speedList[2]
                    else:
                        currSpeedLimit = speedList[1]
                pass
            pass
        pass

    # Step 2
        eval = True
        actualChordLength = getChordLength(Pstarting, Pnext)
        if actualChordLength > CHORDLENGTHTHRESHOLD:
            actualError = ALLOWABLEERROR + 1
            eval = False
            # Go to step 7

    # Step 3
        deltaHeadings = abs(Pnext[4] - Pstarting[4])
        if deltaHeadings > 180: deltaHeadings = 360 - deltaHeadings
        deltaHeadings = abs(math.radians(deltaHeadings))

    # Step 4
        if deltaHeadings < SMALLDELTAPHI and eval:
            actualError = 0
            estimatedRadius = MAXESTIMATEDRADIUS
            eval = False
            # Go to step 8
        elif eval:
            estimatedRadius = actualChordLength/(2*math.sin(deltaHeadings/2))

    # Step 5
        d = estimatedRadius*math.cos(deltaHeadings/2)

    # Step 6
        if eval: #Allow step 4 to maintain 0 actualError
            actualError = estimatedRadius - d

    # Step 7
        if actualError > ALLOWABLEERROR or requiredNode:
            incrementDist = actualChordLength
            totalDist += incrementDist
            insertMapPt(mapPt, pathPt, i-1, tLanes, laneWidth, dL, lcwpStat, totalDist, laneTaperStat, currSpeedLimit)

            Pstarting = pathPt[i-1]
            Pprevious = pathPt[i]
            if i != stopIndex-1:
                Pnext = pathPt[i+1]
            i += 1
    # Step 8
        else:
            if i != stopIndex-1:
                Pnext = pathPt[i+1]
            Pprevious = pathPt[i]
            i += 1

        if i == stopIndex:
            incrementDist = actualChordLength
            totalDist += incrementDist
            insertMapPt(mapPt, pathPt, i-1, tLanes, laneWidth, dL, lcwpStat, totalDist, laneTaperStat, currSpeedLimit)

        if incrDistLC:
            distFromLC += (pathPt[i - 1][0] * 3.28084)/dataFreq
    # Step 9
        # Integrated into step 7
        
    if laneType == 1:
        wzMapLen[0] = totalDist
    else:
        wzMapLen[1] = totalDist