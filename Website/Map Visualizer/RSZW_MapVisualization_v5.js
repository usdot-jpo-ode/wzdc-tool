//
//           ************************ R S Z W / L C ****************************
//           
//           JavaScript functions uses Google map to:
//                        1.           Overlay vehicle path data collected for constructing waypoints (node points) representing all 
//                                      approach and work zone lanes 
//                        2.  Overlay constructed approach and work zone lanes waypoints using different icons
//                        3.           Draw filled rectangular bounding box between each waypoint (node) segment
//                        4.           Replay collected data including test vehicle movement from the tes.
//
//
//           Data arrays used by different function are created in pyhton from vehicle path data 
//
//           Developed by J. Parikh @ CAMP for the V2I Safety Application Project(CAMP)
//           
//           Initial version - August 2017                     Version 1.0
//           Revised data structure - Sept. 2017              Version 1.1
//           Revised version - November 25, 2017 Version 1.2
//
//
//
//****   GLOBAL VARIABLES included from *.js file generated in python from processing vehicle path data...   ****
//
//                        Following global variables are included by *.js file generated in python...
//
//               refPoint                                     [lat,lon,elev]
//               noLanes
//                        mappedLaneNo
//                        laneStat                                         list of lane status to indicate lane open/close with array index pointing to mapData array 
//                                                                                             [idx,lane #, 0/1, offset in meters from ref. pt]...
//                        wpStat                                           list of workers present status to indicate workers present zone with array index pointing 
//                                                                                             to mapData array [idx,0/1, offset in meters from ref. pt]...
//                        laneWidth                                     in meters
//                        mapData                                                     vehicle path data [speed,lat,lon,elev,vehicle heading]
//                        appMapData                                 array of constructed waypoints for each approach lane [lat,lon,elev,0/1]... + heading,WP flag
//                        wzMapData                                   array of constructed waypoints for each work zone lane [lat,lon,elev,0/1]... + heading,WP flag
//
//*******************************
//           
//****   GLOBAL VARIABLES   ****
//
//****   
//                        Canvas and Google map options... 
//****

var rszwMap;                                                                                                                                               //Map object
var myMapOptions;                                                                                                                                    //map options

//
//                        WZ Map Overlay flag..
//

//****                
//                        Variables are used for replaying test data and to animate vehicle movement
//**** 
var myPrevPos, prevPosMarker, currPosMarker;                            //previous position and marker                                                                                    
var prevVehIdx;                                                                                                                                         //Veh heading index    
var carMarker = [];                                                                                                                                      //Array of car icon objects
//****
//                        Variables to hold description of each data point and dot icon for conducted 
//                        application test data for display using clickable infoWindow
//
//                        Following testData array is no longer used for WZ Map Display...
//
//                                                    REMOVED FROM THIS SOURCE...
//
//****
//           var testDataDesc = new Array(testData.length);                              //each data point display string
//           var testDataIcon = new Array(testData.length);                              //dot array for each data point

//****
//                        Variables to hold description of each data points for approach and WZ lanes waypoints (nodes)
//****                
var mapDataDesc = new Array();                                                                                                //description for displayed dot for collected map data
var appDataDesc = new Array();                                                                                   //description for displayed dot for constructed approach lane map data
var wzDataDesc = new Array();                                                                                     //description for displayed dot for constructed approach lane map data                    
var lnDataDesc = new Array();                                                                                       //description for displayed icon for lane status marked in veh path data

//****
//                        Variables to indicate start and end of test data markers
//                        Global variable i must be used with care. Must be reset prior to using it.
//**** 
var i, dataStart, dataEnd;

//****
//                        Function to initialize 
//                        1. collected vehicle path data
//                        2. constructed waypoints for approach lane(s)
//                        3. constructed waypoints for WZ lane(s) including lane closure(s)
//                        
//                        for display using clickable infoWindow
//****

function initDisplayWZMap()                                                                                                                    //Function to initialize map and waypoint(node) data points 
{
    //****
    //                                  Collected vehicle path data...
    //****                                        
    var vSspeed, vSpeedMPH;                                                                                                                      //local temp variables 
    var fontSize = "<font size=\"2\">";                                                                            //set small font size for infoWindow display

    for (i = 0; i < mapData.length; i++) {
        vSpeed = String(mapData[i][0].toFixed(1)) + " m/s";
        vSpeedMPH = " (" + String((mapData[i][0] * 2.23694).toFixed(1)) + " mph)";
        mapDataDesc[i] = fontSize + "<b>Data Point#: </b>" + String(i) + ";<b> Veh Speed: </b>" + vSpeed + vSpeedMPH + ";<b> Lat/Lon/Elev: </b>" + String(mapData[i][1]) + ", " + String(mapData[i][2]) + ", ";
        mapDataDesc[i] = mapDataDesc[i] + String(mapData[i][3].toFixed(0)) + ";<b> Heading: </b>" + String(mapData[i][4].toFixed(2));
    }
    //****
    //                                  Constructed waypoints data for each approach lane...
    //****
    i = 0;
    for (ln = 0; ln < noLanes; ln++)                                                                     //lanewise desc and icon array construction...
    {
        for (ap = 0; ap < appMapData.length; ap++) {
            appLLE = String(appMapData[ap][ln * 5 + 0]) + ", " + String(appMapData[ap][ln * 5 + 1]) + ", " + String(appMapData[ap][ln * 5 + 2]);
            appLLE = ";<b> Lat/Lon/Elev: </b>" + appLLE;
            appDataDesc[i] = fontSize + "<b>Lane/Node: </b>" + String(ln + 1) + "/" + String(ap + 1) + appLLE;
            i++;
        }
    }
    //****
    //                                  Constructed waypoints data for each WZ lane...
    //****                                        
    i = 0;
    for (ln = 0; ln < noLanes; ln++)                                                                     //lanewise description and icon array construction...
    {
        for (wz = 0; wz < wzMapData.length; wz++)                             //for each lane, do all wz map waypoints          
        {
            //
            //                                                                    Construct lcStat description string...
            //
            lcStat = ", LO";                                                                                                                                                                                                     //Lane open at this node       
            if (wzMapData[wz][ln * 5 + 3] == 1) { lcStat = ", LC"; }                                                            //Lane closed at this node
            if (wzMapData[wz][noLanes * 5 + 1] == 1) { lcStat = lcStat + "+WP"; }                                         //Workers present at this node
            //                           lcStat = "<b>"+lcStat+": </b>"
            lcStat = "<b>" + "Lane/Node: </b>" + String(ln + 1) + "/" + String(wz + 1) + lcStat;
            //
            //                                                                    Construct node's Lat,Lon,Elev description string...
            //                                        
            wzLLE = String(wzMapData[wz][ln * 5 + 0]) + ", " + String(wzMapData[wz][ln * 5 + 1]) + ", " + String(wzMapData[wz][ln * 5 + 2]);
            wzLLE = ";<b> Lat/Lon/Elev: </b>" + wzLLE;
            wzDataDesc[i] = fontSize + lcStat + wzLLE;
            i++;
        }
    }
}                                                                                 //end of function initDiaplayWZMap

//                        
//**       initialize the display string and associated dot icons for each of the test data point from
//                        running the RSZW/LC application
//
//**       initDiaplayWZTest Function is NOT USED in this WZ Map Visualization...
//**                                  REMOVED FROM THIS SOURCE...
//**
//
////       -----------------------------------------------------------------------------------------------                         
//
//                        Alternate function to construct infowindow for clickable data point description...              
//
//**       Following Function is NOT USED for WZ Visualization...
//                        

function showMapTestDotInfo(dotPos, dotIcon, dotDesc) {
    var infoWindow = new google.maps.InfoWindow();
    dotMarker = new google.maps.Marker(
        {
            position: dotPos,
            map: rszwMap,
            icon: dotIcon
        }
    );
    //
    //                                  Set Listener for information window. Onclick pop-up display string
    //
    google.maps.event.addListener(dotMarker, 'click', (function (dotMarker) {
        return function () {
            infoWindow.setContent(dotDesc);
            infoWindow.open(rszwMap, dotMarker);
        }
    })
        (dotMarker));
}


//******
//                        Following function can be used to display text on a canvas...
//
//                        ***** NOT USED ***** in this program; Alternate method is used...                                                                                                      
//
//******

function showWZInfo() {
    var wzInfo = document.getElementById("wzInfo_canvas");
    var infoContext = wzInfo.getContext("2d");
    var nodesPerLane = [0, 0];

    nodesPerLane = [msgSegList[1][2], msgSegList[msgSegList.length - 1][2]];

    infoContext.clearRect(0, 0, 1200, 500);

    infoContext.fillStyle = 'royalblue';
    infoContext.font = '12px sans-serif';
    infoContext.textBaseline = 'bottom';
    yPos = 3;
    infoContext.fillText("Work Zone: " + wzDesc, 10, yPos + 15);
    infoContext.fillText("Map Created: " + wzMapDate, 10, yPos + 30);
    infoContext.fillText("WZ Ref. Point at: " + String(refPoint[0]), 10, yPos + 45);
    infoContext.fillText("# of Lanes in WZ: " + String(noLanes), 10, yPos + 60);
    infoContext.fillText("Vehicle path data lane: " + String(mappedLaneNo), 10, yPos + 75);
    infoContext.fillText("Mapped nodes per Approach / WZ lanes: " + String(nodesPerLane[0]) + " / " + String(nodesPerLane[1]), 10, yPos + 90);

    var legendImg = new Image();
    legendImg.onload = function () {
        //   infoContext.drawImage(legendImg, 600,3);
    }
}

//***************************************************
//                        On load from the html file, start here...
//***************************************************

var activeMarkers = false
var activeType = ''
var startCircle;
var endCircle;

var pathPoints = []
var startEndMarkers = []
var newIDs = []
var pathToIndex = []
var markerLocations = {}
var currentMarkers = []
var validRowMappings = {}
var googleMarkers = []
var startPointIcon = 'Icons\\pathStartPoint.png';
var endPointIcon = 'Icons\\pathEndPoint.png';
var startMarkerIcon = 'Icons\\startDataLogPoint.png';
var endMarkerIcon = 'Icons\\endDataLogPoint.png';
var refPointIcon = 'Icons\\refPoint3white.png';                              //ref point icon
var mapDataPtIcon = 'Icons\\vehPath2.png';                                                 //vehicle path data point icon
var approachPtIcon = 'Icons\\approachPoint.png';                                                       //vehicle path data point icon

var laneOpenIcon = ['Icons\\lane1OpenPoint.png', 'Icons\\lane2OpenPoint.png',
    'Icons\\lane3OpenPoint.png', 'Icons\\lane4OpenPoint.png',
    'Icons\\lane5OpenPoint.png', 'Icons\\lane6OpenPoint.png',
    'Icons\\lane7OpenPoint.png', 'Icons\\lane8OpenPoint.png'];

var laneClosedIcon = ['Icons\\lane1ClosedPointO.png', 'Icons\\lane2ClosedPointO.png',
    'Icons\\lane3ClosedPointO.png', 'Icons\\lane4ClosedPointO.png',
    'Icons\\lane5ClosedPointO.png', 'Icons\\lane6ClosedPointO.png',
    'Icons\\lane7ClosedPointO.png', 'Icons\\lane8ClosedPointO.png'];

var rpID = ''

var wpPointIcon = ['Icons\\wnpPoint.png', 'Icons\\wpPointO.png'];

//iconsDict = {
//    'Icons\\refPoint3Green.png': 'RP',
//    'Icons\\lane1OpenPoint.png': 'LO,1',
//    'Icons\\lane2OpenPoint.png': 'LO,2',
//    'Icons\\lane3OpenPoint.png': 'LO,3',
//    'Icons\\lane4OpenPoint.png': 'LO,4',
//    'Icons\\lane5OpenPoint.png': 'LO,5',
//    'Icons\\lane6OpenPoint.png': 'LO,6',
//    'Icons\\lane7OpenPoint.png': 'LO,7',
//    'Icons\\lane8OpenPoint.png': 'LO,8',
//    'Icons\\lane1ClosedPointO.png': 'LC,1',
//    'Icons\\lane2ClosedPointO.png': 'LC,2',
//    'Icons\\lane3ClosedPointO.png': 'LC,3',
//    'Icons\\lane4ClosedPointO.png': 'LC,4',
//    'Icons\\lane5ClosedPointO.png': 'LC,5',
//    'Icons\\lane6ClosedPointO.png': 'LC,6',
//    'Icons\\lane7ClosedPointO.png': 'LC,7',
//    'Icons\\lane8ClosedPointO.png': 'LC,8',
//}
function startHere() {

    //if (typeof mapData === 'undefined')
    //    return

    //
    //                                  Built display dot icon and display string for each data point for Map and Test Data...
    //                                  
    initDisplayWZMap();                                                                                                                                            //Map data points
    //**                initDisplayWZTest();  *** NOT NEEDED FOR WZ VISUALIZATION, FUNCTION REMOVED FROM THIS SOURCE ***         //Test data points                 

    i = dataStart;                                                                                                                                                         //start at first non-zero vehicle speed                                                            

    //*******************************************************************************                                                                     
    //                                  Start displaying stuff...                 
    //                                  Setup google map parameters... 
    //*******************************************************************************
    
    var myMapOptions =                                                                                                                                                                                                  //gMap options...                                       
    {
        zoom: 15,                                                                                                                                                                                                   //Works only if fitBounds below is commented out...
        center: new google.maps.LatLng(refPoint[1], refPoint[2]),                                  //Reference Point...
        // center: new google.maps.LatLng(mapData[0][1], mapData[0][2]),              //First map data point
        mapTypeId: google.maps.MapTypeId.HYBRID,                                                                                                //Satellite + Street names
        mapTypeControl: true,
        zoomControl: true,
        scaleControl: true,
        streetViewControl: true,
        rotateControl: true,
        fullscreenControl: true
    };

    rszwMap = new google.maps.Map(document.getElementById("map_canvas"), myMapOptions);
    rszwMap.setTilt(0);                                                                                                                                //set map tilt to 0 or 45 degrees

    var controlDiv = document.getElementById('mapControlsDiv');
    rszwMap.controls[google.maps.ControlPosition.TOP_CENTER].push(controlDiv);

    var startPoint = new google.maps.LatLng(wzMapData[0][0], wzMapData[0][1]);
    var endPoint = new google.maps.LatLng(wzMapData[wzMapData.length - 1][0], wzMapData[wzMapData.length - 1][1]);
    //var heading = google.maps.geometry.spherical.computeHeading(startPoint, endPoint);
    //rszwMap.setHeading(100); Doesn't work

    //****
    //                                  Local variables for ref point and other icons
    //****                          

    //****                                        
    //                                  place collected vehicle path data points with purple dots on google map... 
    //                                  Call function to associate clickable info.window for each data point...
    //****                                        
    dataLogIDs = [uuidv4(), uuidv4()];
    markerIDs = [uuidv4(), uuidv4()];
    for (md = 0; md < mapDataDesc.length; md++) {
        dotLoc = new google.maps.LatLng(mapData[md][1], mapData[md][2]);
        pathPoints.push(dotLoc);
        pathToIndex.push([dotLoc, md]);
        

        if (md == 0) {
            title = new Title('Data Log', 'True', dataLogIDs[0], dataLogIDs[1]);
            markerLocations[title.ID] = md
            showDotInfo(dotLoc, startPointIcon, "<b><font color='green'>Start of Work Zone</font></b>", title.toString());

            //startLoc = new google.maps.LatLng(startMarkerLoc[0], startMarkerLoc[1]);
            //startCircle = new google.maps.Circle({
            //    strokeColor: '#00FF00',
            //    strokeOpacity: 0.8,
            //    strokeWeight: 2,
            //    fillOpacity: 0,
            //    map: rszwMap,
            //    center: startLoc,
            //    radius: 50
            //});

            //title = new Title('Start Point', '', markerIDs[0], markerIDs[1]);
            //markerLocations[title.ID] = find_index_closest_point(startLoc, pathPoints)
            //showDotInfo(startLoc, startMarkerIcon, "<b><font color='green'>Start of Work Zone</font></b>", title.toString());
            //fillColor: '#00FF00',
            //    fillOpacity: 0.35,
        }
        else if (md == mapDataDesc.length - 1) {
            title = new Title('Data Log', 'False', dataLogIDs[1], dataLogIDs[0]);
            markerLocations[title.ID] = md
            showDotInfo(dotLoc, endPointIcon, "<b><font color='red'>End of Work Zone</font></b>", title.toString());

            //endLoc = new google.maps.LatLng(endMarkerLoc[0], endMarkerLoc[1]);
            //endCircle = new google.maps.Circle({
            //    strokeColor: '#FF0000',
            //    strokeOpacity: 0.8,
            //    strokeWeight: 2,
            //    fillOpacity: 0,
            //    map: rszwMap,
            //    center: endLoc,
            //    radius: 50
            //});
            //title = new Title('End Point', '', markerIDs[1], markerIDs[0]);
            //markerLocations[title.ID] = find_index_closest_point(endLoc, pathPoints)
            //showDotInfo(endLoc, endMarkerIcon, "<b><font color='red'>End of Work Zone</font></b>", title.toString());
        }
        else {
            title = new Title('Data Point', '', uuidv4(), '');
            showDotInfo(dotLoc, mapDataPtIcon, mapDataDesc[md], title.toString());         //function to show placed dot icon and associated description
        }
        //                 md = md + 2;                                                                                                                                //skip points for display 
    }

    //****
    //                                  Place the reference point on map, associate current data point,lat,lon,elev for infoWindow
    //****                          
    var refPointDesc = "<b>Ref. Pt. @ Data Pt.: </b>" + String(refPoint[0]) + ",<b> Lat/Lon/Elev: </b>" + String(refPoint[1]) + ", " + String(refPoint[2]) + ", " + String(refPoint[3]);
    var refPointLoc = new google.maps.LatLng(refPoint[1], refPoint[2]);              //Show reference point, slightly offset   + 0.000005

    title = new Title('RP', '', uuidv4(), '');
    rpID = title.ID;
    markerLocations[title.ID] = refPoint[0]
    showDotInfo(refPointLoc, refPointIcon, refPointDesc, title.toString());                  //show reference point with description

    rszwMap.setCenter(refPointLoc);                                                                                            //Center map to reference point                        

    //********************************************************************
    //                                  Start displaying WZ parameters, lane and workers presence status stuff...                           
    //                                  Build txt string with html tags to display WZ information Msg + Legends 
    //********************************************************************                                         

    var nodesPerLane = [0, 0];
    var txt = "";

    nodesPerLane = [msgSegList[1][2], msgSegList[msgSegList.length - 1][2]];
    //
    //                    Build the complete text string describing WZ parameters...
    //                    Complete text is displayed later after building lane status and workers presence status...
    //                                  
    txt = "<center><b><font size='3'>Mapped Work Zone</b></font></br></center>";
    txt = txt + "<Center><b><font color='blue'>" + wzDesc + "</b></font><hr></center>";
    txt = txt + "Map Created: <b>" + wzMapDate + "</b></br>";

    //                                  WZ length - in the RSZW_MAP_jsData.js data file for map generated prior to Jan. 2019
    //                                                does not have wzLength variable. To avoid error following is added... Jan. 10, 2019
    //                                                                                        
    if (typeof wzLength !== "undefined") {
        txt = txt + "Mapped WZ Length (meters):</br>";
        txt = txt + "&nbsp;&nbsp;App: <b>" + String(wzLength[0]) + "</b> + WZ: <b>" + String(wzLength[1]) + "</b> = <b>"
            + String(wzLength[0] + wzLength[1]) + "</b></br>";
    }

    txt = txt + "Start of WZ @ Data Point: <b>" + String(refPoint[0]) + ";</b></br> &nbsp;&nbsp;@ Lat/Lon: <b>"
        + String(refPoint[1]) + ", " + String(refPoint[2]) + "</b></br>";
    txt = txt + "# of Lanes in WZ: <b>" + String(noLanes) + "</b></br>";
    txt = txt + "Vehicle Path Data Lane: <b>" + String(mappedLaneNo) + "</b></br>";
    txt = txt + "Nodes Per Approach/WZ Lanes: <b>" + String(nodesPerLane[0]) + "/" + String(nodesPerLane[1]) + "</b></br>";
    txt = txt + "<hr><b><center>Start/End of Lane Closures</b></center>";

    //****
    //                                  Overlay lane status (close/open) marked during vehicle path data collection...
    //****
    var laneIDs = new Array(9)

    for (ls = 1; ls < laneStat.length; ls++) {
        dataPtIndex = laneStat[ls][0];

        if (laneStat[ls][2] == 1) {
            laneIDPair = [uuidv4(), uuidv4()];
            laneIDs[laneStat[ls][1]] = laneIDPair;
            laneID = laneIDPair[0];
        }

        if (laneStat[ls][2] == 0) {
            laneIDPair = laneIDs[laneStat[ls][1]];
            laneID = laneIDPair[1];
        }

        [description, titleString, txtLaneEvent, lsIcon] = createLaneContent(laneStat[ls][2], laneStat[ls][1], laneIDPair, dataPtIndex)

        txt = txt + txtLaneEvent;

        //
        //                                            Place the lane status icon w/ description... 
        //
        dotLoc = new google.maps.LatLng(mapData[dataPtIndex + 0][1], mapData[dataPtIndex + 0][2]);
        showDotInfo(dotLoc, lsIcon, description, titleString);                                                               //function to show placed dot icon and associated description                                                                                                                  
        //
        //                                            Add horizontal line...
        //                                                                                                   
        txt = txt + "</br>";
    }

    //**********
    //                                  Overlay workers present zone status (start/end) marked during vehicle path data collection...
    //**********                            

    txt = txt + "<hr><b><center>Start/End of Workers Presence</b></center>";                                        //WP/WnP text for display...

    wpIDs = []
    for (wp = 0; wp < wpStat.length; wp++) {
        dataPtIndex = wpStat[wp][0];

        if (wpStat[wp][1] == 1) {
            wpIDs = [uuidv4(), uuidv4()]
        }

        [description, titleString, txtUpdated, wpIcon] = createWorkerContent(wpStat[wp][1], wpIDs, dataPtIndex)

        txt = txt + txtUpdated;

        dotLoc = new google.maps.LatLng(mapData[dataPtIndex + 0][1], mapData[dataPtIndex + 0][2]);
        showDotInfo(dotLoc, wpIcon, description, titleString);                                    //function to show placed dot icon and assocaited description
    }
    //
    //                                  Add horizontal line...
    //                    
    txt = txt + "<hr>";
    //
    //                                  Display completed text...
    //

    // txt = txt + "<button id='displayMapNodesBtn' class='overlay_btn' onclick='displayMapNodes_drawRectBB(); return false;'>Overlay WZ Map</button>";

    txt = txt + "</br><p>";
    txt = txt + "<img src = './Icons/visualization_legend.png' class='wzLegends'>";
    //                    
    //                    The following is a fancy way to show larger legend image using onmouseover and onmouseout...
    //                    ... NOT USED... It does not pop-up on the map, but works great on wzInfo_text section
    ///                                 

    ////                 txt = txt + "<img onmouseover='bigLegend(this)' onmouseout='smallLegend(this)' border='0'                      \
    ////                                                   src='./Icons/Legends-RSZW5.png' alt='Legends' width='128' style='left:50px'>";

    document.getElementById('wzInfo_text').innerHTML = txt;
    getCurrentMarkers()
    displayMapNodes_drawRectBB()
}

function createLaneContent(laneStat, lane, laneIDPair, dataPtIndex) {
    // Returns [Marker Description, Marker Title, txt info]
    if (laneStat == 1) {
        id = 1
        idp = 0
        laneStatMarker = 'LC'
        lsIcon = laneClosedIcon[lane - 1];

        txt = "<font color='red'>&emsp;Start of Lane #" + String(lane) + " Closure @: " + String(dataPtIndex) + "</font>";
    }
    else if (laneStat == 0) {
        id = 0
        idp = 1
        laneStatMarker = 'LO'
        lsIcon = laneOpenIcon[lane - 1];

        txt = "<font color='green'>&emsp;End of Lane #" + String(lane) + " Closure @: " + String(dataPtIndex) + "</font></br>";
    }

    title = new Title(laneStatMarker, lane.toString(), laneIDPair[id], laneIDPair[idp])

    description = createMarkerDesc(title, dataPtIndex)

    titleString = title.toString()
    // title = [laneStatMarker, laneStat.toString(), laneIDPair[id], laneIDPair[idp]].join(',');

    markerLocations[title.ID] = dataPtIndex
    return [description, titleString, txt, lsIcon]
}

function createWorkerContent(wpStat, wpIDs, dataPtIndex) {
    // Returns [Marker Description, Marker Title, txt info]
    var title;
    if (wpStat == 1) {
        title = new Title('WP', 'True', wpIDs[0], wpIDs[1]);

        wStat = "<font color='red'>Start of Workers Presence";
        wpIcon = wpPointIcon[wpStat];
        txt = "<font color='red'>&emsp;&emsp;Start @: " + String(dataPtIndex) + "</font>";                                       //Text for Start of WP
    }
    else if (wpStat == 0) {
        title = new Title('WP', 'False', wpIDs[1], wpIDs[0]);

        wStat = "<font color='green'>End of Workers Presence";
        wpIcon = wpPointIcon[wpStat];

        txt = "<font color='green'>&emsp;&emsp; End @: " + String(dataPtIndex) + "</font></br>";              //Text for End of WP
    }

    description = createMarkerDesc(title, dataPtIndex)

    titleString = title.toString()
    // title = [laneStatMarker, laneStat.toString(), laneIDPair[id], laneIDPair[idp]].join(',');

    markerLocations[title.ID] = dataPtIndex
    return [description, titleString, txt, wpIcon]
}

function createAddMarkerText(marker, value) {
    if (marker == 'LC') {
        text = 'Click To Add <b>Start Of Lane ' + value + ' Closure</b> Marker'
    }
    else if (marker == 'LO') {
        text = 'Click To Add <b>End Of Lane ' + value + ' Closure</b> Marker'
    }
    else { // WP
        if (value == 'True') {
            text = 'Click To Add <b>Start Of Workers Present</b> Marker'
        }
        else {
            text = 'Click To Add <b>End Of Workers Present</b> Marker'
        }
    }
    return text
}

function updateOverlayText(type, order) {
    if (type == 'Lane') {
        if (order == 'Start') {
            text = createAddMarkerText('LO', '1');
            $('#mapBtnsOverlay').html(text)
        }
        else if (order == 'End') {
            $('#mapBtnsOverlay').hide()
        }
        else {
            text = createAddMarkerText('LC', '1');
            $('#mapBtnsOverlay').html(text)
            $('#mapBtnsOverlay').show()
        }
    }
    else if (type == 'WP') {
        if (order == 'Start') {
            text = createAddMarkerText('WP', 'False');
            $('#mapBtnsOverlay').html(text)
        }
        else if (order == 'End') {
            $('#mapBtnsOverlay').hide()
        }
        else {
            text = createAddMarkerText('WP', 'True');
            $('#mapBtnsOverlay').html(text)
            $('#mapBtnsOverlay').show()
        }
    }
}

function add_lane_closure() {
    setMapOnClickListeners('Lane')

    //dataPtIndex = laneStat[ls][0];

    //if (laneStat[ls][2] == 1) {
    //    laneIDPair = [uuidv4(), uuidv4()];
    //    laneIDs[laneStat[ls][1]] = laneIDPair;
    //    laneID = laneIDPair[0];
    //}

    //if (laneStat[ls][2] == 0) {
    //    laneIDPair = laneIDs[laneStat[ls][1]];
    //    laneID = laneIDPair[1];
    //}

    //[description, titleString, txtLaneEvent, lsIcon] = createLaneContent(laneStat[ls][2], laneStat[ls][1], laneIDPair, dataPtIndex)

    //txt = txt + txtLaneEvent;

    ////
    ////                                            Place the lane status icon w/ description... 
    ////
    //markerLocations[laneID] = dataPtIndex
    //dotLoc = new google.maps.LatLng(mapData[dataPtIndex + 0][1], mapData[dataPtIndex + 0][2]);
    //showDotInfo(dotLoc, lsIcon, description, titleString);                                                               //function to show placed dot icon and associated description                                                                                                                  
    ////
    ////                                            Add horizontal line...
    ////                                                                                                   
    //txt = txt + "</br>";
}

function add_work_presence() {
    setMapOnClickListeners('WP')

    //wpIDs = [uuidv4(), uuidv4()]

    //// First Marker
    //dataPtIndex = 23;

    //[description, titleString, txtUpdated, wpIcon] = createWorkerContent(wpStat[wp][1], wpIDs, dataPtIndex)

    //dotLoc = new google.maps.LatLng(mapData[dataPtIndex + 0][1], mapData[dataPtIndex + 0][2]);
    //showDotInfo(dotLoc, wpIcon, description, titleString);

    //// Second Marker
    //dataPtIndex = 23;

    //[description, titleString, txtUpdated, wpIcon] = createWorkerContent(wpStat[wp][1], wpIDs, dataPtIndex)

    //dotLoc = new google.maps.LatLng(mapData[dataPtIndex + 0][1], mapData[dataPtIndex + 0][2]);
    //showDotInfo(dotLoc, wpIcon, description, titleString);
}

function setMapOnClickListeners(type) {
    // addOverlay()
    activeType = type;
    activeMarkers = true;
    updateOverlayText(type, '')
    google.maps.event.addListener(rszwMap, 'click', function (event) {
        addCurrentMarker(event.latLng)
    });
}

function addCurrentMarker(droppedPosition) {
    [validLocations, backwardMapping] = getValidDropLocations(null, false)
    dataPtIndex = parseInt(backwardMapping[find_index_closest_point(droppedPosition, validLocations)]);
    // console.log(dataPtIndex)
    // var dataPtIndex = find_index_closest_point(droppedPosition, pathPoints);


    if (startEndMarkers.length == 0) {
        order = 'Start'
        newIDs = [uuidv4(), uuidv4()];
    }
    else if (startEndMarkers.length == 1) {
        order = 'End'
        google.maps.event.clearListeners(rszwMap, 'click');
    }
    else
        return

    updateOverlayText(activeType, order)

    if (activeType === 'WP') {
        // console.log('Adding WP Marker: ' + order)
        if (order == 'Start') {
            wpStat = 1;
        }
        else {
            wpStat = 0;
        }
        [description, titleString, txtUpdated, wpIcon] = createWorkerContent(wpStat, newIDs, dataPtIndex)

        startEndMarkers.push(titleString)
        dotLoc = new google.maps.LatLng(mapData[dataPtIndex + 0][1], mapData[dataPtIndex + 0][2]);
        showDotInfo(dotLoc, wpIcon, description, titleString);
    }
    else {
        // console.log('Adding Lane Marker: ' + order)
        lane = 1
        if (order == 'Start') {
            laneStat = 1;
        }
        else {
            laneStat = 0;
        }
        [description, titleString, txtLaneEvent, lsIcon] = createLaneContent(laneStat, lane, newIDs, dataPtIndex)

        startEndMarkers.push(titleString)

        dotLoc = new google.maps.LatLng(mapData[dataPtIndex + 0][1], mapData[dataPtIndex + 0][2]);
        showDotInfo(dotLoc, lsIcon, description, titleString);
    }

    if (order == 'End') {
        startEndMarkers = [];
        activeMarkers = false;
        updateOverlayText()
    }
}

function getValidDropLocations(dataPtIndex, isRP) {

    [forwardMapping, backwardMapping, validPoints] = createMappings(dataPtIndex, isRP);

    return [validPoints, backwardMapping];
}

function createMappings(includedIndex, isRP) {
    forwardMapping = {}
    validPoints = []
    indexesRemoved = []

    rpIndex = markerLocations[rpID]
    if (!isRP) {
        for (i = 0; i <= rpIndex; i++) {
            indexesRemoved.push(i);
        }
    }

    // REQUIRES *markerLocations* TO BE SORTED BY ROW INDEX
    for (i = 0; i < currentMarkers.length; i++) {
        // Do not remove from list if was previous location or has already been removed
        if (currentMarkers[i][0] != includedIndex && !indexesRemoved.includes(currentMarkers[i][0])) {
            // console.log('Index to be removed: ' + currentMarkers[i][0].toString())
            indexesRemoved.push(parseInt(currentMarkers[i][0]))
        }
    }

    j = 0;
    for (i = 0; i < pathPoints.length; i++) {
        if (indexesRemoved.includes(i))
            forwardMapping[i] = null
        else {
            forwardMapping[i] = j
            validPoints.push(pathPoints[i])
            j++
        }
    }
    backwardMapping = flipMapping(forwardMapping);
    // console.log(forwardMapping)
    // console.log(backwardMapping)

    return [forwardMapping, backwardMapping, validPoints]
}

function flipMapping(data) {
    var key, tmp_ar = {};

    for (key in data) {
        if (data[key] != null)
            tmp_ar[data[key]] = key;
    }

    return tmp_ar;
}

function getOriginalIndex(index) {

}

// --------------------------------------------------------------------------------------------------------
// --------------------------------------   TITLE OBJECT   ------------------------------------------------
// --------------------------------------------------------------------------------------------------------
function Title(type, value, ID, partnerID) {
    this.type = type;
    this.value = value;
    this.ID = ID;
    this.partnerID = partnerID;
    // return this;
}

Title.prototype.toString = function () {
    return [this.type, this.value, this.ID, this.partnerID].join(',');
}

String.prototype.parseTitle = function () {
    title = this.split(',')
    return new Title(title[0], title[1], title[2], title[3]);
}

function createMarkerDesc(title, dataPtIndex) {
    if (title.type === 'LC') {
        lStat = "<font color='red'>Start of Lane #";
        description = "<b>Data Point#: " + String(dataPtIndex) + ", " + lStat + String(title.value) + " Closure" +
            createInputString("button", "rm_" + title.ID, "removeMarker(this.id)", "Remove Marker") +
            createInputString("button", "upd_" + title.ID, "updateMarker(this.id)", "Change Lane") + "<b>";
    }
    else if (title.type === 'LO') {
        lStat = "<font color='green'>End of Lane #";
        description = "<b>Data Point#: " + String(dataPtIndex) + ", " + lStat + String(title.value) + " Closure" +
            createInputString("button", "rm_" + title.ID, "removeMarker(this.id)", "Remove Marker") +
            createInputString("button", "upd_" + title.ID, "updateMarker(this.id)", "Change Lane") + "<b>";
    }
    else if (title.type == 'WP') {
        if (title.value == 'True') {
            wStat = "<font color='red'>Start of Workers Presence";
        }
        else if (title.value == 'False') {
            wStat = "<font color='green'>End of Workers Presence";
        }
        description = "<b>Data Point#: " + String(dataPtIndex) + ", " + wStat +
            createInputString("button", "rm_" + title.ID, "removeMarker(this.id)", "Remove Marker") + "<b>";
    }
    return description
}

function updateMarkerDescriptionHandler(marker) {
    title = marker.title.parseTitle();
    dataPtIndex = markerLocations[title.ID];
    description = createMarkerDesc(title, dataPtIndex)
    updateMarkerDescription(marker, description)
}

function createInputString(type, id, onClick, value) {
    return "<input type=\"" + type + "\" id=\"" + id + "\" onclick=\"" + onClick + "\" value=\"" + value + "\"/>";
}

function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

function removeMarker(elementID) {
    var id = elementID.split('_')[1];
    var googleMarker1 = getGoogleMarkerByID(id)
    var partnerID = googleMarker1.title.parseTitle().partnerID
    var googleMarker2 = getGoogleMarkerByID(partnerID)

    googleMarker1.setMap(null);
    removeMarkerFromList(id);

    googleMarker2.setMap(null);
    removeMarkerFromList(partnerID);

    getCurrentMarkers()
}

function removeMarkerFromList(id) {
    newMarkersList = []
    for (i = 0; i < googleMarkers.length; i++) {
        if (googleMarkers[i].title.parseTitle().ID != id) {
            newMarkersList.push(googleMarkers[i])
        }
    }
    googleMarkers = newMarkersList;
}

function updateMarker(elementID) {
    var lane = Number(window.prompt("New Lane #", ""));
    if (lane == NaN || lane > 8 || lane <= 0)
        return;

    var id = elementID.split('_')[1];
    var googleMarker1 = getGoogleMarkerByID(id)

    var partnerID = googleMarker1.title.parseTitle().partnerID

    var googleMarker2 = getGoogleMarkerByID(partnerID)

    updateLane(googleMarker1, lane, id)
    updateLane(googleMarker2, lane, partnerID)

    //var innerHTML = document.getElementById(elementID).parentElement.innerHTML;
    //document.getElementById(elementID).parentElement.innerHTML = innerHTML.replace('#' + id[1], '#' + lane)

    getCurrentMarkers()
}

function updateLane(googleMarker, lane) {
    var prevTitle = googleMarker.title.parseTitle();
    // var prevLane = prevTitle[1];
    newTitle = new Title(prevTitle.type, lane.toString(), prevTitle.ID, prevTitle.partnerID);
    googleMarker.title = newTitle.toString();

    if (prevTitle.type === 'LC')
        icon = laneClosedIcon[lane - 1];
    else
        icon = laneOpenIcon[lane - 1];
    googleMarker.setIcon(icon);

    updateMarkerDescriptionHandler(googleMarker);

    //var desc = markerDescriptions[prevTitle[2]]
    //desc = desc.replace('#' + prevTitle[1], '#' + lane)
    //markerDescriptions[prevTitle[2]] = desc
    // var desc = googleMarker.infoWindow.innerHTML;
    // newDesc = desc.replace(', ' + prevLane + ' ', ', ' + lane + ' ')
}

function getGoogleMarkerByID(ID) {
    for (var i = 0; i < googleMarkers.length; i++) {
        var title = googleMarkers[i].title.parseTitle()
        if (ID == title.ID) {
            return googleMarkers[i]
        }
    }
}

function bigLegend(x) {
    x.style.width = "300px";
    x.style.left = "1px";
    x.style.zIndex = "1";
}

function smallLegend(x) {
    x.style.width = "128px";
    x.style.left = "50px";
}


function find_closest_point_on_path(drop_pt, path_pts) {
    distances = new Array();//Stores the distances of each pt on the path from the marker point 
    distance_keys = new Array();//Stores the key of point on the path that corresponds to a distance

    //For each point on the path
    $.each(path_pts, function (key, path_pt) {
        //Find the distance in a linear crows-flight line between the marker point and the current path point
        var R = 6371; // km
        var dLat = (path_pt.lat() - drop_pt.lat()).toRad();
        var dLon = (path_pt.lng() - drop_pt.lng()).toRad();
        var lat1 = drop_pt.lat().toRad();
        var lat2 = path_pt.lat().toRad();

        var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1) * Math.cos(lat2);
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        var d = R * c;
        //Store the distances and the key of the pt that matches that distance
        distances[key] = d;
        distance_keys[d] = key;

    });
    var pathPt = path_pts[distance_keys[Array.min(distances)]];
    var x = pathToIndex.find(e => e[0] == pathPt)
    //Return the latLng obj of the second closest point to the markers drag origin. If this point doesn't exist snap it to the actual closest point as this should always exist
    // (typeof path_pts[distance_keys[Math.min(distances)] + 1] === 'undefined') ? path_pts[distance_keys[Math.min(distances)]] : path_pts[distance_keys[Math.min(distances)] + 1];
    return pathPt;
}

function find_index_closest_point(drop_pt, path_pts) {
    distances = new Array();//Stores the distances of each pt on the path from the marker point 
    distance_keys = new Array();//Stores the key of point on the path that corresponds to a distance

    //For each point on the path
    $.each(path_pts, function (key, path_pt) {
        //Find the distance in a linear crows-flight line between the marker point and the current path point
        var R = 6371; // km
        var dLat = (path_pt.lat() - drop_pt.lat()).toRad();
        var dLon = (path_pt.lng() - drop_pt.lng()).toRad();
        var lat1 = drop_pt.lat().toRad();
        var lat2 = path_pt.lat().toRad();

        var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1) * Math.cos(lat2);
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        var d = R * c;
        //Store the distances and the key of the pt that matches that distance
        distances[key] = d;
        distance_keys[d] = key;

    });
    //Return the latLng obj of the second closest point to the markers drag origin. If this point doesn't exist snap it to the actual closest point as this should always exist
    // (typeof path_pts[distance_keys[Math.min(distances)] + 1] === 'undefined') ? path_pts[distance_keys[Math.min(distances)]] : path_pts[distance_keys[Math.min(distances)] + 1];
    return distance_keys[Array.min(distances)];
}

function getPathIndex(pt) {
    return pathToIndex.find(e => e[0] == pt)[1]
}

function getCurrentMarkers() {
    markers = []
    for (var i = 0; i < googleMarkers.length; i++) {
        var title = googleMarkers[i].title.parseTitle()
        var index = markerLocations[title.ID]
        marker = [index, title.type, title.value]
        markers.push(marker)
    }

    markers.sort(sortMarkers);
    markerString = ''
    for (var i = 0, l = markers.length; i < l; i++) {
        markerString += markers[i].join(",") + ';';
        // console.log(markerString)
    }

    console.log("Markers: " + markerString);
    document.getElementById('hiddenMarkers').value = markerString;
    currentMarkers = markers;
}

function sortMarkers(a, b) {
    if (a[0] === b[0]) {
        return 0;
    }
    else {
        return (a[0] < b[0]) ? -1 : 1;
    }
}

Array.min = function (array) {
    return Math.min.apply(Math, array);
};

/** Converts numeric degrees to radians */
if (typeof (Number.prototype.toRad) === "undefined") {
    Number.prototype.toRad = function () {
        return this * Math.PI / 180;
    }
}


//************************************************************************************************************************
//
//                        Following function is invoked by clicking a button from the html file (same as startHere() function)...   
//
//************************************************************************************************************************
//****
//                        Function to place constructed map node points for approach lanes and WZ lane
//                        Also, draw rectangle bounding box between the node points
//
//****
var isFirstClick = true
function displayMapNodes_drawRectBB() {
    try {
        //****
        //                              Local variables...
        //****                                    

        if (!isFirstClick) return
        var appDataPtIcon = 'Icons\\approachPoint.png';
        var wzDataPtIcon = 'Icons\\wzPoint2.png';
        var wzLanOpenIcon = 'Icons\\wzLaneOpen3.png';
        var wzLCPtIcon = 'Icons\\orangeBarrelSmall1.png';
        var wzWPPtIcon = 'Icons\\wzWorkers4.png';
        var spdLimitMainIcon = 'Icons\\speed_limit_main.jpg';
        var spdLimitWZIcon = 'Icons\\speed_limit_wz.jpg';
        var spdLimitWPIcon = 'Icons\\speed_limit_wp.jpg';
        var dotLoc, dotLoc1, wpIconLoc;


        var halfLWApp = (laneWidth + lanePadApp) / 2;                                         //data point is in middle of the lane + approach lane padding
        var headLoc = noLanes * 5;                                                                                    //for each lane, 4 columns (lon,lat,elev,0/1,0/1)

        i = 0;
        ///console.log("No Lanes = ", noLanes, refPoint);

        for (ln = 0; ln < noLanes; ln++) {
            for (ap = 0; ap < appMapData.length; ap++) {
                dotLoc = new google.maps.LatLng(appMapData[ap][ln * 5 + 0], appMapData[ap][ln * 5 + 1]);
                //showDotInfo(dotLoc, appDataPtIcon, appDataDesc[i]);

                if (ap < appMapData.length - 1) { //mappedLaneNo == ln + 1 && 
                    var speedLimitIcon = null
                    var speedLimitSide = null
                    if (ap == 0) {
                        if (ln == 0) {
                            speedLimitIcon = spdLimitMainIcon
                            speedLimitSide = 'left'
                        }
                        else if (ln == noLanes - 1) {
                            speedLimitIcon = spdLimitMainIcon
                            speedLimitSide = 'right'
                        }
                    }
                    dotLoc1 = new google.maps.LatLng(appMapData[ap + 1][ln * 5 + 0], appMapData[ap + 1][ln * 5 + 1]);
                    //****
                    //                                                                          Draw a rectangular box around the collected map data points bet two constructed APP points
                    //                                                                          equal to the laneWidth+lanePad to see how many points are outside the box.
                    //                                                                          This visualization provides clue on a curved lane the dist between points and need for   
                    //                                                                          creating dynamic distance between map points for approach and wz lanes...
                    //****
                    drawRectBB(dotLoc, dotLoc1, halfLWApp, appMapData[ap + 0][headLoc], appMapData[ap + 1][headLoc], 'Grey', null, speedLimitIcon, speedLimitSide);
                }
                i++;
            }
        }

        //****                                    
        //                              place constructed WZ lane map data points on the map... 
        //                              Call function to associate clickable info.window for each data point...
        //****
        var halfLWWZ = (laneWidth + lanePadWZ) / 2;                                                                     //data point is in middle of the lane + WZ lane padding
        var wzIcon;
        var spherical = google.maps.geometry.spherical;
        //var laneTapering = new Array(noLanes); //[[false, ]]
        //for (ln = 0; ln < noLanes; ln++) {
        //    var laneTaperArr = new Array()
        //    var startDist, endDist
        //    for (j = 0; j < wzMapData.length; j++) {
        //        if (wzMapData[j][ln * 5 + 4] != 0) {
        //            if (startDist == null && endDist == null) {
        //                startDist = wzMapData[j][noLanes * 5 + 2];
        //                var num = wzMapData[j][ln * 5 + 4];
        //                for (k = j; k < wzMapData.length - 1; k++) {
        //                    if (wzMapData[k][ln * 5 + 4] == num && wzMapData[k + 1][ln * 5 + 4] != num) {
        //                        endDist = wzMapData[k + 1][noLanes * 5 + 2];
        //                        break;
        //                    }
        //                }
        //            }
        //            laneTaperArr.push([wzMapData[j][ln * 5 + 4], wzMapData[j][noLanes * 5 + 2], startDist, endDist])
        //            if (wzMapData[j][ln * 5 + 4] == 0) {
        //                laneTaperArr.push([wzMapData[j + 1][ln * 5 + 4], wzMapData[j + 1][noLanes * 5 + 2], startDist, endDist])
        //                endDist = null
        //                startDist = null
        //            }
        //        }
        //        else {
        //            endDist = null
        //            startDist = null
        //        }
        //    }
        //}

        i = 0;
        for (ln = 0; ln < noLanes; ln++) {
            var startDist, endDist, closedSide
            for (wz = 0; wz < wzMapData.length; wz++) {
                var speedLimitIcon = null
                var speedLimitSide = null
                if (ln == 0) {
                    if (wz == 0) {
                        speedLimitIcon = spdLimitWZIcon
                    }
                    else if (wzMapData[wz][noLanes * 5 + 1] == 1 && wzMapData[wz - 1][noLanes * 5 + 1] == 0) speedLimitIcon = spdLimitWPIcon
                    else if (wzMapData[wz][noLanes * 5 + 1] == 0 && wzMapData[wz - 1][noLanes * 5 + 1] == 1) speedLimitIcon = spdLimitWZIcon
                    if (speedLimitIcon != null) speedLimitSide = 'left'
                }
                else if (ln == noLanes - 1) {
                    if (wz == 0) {
                        speedLimitIcon = spdLimitWZIcon
                    }
                    else if (wzMapData[wz][noLanes * 5 + 1] == 1 && wzMapData[wz - 1][noLanes * 5 + 1] == 0) speedLimitIcon = spdLimitWPIcon
                    else if (wzMapData[wz][noLanes * 5 + 1] == 0 && wzMapData[wz - 1][noLanes * 5 + 1] == 1) speedLimitIcon = spdLimitWZIcon
                    if (speedLimitIcon != null) speedLimitSide = 'right'
                }
                wzIcon = wzLanOpenIcon;                                                                                                                                                                 //wz Icon
                if (wzMapData[wz][ln * 5 + 3] == 1) { wzIcon = wzLCPtIcon; }                                           //LC at this node
                //****
                //                                                                overlay icon for wz node on g. map...
                //****
                dotLoc = new google.maps.LatLng(wzMapData[wz][ln * 5 + 0], wzMapData[wz][ln * 5 + 1]);
                //showDotInfo(dotLoc, wzIcon, wzDataDesc[i]);
                //****
                //                                                                For workers present, the icon will be displayed outside the last (right most) lane only 
                //                                                                and not on each lane...
                //                                                                added on Dec. 1, 2017
                //****
                if (wzMapData[wz][noLanes * 5 + 1] == 1)                                                                                                              //Workers present at this node
                {
                    if (ln == noLanes - 1) {
                        //****                                   
                        //                                                                                   Construct coords to overlay workers present icon outside the last lane...                                     
                        //****
                        wpIconLoc = spherical.computeOffset(dotLoc, halfLWWZ * 2, wzMapData[wz + 0][headLoc] + 90.0);

                        //                                                                                   wpIconLoc = new google.maps.LatLng(wzMapData[wz][ln*4+0],wzMapData[wz][ln*4+1]);  outside the last lane...
                        //                                                                        showDotInfo(wpIconLoc,wzWPPtIcon,wzDataDesc[i]);
                        showDotInfo(wpIconLoc, wzWPPtIcon, "Workers Present...", 'WPIcons,');                          //Clickable description for infoWindow...
                    }
                }
                //****
                //                                                                Draw a rectangular box on the collected map data lane points bet two points (WZ map point) 
                //                                                                equal to the laneWidth to see how many points are outside the box. This visualization provides clue 
                //                                                                of curved lane and how to create dynamic distance between map points for approach and wz lanes...
                //****
                //if (wzMapData[wz][noLanes * 5 + 4] == 1 && !laneTapering[ln])
                if (wz < wzMapData.length - 1) { //mappedLaneNo == ln + 1 && 
                    //console.log(wzMapData[wz + 1][ln * 5 + 0])
                    dotLoc1 = new google.maps.LatLng(wzMapData[wz + 1][ln * 5 + 0], wzMapData[wz + 1][ln * 5 + 1]);
                    //****
                    //                                                                          Draw a rectangular box around the collected map data lane points bet two constructed WZ points
                    //                                                                          equal to the laneWidth+lanePad to see how many points are outside the box. 
                    //                                                                          This visualization provides clue on a curved lane the dist between points and need for   
                    //                                                                          creating dynamic distance between map points for approach and wz lanes...
                    //****                        
                    var color = 'Blue';
                    var draw = true;
                    var currTaperVal;
                    if (mappedLaneNo != ln + 1) {
                        currTaperVal = wzMapData[wz][ln * 5 + 4]
                        if (wzMapData[wz][ln * 5 + 4] != 0) {
                            color = 'Red'
                            var num, direc;
                            if (wzMapData[wz][ln * 5 + 4] == 1) {
                                // console.log('Tapering Right')
                                num = 1;
                                direc = 'right'
                                if (wzMapData[wz][ln * 5 + 3] == 1 && wzMapData[wz][(ln + 1) * 5 + 3] == 0 && wzMapData[wz][(ln + 1) * 5 + 4] == 0) {
                                    closedSide = 'right'
                                }
                                else closedSide = null
                            }
                            else if (wzMapData[wz][ln * 5 + 4] == 2) {
                                // console.log('Tapering Left')
                                num = 2;
                                direc = 'left'
                                if (wzMapData[wz][ln * 5 + 3] == 1 && wzMapData[wz][(ln - 1) * 5 + 3] == 0 && wzMapData[wz][(ln - 1) * 5 + 4] == 0) closedSide = 'left'
                                else closedSide = null
                            }
                            else {
                                // console.log('Weird taper, drawing rect')
                                if (draw) drawRectBB(dotLoc, dotLoc1, halfLWWZ, wzMapData[wz + 0][headLoc], wzMapData[wz + 1][headLoc], color, null, speedLimitIcon, speedLimitSide);
                                draw = false;
                            }
                            var currDist, nextDist, deltaDist, startFrac, endFrac;

                            currDist = wzMapData[wz][noLanes * 5 + 2];

                            if ((startDist == null && endDist == null) || currDist > endDist) {
                                startDist = wzMapData[wz][noLanes * 5 + 2];
                                var num = wzMapData[wz][ln * 5 + 4];
                                for (j = wz; j < wzMapData.length - 1; j++) {
                                    if ((wzMapData[j][ln * 5 + 4] == num && wzMapData[j + 1][ln * 5 + 4] != num) || j == wzMapData.length - 2) {
                                        endDist = wzMapData[j + 1][noLanes * 5 + 2];
                                        break;
                                    }
                                }
                            }

                            if (startDist == null || endDist == null) {
                                // console.log('Failed to find start/end distances, drawing rect')
                                if (draw) drawRectBB(dotLoc, dotLoc1, halfLWWZ, wzMapData[wz + 0][headLoc], wzMapData[wz + 1][headLoc], color, null, speedLimitIcon, speedLimitSide);
                                draw = false;
                            }
                            deltaDist = endDist - startDist;

                            if (wz < wzMapData.length - 1) nextDist = wzMapData[wz + 1][noLanes * 5 + 2];
                            else nextDist = deltaDist + startDist;

                            startFrac = (currDist - startDist) / deltaDist;
                            endFrac = (nextDist - startDist) / deltaDist;

                            if (startFrac > 1 || startFrac < 0) {
                                console.log("Error: Start fraction invalid, startFrac = " + startFrac + ". Setting startFrac to 1")
                                startFrac = 1
                            }
                            if (endFrac > 1 || endFrac < 0) {
                                console.log("Error: Start fraction invalid, endFrac = " + endFrac + ". Setting endFrac to 1")
                                endFrac = 1
                            }

                            if (wzMapData[wz][ln * 5 + 3] == 0) {
                                startFrac = 1 - startFrac
                                endFrac = 1 - endFrac
                                if (direc == 'left') direc = 'right'
                                else direc = 'left'
                            }

                            if (draw) drawPolygonBB(dotLoc, dotLoc1, halfLWWZ, wzMapData[wz + 0][headLoc], wzMapData[wz + 1][headLoc], direc, startFrac, endFrac, color, speedLimitIcon, speedLimitSide);
                            draw = false;
                        }
                        else if (wzMapData[wz][ln * 5 + 3] == 0) color = 'Green';
                        else if (mappedLaneNo != ln + 1) color = 'Red';
                        if (currTaperVal != 0 && wz != wzMapData.length - 2 && currTaperVal != wzMapData[wz + 1][ln * 5 + 4]) {
                            startDist = null;
                            endDist = null;
                        }
                    }
                    //console.log('No taper, drawing rect')
                    if (closedSide == 'right') {
                        if (wzMapData[wz][(ln + 1) * 5 + 3] != 0 || wzMapData[wz][(ln + 1) * 5 + 4] != 0) closedSide = null
                    }
                    else if (closedSide == 'left') {
                        if (wzMapData[wz][(ln - 1) * 5 + 3] != 0 || wzMapData[wz][(ln - 1) * 5 + 4] != 0) closedSide = null
                    }
                    else if (ln < noLanes - 1) {
                        if (wzMapData[wz][ln * 5 + 3] == 1 && wzMapData[wz][(ln + 1) * 5 + 3] == 0 && wzMapData[wz][(ln + 1) * 5 + 4] == 0) closedSide = 'right'
                        //else closedSide = null
                    }
                    else if (ln > 0) {
                        if (wzMapData[wz][ln * 5 + 3] == 1 && wzMapData[wz][(ln - 1) * 5 + 3] == 0 && wzMapData[wz][(ln - 1) * 5 + 4] == 0) closedSide = 'left'
                        //else closedSide = null
                    }
                    if (draw) drawRectBB(dotLoc, dotLoc1, halfLWWZ, wzMapData[wz + 0][headLoc], wzMapData[wz + 1][headLoc], color, closedSide, speedLimitIcon, speedLimitSide);
                }
                i++;
                if (wz == wzMapData.length - 1) {
                    startDist = null;
                    endDist = null;
                }
            }
        }
        isFirstClick = false
        return false
        //
        //                              Disable the button now...              Following doesn't work, may be need to make the button global...
        //                              Will do some other time...
        //                              
        //                 document.getElementsByClassName('overlay_btn').disabled = true;
    }
    catch (err) {
        console.log('error')
        console.log(err)
        return false
    }
}                                                                                                                                        //end of displayMapNodes_drawBB

//****   
//                        Function below draws a rectangular bounding box on the collected vehicle path lane data points bet two constructed
//                        waypoints (node points). The bounding box is equal to the laneWidth to see how many vehicle path points are falling 
//                        outside the box that indicates that the map matching would fail in that area and the constructed waypoints (node points)
//                        are incorrect. This visualization is particularly handy to see how the waypoints are selected by the python s/w that 
//                        generated the waypoints (node points) on a curved lane...
//****                                           

function drawRectBB(dotLoc0, dotLoc1, dist, head0, head1, fColor, closedSide, speedLimitIcon, speedLimitSide) {
    var spherical = google.maps.geometry.spherical;
    var tLeft, tRight, bRight, bLeft;
    //
    //                                  Construct coords for four corners
    //
    tLeft = spherical.computeOffset(dotLoc0, dist, head0 - 90.0);
    tRight = spherical.computeOffset(dotLoc0, dist, head0 + 90.0);
    bRight = spherical.computeOffset(dotLoc1, dist, head1 + 90.0);
    bLeft = spherical.computeOffset(dotLoc1, dist, head1 - 90.0);
    //                                                                           
    //                                  Draw the rectangle polygon.
    //
    if (fColor == 'Red') {
        var rectCoords = [tLeft, tRight, bRight, bLeft];

        var leftColor = '#FFFFFF';
        var rightColor = '#FFFFFF';
        if (closedSide == 'left') rightColor = '#FF0000';
        else if (closedSide == 'right') leftColor = '#FF0000';
        else if (closedSide == null) {
            rightColor = '#FF0000';
            leftColor = '#FF0000';
        }

        var mapRect = new google.maps.Polygon({
            paths: rectCoords,
            strokeColor: '#000000',
            strokeOpacity: 1,
            strokeWeight: 0,
            fillColor: '#FF0000',
            fillOpacity: 0.50
        });
        mapRect.setMap(rszwMap)
        var mapLine1 = new google.maps.Polyline({
            path: [tLeft, bLeft],
            strokeColor: leftColor,
            strokeOpacity: 1,
            strokeWeight: 2
        });
        var mapLine2 = new google.maps.Polyline({
            path: [tRight, bRight],
            strokeColor: rightColor,
            strokeOpacity: 1,
            strokeWeight: 2
        });
        var mapLine3 = new google.maps.Polyline({
            path: [tRight, tLeft],
            strokeColor: '#000000',
            strokeOpacity: .5,
            strokeWeight: 1
        });
        var mapLine4 = new google.maps.Polyline({
            path: [bRight, bLeft],
            strokeColor: '#000000',
            strokeOpacity: .5,
            strokeWeight: 1
        });
        mapLine1.setMap(rszwMap)
        mapLine2.setMap(rszwMap)
        mapLine3.setMap(rszwMap)
        mapLine4.setMap(rszwMap)
    }
    else {
        var rectCoords = [tLeft, tRight, bRight, bLeft];
        var mapLine1 = new google.maps.Polyline({
            path: [tLeft, bLeft],
            strokeColor: '#FFFFFF',
            strokeOpacity: 1,
            strokeWeight: 2
        });
        var mapLine2 = new google.maps.Polyline({
            path: [tRight, bRight],
            strokeColor: '#FFFFFF',
            strokeOpacity: 1,
            strokeWeight: 2
        });
        var mapLine3 = new google.maps.Polyline({
            path: [tRight, tLeft],
            strokeColor: '#000000',
            strokeOpacity: .5,
            strokeWeight: 1
        });
        var mapLine4 = new google.maps.Polyline({
            path: [bRight, bLeft],
            strokeColor: '#000000',
            strokeOpacity: .5,
            strokeWeight: 1
        });
        mapLine1.setMap(rszwMap)
        mapLine2.setMap(rszwMap)
        mapLine3.setMap(rszwMap)
        mapLine4.setMap(rszwMap)
    }
    //var mapRect = new google.maps.Polygon({
    //    paths: rectCoords,
    //    strokeColor: '#FF0000',
    //    strokeOpacity: 1,
    //    strokeWeight: 1,
    //    fillColor: fColor,
    //    fillOpacity: 0.10
    //});
    //mapRect.setMap(rszwMap)
    if (closedSide != null) {
        if (closedSide == 'left') {
            p1 = tLeft;
            p2 = bLeft;
        }
        else {
            p1 = tRight;
            p2 = bRight;
        }
        var heading = google.maps.geometry.spherical.computeHeading(p1, p2);
        var totDist = google.maps.geometry.spherical.computeDistanceBetween(p1, p2)
        var dist = 5;
        var max = Math.floor((totDist / dist) - 1);
        for (i = 0; i < max; i++) {
            pt = spherical.computeOffset(p1, i * dist, heading);
            addCustomMarker(pt, 'Icons\\orangeBarrelSmall1.png');
        }
        pt = spherical.computeOffset(p1, ((max - 1) * dist + totDist) / 2, heading);
        addCustomMarker(pt, 'Icons\\orangeBarrelSmall1.png');
    }
    if (speedLimitIcon != null && speedLimitSide != null) {
        if (speedLimitSide == 'left') {
            pt = spherical.computeOffset(dotLoc0, 15, head0 - 90.0);
            addCustomMarker(pt, speedLimitIcon);
        }
        else {
            pt = spherical.computeOffset(dotLoc0, 15, head0 + 90.0);
            addCustomMarker(pt, speedLimitIcon);
        }
    }
}                                                                                                                                        //end of drawRectBB

function drawPolygonBB(dotLoc0, dotLoc1, dist, head0, head1, side, fracStart, fracEnd, fColor, speedLimitIcon, speedLimitSide) {
    var spherical = google.maps.geometry.spherical;
    var tLeft, tRight, bRight, bLeft;
    if (side == 'left') { //Lane tapering to the left
        tLeft = spherical.computeOffset(dotLoc0, dist, head0 - 90.0);
        tRight = spherical.computeOffset(dotLoc0, dist * 2 * (0.5 - fracStart), head0 + 90.0);
        bRight = spherical.computeOffset(dotLoc1, dist * 2 * (0.5 - fracEnd), head1 + 90.0);
        bLeft = spherical.computeOffset(dotLoc1, dist, head1 - 90.0);
        var mapLine2 = new google.maps.Polyline({
            path: [tRight, bRight],
            strokeColor: '#FFFFFF',
            strokeOpacity: 1,
            strokeWeight: 2
        });
        var mapLine3 = new google.maps.Polyline({
            path: [tRight, tLeft],
            strokeColor: '#000000',
            strokeOpacity: .5,
            strokeWeight: 1
        });
        var mapLine4 = new google.maps.Polyline({
            path: [bRight, bLeft],
            strokeColor: '#000000',
            strokeOpacity: .5,
            strokeWeight: 1
        });
        mapLine2.setMap(rszwMap)
        mapLine3.setMap(rszwMap)
        mapLine4.setMap(rszwMap)
    }
    else { //Lane tapering to the right
        tLeft = spherical.computeOffset(dotLoc0, dist * 2 * (0.5 - fracStart), head0 - 90.0);
        tRight = spherical.computeOffset(dotLoc0, dist, head0 + 90.0);
        bRight = spherical.computeOffset(dotLoc1, dist, head1 + 90.0);
        bLeft = spherical.computeOffset(dotLoc1, dist * 2 * (0.5 - fracEnd), head1 - 90.0);
        var mapLine1 = new google.maps.Polyline({
            path: [tLeft, bLeft],
            strokeColor: '#FFFFFF',
            strokeOpacity: 1,
            strokeWeight: 2
        });
        var mapLine3 = new google.maps.Polyline({
            path: [tRight, tLeft],
            strokeColor: '#000000',
            strokeOpacity: .5,
            strokeWeight: 1
        });
        var mapLine4 = new google.maps.Polyline({
            path: [bRight, bLeft],
            strokeColor: '#000000',
            strokeOpacity: .5,
            strokeWeight: 1
        });
        mapLine1.setMap(rszwMap)
        mapLine3.setMap(rszwMap)
        mapLine4.setMap(rszwMap)
    }

    var p1, p2
    if (side == 'left') { //Lane tapering to the left
        tLeft = spherical.computeOffset(dotLoc0, -dist * 2 * (0.5 - fracStart), head0 - 90.0);
        tRight = spherical.computeOffset(dotLoc0, dist, head0 + 90.0);
        bRight = spherical.computeOffset(dotLoc1, dist, head1 + 90.0);
        bLeft = spherical.computeOffset(dotLoc1, -dist * 2 * (0.5 - fracEnd), head1 - 90.0);
        p1 = tLeft;
        p2 = bLeft;
        p3 = tRight;
        p4 = bRight;
    }
    else { //Lane tapering to the right
        tLeft = spherical.computeOffset(dotLoc0, dist, head0 - 90.0);
        tRight = spherical.computeOffset(dotLoc0, -dist * 2 * (0.5 - fracStart), head0 + 90.0);
        bRight = spherical.computeOffset(dotLoc1, -dist * 2 * (0.5 - fracEnd), head1 + 90.0);
        bLeft = spherical.computeOffset(dotLoc1, dist, head1 - 90.0);
        p1 = tRight;
        p2 = bRight;
        p3 = tLeft;
        p4 = bLeft;
    }
    //                                  
    //                                  Construct coords for four corners                             
    //
    //                                                                           
    //                                  Draw the rectangle polygon.
    //
    //var mapLine1 = new google.maps.Polyline({
    //    path: [tLeft, bLeft],
    //    strokeColor: '#FF0000',
    //    strokeOpacity: 1,
    //    strokeWeight: 1,
    //    fillColor: 'Orange',
    //    fillOpacity: 0.20
    //});
    //mapLine1.setMap(rszwMap)
    //var mapLine2 = new google.maps.Polyline({
    //    path: [tRight, bRight],
    //    strokeColor: '#FF0000',
    //    strokeOpacity: 1,
    //    strokeWeight: 1,
    //    fillColor: 'Orange',
    //    fillOpacity: 0.20
    //});
    //mapLine2.setMap(rszwMap)
    var rectCoords = [tLeft, tRight, bRight, bLeft];
    var mapRect = new google.maps.Polygon({
        paths: rectCoords,
        strokeColor: '#FF0000',
        strokeOpacity: 1,
        strokeWeight: 0,
        fillColor: 'Red',
        fillOpacity: 0.50
    });
    mapRect.setMap(rszwMap)
    var mapLine5 = new google.maps.Polyline({
        path: [p3, p4],
        strokeColor: '#FF0000',
        strokeOpacity: 1,
        strokeWeight: 2
    });
    mapLine5.setMap(rszwMap)
    var mapLine6 = new google.maps.Polyline({
        path: [p1, p3],
        strokeColor: '#000000',
        strokeOpacity: .5,
        strokeWeight: 1
    });
    mapLine6.setMap(rszwMap)
    var mapLine7 = new google.maps.Polyline({
        path: [p2, p4],
        strokeColor: '#000000',
        strokeOpacity: .5,
        strokeWeight: 1
    });
    mapLine7.setMap(rszwMap)

    var heading = google.maps.geometry.spherical.computeHeading(p1, p2);
    var totDist = google.maps.geometry.spherical.computeDistanceBetween(p1, p2)
    var dist = 5;
    var max = Math.floor((totDist / dist) - 1);
    for (i = 0; i < max; i++) {
        pt = spherical.computeOffset(p1, i * dist, heading);
        addCustomMarker(pt, 'Icons\\orangeBarrelSmall1.png');
    }
    pt = spherical.computeOffset(p1, ((max - 1) * dist + totDist) / 2, heading);
    addCustomMarker(pt, 'Icons\\orangeBarrelSmall1.png');

    if (speedLimitIcon != null && speedLimitSide != null) {
        if (speedLimitSide == 'left') {
            pt = spherical.computeOffset(dotLoc0, 15, head0 - 90.0);
            addCustomMarker(pt, speedLimitIcon);
        }
        else {
            pt = spherical.computeOffset(dotLoc0, 15, head0 + 90.0);
            addCustomMarker(pt, speedLimitIcon);
        }
    }
}

function addCustomMarker(dotPos, dotIcon) {
    dotMarker = new google.maps.Marker(
        {
            position: dotPos,
            map: rszwMap,
            icon: dotIcon,
        }
    );
}

google.maps.InfoWindow.prototype.isOpen = function () {
    var map = this.getMap();
    return (map !== null && typeof map !== "undefined");
}

function updateMarkerDescription(marker, description) {
    if (marker.infoWindow != null) {
        marker.infoWindow.setContent(description)
        if (marker.infoWindow.isOpen()) {
            marker.infoWindow.close();
            marker.infoWindow.open(rszwMap, marker);
        }
    }
    else {
        marker.infoWindow = new google.maps.InfoWindow({
            content: description
        })
    }
}

//function addMarkerDescription(marker, description) {
//    marker.
//    google.maps.event.addListener(dotMarker, 'click', (function (dotMarker) {
//        return function () {
//            infoWindow.setContent(dotDesc);
//            infoWindow.open(rszwMap, dotMarker);
//        }
//    })
//        (dotMarker));
//}

//  *******************************************************************
//
//                        Function testDrive() to show test car on google map
//                        This function is invoked from button click on the visualization screen 
//                        THIS FUNCTION IS NO LONGER USED IN WZ MAP VISUALIZATION - REMOVED... 
//
//  *******************************************************************

//
//                        ****      function showCurrPos (newPos, head)...            NOT USED, REMOVED from THIS SOURCE ...****
//                                      

//
//                        Alternate function to construct infowindow for clickable data point description...              
//                                                    
function showDotInfo(dotPos, dotIcon, dotDesc, titleString) {
    title = titleString.parseTitle();
    // console.log(titleString)

    isDraggable = false;
    criticalMarker = false;
    snap = false;
    if (title.type === "RP" || title.type === "WP" || title.type === "LO" || title.type === "LC") {
        isDraggable = true;
        snap = true;
        criticalMarker = true;
    }
    else if (title.type === "Data Log") {
        criticalMarker = true;
    }
    else if (title.type == "Start Point") {
        isDraggable = true
        criticalMarker = true;
    }
    else if (title.type == "End Point") {
        isDraggable = true
        criticalMarker = true;
    }

    var dotMarker = new google.maps.Marker(
        {
            position: dotPos,
            map: rszwMap,
            icon: dotIcon,
            draggable: isDraggable,
            title: titleString,
        }
    );

    if (title.type == "Start Point") {
        startCircle.bindTo("center", dotMarker, "position")
    }
    else if (title.type == "End Point") {
        endCircle.bindTo("center", dotMarker, "position")
    }


    // Set InfoWindow as property of marker so it can be accessed later
    updateMarkerDescription(dotMarker, dotDesc)

    //
    //                                  Set listener for information window. Onclick popup display string
    //

    if (criticalMarker) {
        google.maps.event.addListener(dotMarker, 'click', (function (e) {
            this.infoWindow.open(rszwMap, this)
        }));
    }
    else {
        google.maps.event.addListener(dotMarker, 'click', (function (e) {
            if (activeMarkers) {
                addCurrentMarker(e.latLng)
            }
            else {
                this.infoWindow.open(rszwMap, this)
            }
        }));
    }

    if (criticalMarker) {
        googleMarkers.push(dotMarker)
        if (isDraggable) {
            if (snap) {
                google.maps.event.addDomListener(dotMarker, 'dragend', function (e) {
                    title = this.title.parseTitle();
                    [validLocations, backwardMapping] = getValidDropLocations(markerLocations[title.ID], title.type == 'RP')
                    pathPtIndex = parseInt(backwardMapping[find_index_closest_point(e.latLng, validLocations)]);
                    markerLocations[title.ID] = pathPtIndex;

                    this.setPosition(pathPoints[pathPtIndex]);

                    updateMarkerDescriptionHandler(this);

                    getCurrentMarkers()
                })
            }
            else {

                google.maps.event.addDomListener(dotMarker, 'dragend', function (e) {
                    title = this.title.parseTitle();
                    [validLocations, backwardMapping] = getValidDropLocations(markerLocations[title.ID], title.type == 'RP')
                    pathPtIndex = parseInt(backwardMapping[find_index_closest_point(e.latLng, validLocations)]);
                    markerLocations[title.ID] = pathPtIndex;

                    updateMarkerDescriptionHandler(this);

                    getCurrentMarkers()
                })
            }
        }
        getCurrentMarkers()
    }
}