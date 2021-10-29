<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="V2X_Verification.aspx.cs" Inherits="Neaera_Website_2018.V2X_Verification" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title></title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <link rel="stylesheet" href="assets_v2x/css/uswds.min.css">
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
    <!-- V2X Styles -->
    <link rel="stylesheet" href="css/styles.css">
    <link rel="stylesheet" href="css/formdesign.css">
    <script src="assets_v2x/js/uswds.min.js"></script>
    <!-- Redesign Styles -->
    <link rel="stylesheet" href="css/redesign_styles.css">
    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    <%--

    <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
    <script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>--%>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <%--<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script><%----%>
     
    <%--<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>--%>

    <link href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/css/toastr.min.css" rel="stylesheet" />
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/js/toastr.min.js"></script>
    
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

    <style>
        #map {
            height: 600px;
            width: 100%;
        }

        #info-box {
            background-color: white;
            border: 1px solid black;
            font-size: 15px;
            width: 300px;
        }

        .partialCenter {
            margin-left: 20%;
            margin-top: 10px
        }

        #listConfigurationFiles {
            margin-left: 20%;
            width: 400px;
        }

        .tab-pane {
            border-style: double;
            border-color: lightgrey;
            height: 1400px;
            position: relative;
        }

        .navBtnContianer {
            position: absolute;
            bottom: 0px;
            width: 100%
        }

        .nextBtn {
            position: absolute;
            right: 15px;
            bottom: 8px;
        }
         .nextBtnAddInfo {
            position: absolute;
            right: 70px;
            bottom: 8px;
        }
        .prevBtn {
            position: absolute;
            left: 15px;
            bottom: 8px;
        }

        #top-info {
            position: relative
        }

        #menu-top {
            position: absolute;
            right: 0px;
            bottom: 0px
        }

        #menu-top a {
            color: #000;
            text-decoration: none;
            font-weight: 500;
            padding: 25px 15px 25px 15px;
            text-transform: uppercase;
            font-size: 16px;
            font-weight: 900;
            color: white
        }

        .menu-top-active {
            background-color: #929292;
            cursor: none;
            pointer-events: none;
        }

        .top-nav {
            padding-left: 0;
            margin-bottom: 0;
            list-style: none;
        }

        .top-nav > li {
            position: relative;
            display: block;
        }

        .top-nav > li > a {
            position: relative;
            display: block;
            padding: 10px 15px;
        }

        .top-nav > li > a:hover,
        .top-nav > li > a:focus {
            text-decoration: none;
            background-color: #929292;
        }

        .top-navbar-nav {
            margin: 0;
        }

        .top-navbar-nav > li {
            float: left;
        }

        .top-navbar-nav > li > a {
            padding-top: 15px;
            padding-bottom: 15px;
        }

        table {
            width: 70%;
        }

        table, th, td {
            border: solid 1px #DDD;
            border-collapse: collapse;
            padding: 2px 3px;
            text-align: center;
        }

        .btnDisabled {
            background: grey !important;
        }

        .wzInfo_text {
            /*width: calc(20% - 10px);*/
            height: 800px;
            position: absolute;
            font-size: 13px;
            background-color: lightyellow;
            /*left: 10px;*/
        }

        .overlay_btn {
            height: 25px;
            width: 120px;
            position: absolute;
            left: 289px;
            font-size: 13px;
        }

        .wzLegends {
            width: 170px;
            background-color: lightblue;
            position: absolute;	
            left: 28px;
            margin-left: auto;
            margin-right: auto;
        }

        .map_canvas {
            height: 800px;
            /*width: 80%;*/
            width: 100%;
        }
    </style>

    <script>
        $(function () {
            $("#tabs").tabs();
        });
    </script>
</head>
<body>
    <form id="form1" method="post" runat="server">
        <div id="top-info">
            <div class="grid-container">
                <div class="hero-intro">
                    <div class="grid-row">
                        <div class="tablet:grid-col-8">
                            <h2 align="left">V2X TMC Data Collection Website </h2>
                        </div>
                    </div>
                    <div class="grid-row">
                        <div class="tablet:grid-col-8">
                            <p align="left">
                                Work Zone Data Exchange - Verify Work Zones
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <ul id="menu-top" class="top-nav top-navbar-nav top-navbar-right">
                <li><a href="V2x_Home.aspx">HOME</a></li>
                <li><a href="V2X_ConfigCreator.aspx">CONFIGURATION</a></li>
                <li><a href="V2X_Upload.aspx">UPLOAD</a></li>
                <li><a href="V2X_Verification.aspx" class="menu-top-active" onclick="return false;">VERIFICATION</a></li>
                <li><a href="V2X_Published.aspx">PUBLISHED</a></li>
                <li><a href="V2X_Logs.aspx">LOGGING</a></li>
            </ul>
        </div>

        <!-- Page content starts here -->
        <div class="form-style-2">
            <div class="grid-container">
                <h1 class="text-center">Work Zone Verification</h1>
                <div class="form-style-2-heading">Choose Work Zone to Visualize</div>

                <div class="form-style-4" style="min-width: 1000px;">
                    <div class="grid-container">
                        <!-- Top elements -->
                        <div class="row">
                            <div class="column" style="width: 450px;">
                                <div>
                                    <div>
                                        <asp:ListBox ID="listConfigurationFiles" runat="server" Style="margin-left: 5%; width: 400px; height: 150px"></asp:ListBox>
                                    </div>
                                    <asp:HiddenField runat="server" ID="myHiddenoutputlist" />
                                    <asp:HiddenField runat="server" ID="hiddenMarkers" />
                                    <asp:HiddenField runat="server" ID="HiddenWZID" />
                                    <asp:Button ID="VisualizeButton" class="upload partialCenter" runat="server" Text="Load Visualization" Style="margin-left: 5%;" OnClick="VisualizeButton_Click" /><br />
                                    <asp:Button ID="VerificationButton" class="partialCenter" runat="server" Text="Verify Work Zone Data and Publish" Style="display: none; margin-left: 5%;" OnClientClick="return confirm('Are you sure you want to publish this work zone?')" OnClick="VerificationButton_Click" /><br />
                                    <input type="hidden" id="hdnParam" runat="server" clientidmode="Static" value="This is my message" />
                                    <input type="hidden" id="msgtype" runat="server" clientidmode="Static" />
                                </div>
                            </div>
                            
                            <div class="column" style="width: 150px;">
                                <div>
                                    <input type="button" id="verifyMarkersButton" value="Verify markers" onclick="submitStuff()"/><br />
                                    <asp:Button ID="updatePathDataButton" class="btnDisabled" runat="server" Text="Confirm Edit" OnClick="updatePathData_Click" disabled="disabled" style="margin-top: 10px;"/><br />
                                    <asp:Button ID="uploadPathDataButton" class="btnDisabled" runat="server" Text="Save Work Zone" OnClick="uploadPathData_Click" disabled="disabled" style="margin-top: 10px;"/><br />
                                </div>
                            </div>
                            
                            <div class="column" style="width: calc(100% - 600px)">

                                <div>
                                    <ol>
                                        <li>Edit Work Zone
                                            <div style="margin-left: 5px">
                                                <b>Move markers</b> (drag), <b>add markers</b> (buttons at top of map) and <b>remove markers</b> (button in popup window). 
                                                NOTE: WZ Visualization will not update until you hit the "Confirm Edits" button
                                            </div>
                                        </li>
                                        <li>Verify Markers
                                            <div style="margin-left: 5px">
                                                Hit <b>Verify Markers</b> button. 
                                                If markers are valid, "Confirm Edit" button will be enabled. 
                                                If the markers are invalid, a popup will be shown with the errors found.
                                            </div>
                                        </li>
                                        <li>Confirm Edits
                                            <div style="margin-left: 5px">
                                                Hit <b>Confirm Edits</b> button. 
                                                Local work zone visualization will be updated with edits made. 
                                                'Save Work Zone' will be enabled.
                                            </div>
                                        </li>
                                        <li>Save Work Zone
                                            <div style="margin-left: 5px">
                                                Hit <b>Save Work Zone</b> button.
                                                Updated work zone will be uploaded and message generation will begin. 
                                                <b>Message generation will take up to 3 minutes</b>. To check if the work zone map has been updated, 
                                                re-load the visualization in the "Select Work Zone" tab and ensure that the visualization has recently completed updates.
                                            </div>
                                        </li>          
                                    </ol>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Bottom elements -->
            <div class="row" id="mapVisualizerContainer" style="display: none">
                <!-- Map Legend -->
                <div class="column" style="width: 250px;">

                    <!--	Define area to display WZ Infromation...	-->
                    <p class="wzInfo_text" id="wzInfo_text" style="overflow-y: scroll"></p>

                    <!--	Button to overlay bounding box...			-->
                    <!--	<button class="overlay_btn" onclick="displayMapNodes_drawRectBB();">Overlay WZ Map</button>  -->

                    <!--	Show map legends...		-->
                    <!--	<img src = "./Icons/Legends-RSZW6.png" class="wzLegends">  -->
                </div>

                <!-- Map Canvas -->
                <div class="column" style="width: calc(100% - 250px);">
                    <!--	Canvas for overlaying content on Google Map	-->
                    <div class="map_canvas" id="map_canvas"></div>
                    <asp:HiddenField runat="server" ID="HiddenField1" />

                    <%--<div id="mapOverlay" style="height: 60px; background: #DDDDDD; position: absolute; top: 0px; left: 240px; right: 60px">
                        Adding Lane 1 Closure Pair (current marker: <b>Lane 1 Closing</b>)
                    </div>--%>

                    <div id="mapControlsDiv" style="margin-left: calc(214px + ((65% - 234px) / 2))">
                        <button type="button" id="addLaneClosureBtn" onclick="add_lane_closure()" style="font-size: 16px">Add Lane Closure</button>
                        <button type="button" id="addWorkerPresenceBtn" onclick="add_work_presence()" style="font-size: 16px">Add Worker Presence</button>
                        <div id="mapBtnsOverlay" style="position: absolute; top: 0px; height: 50px; width: 100%; background: #DDDDDD; font-size: large; display: none">
                            Click To Add <b>Start Of Lane 1 Closure</b> Marker
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>

            function doTab(obj) {
                var index = $(".active").attr("data_id");//get current active tab
                if ((obj == "Previous") || (obj == "Previous_Tab2") || (obj == "Previous_Tab3") || (obj == "Previous_Tab4")) {
                    index = parseInt(index) - 1;//parseInt() convert index from string type to int type
                }
                else {
                    index = parseInt(index) + 1;
                }
                $('.nav-tabs a[data_id="' + index + '"]').tab('show');
            }


            var map;

            function initMap() {
                var boulder = { lat: 40.93977, lng: -105.185182 };
                var myMapOptions =															//gMap options... 			
                {
                    zoom: 4,															//Works only if fitBounds below is commented out...
                    center: boulder,			//Reference Point...
                    // center: new google.maps.LatLng(mapData[0][1], mapData[0][2]),	//First map data point
                    mapTypeId: google.maps.MapTypeId.HYBRID,							//Satellite + Street names
                    mapTypeControl: true,
                    zoomControl: true,
                    scaleControl: true,
                    mapTypeControl: true,
                    streetViewControl: true,
                    rotateControl: true,
                    fullscreenControl: true
                };	
                map = new google.maps.Map(document.getElementById('map'), myMapOptions);
			    map.setTilt(0);
                center_display = document.getElementById('info-box')
                map.controls[google.maps.ControlPosition.TOP_CENTER].push(center_display);
                //initEvents();
            }
            // initMap()

            function loadGeoJsonString(geoString) {
                // var geojson = JSON.parse(geoString);
                // map.data.addGeoJson(geojson);
                // zoom(map);
                // loadJsonInfo();
                startHere();
                $('#mapVisualizerContainer').show()
                // openVisPopup();
            }

            /**
             * Update a map's viewport to fit each geometry in a dataset
             * @param {google.maps.Map} map The map to adjust
             */
            function zoom(map) {
                var bounds = new google.maps.LatLngBounds();
                map.data.forEach(function (feature) {
                    processPoints(feature.getGeometry(), bounds.extend, bounds);
                });
                map.fitBounds(bounds);
            }

            /**
             * Process each point in a Geometry, regardless of how deep the points may lie.
             * @param {google.maps.Data.Geometry} geometry The structure to process
             * @param {function(google.maps.LatLng)} callback A function to call on each
             *     LatLng point encountered (e.g. Array.push)
             * @param {Object} thisArg The value of 'this' as provided to 'callback' (e.g.
             *     myArray)
             */
            function processPoints(geometry, callback, thisArg) {
                if (geometry instanceof google.maps.LatLng) {
                    callback.call(thisArg, geometry);
                }
                else if (geometry instanceof google.maps.Data.Point) {
                    callback.call(thisArg, geometry.get());
                }
                else {
                    geometry.getArray().forEach(function (g) {
                        processPoints(g, callback, thisArg);
                    });
                }
            }

            function loadGeoJson() {
                var geojson_string = $('#geojsonStringDiv').text()
                loadGeoJsonString(geojson_string);
            }


            function loadGeoJsonAndShowContent(geoString) {
                loadGeoJsonString("");
                showContent()
            }

            function loadJsonInfo() {
                var infowindow_json = new google.maps.InfoWindow({
                    content: "hello"
                });
                map.data.setStyle({
                    strokeColor: '#5ADEBF',
                    strokeWeight: 5
                });
                map.data.addListener('mouseover', function (event) {
                    map.data.revertStyle();
                    map.data.overrideStyle(event.feature, { strokeColor: '#D54AD5', strokeWeight: 8 });
                    var road_name = event.feature.getProperty('road_name');
                    var total_num_lanes = event.feature.getProperty('total_num_lanes');
                    var reduced_speed_limit = event.feature.getProperty('reduced_speed_limit');
                    var workers_present = event.feature.getProperty('workers_present');
                    var vehicle_impact = event.feature.getProperty('vehicle_impact');
                    var lanes = event.feature.getProperty('lanes');
                    var lanes_text = ''
                    for (i = 0; i < lanes.length; i++) {
                        lanes_text += '<tr><td>Lane ' + lanes[i]['lane_number'] + '(' + lanes[i]['type'] + '): </td><td>' + lanes[i]['status'] + '</td></tr>';
                    }
                    var html = '<table style="width:100%">' +
                        '<colgroup>' +
                        '<col span="1" style="width: 160px;">' +
                        '<col span="1" style="width: 138px;">' +
                        '</colgroup>' +
                        '<tbody>' +
                        '<tr><td>Road Name: </td><td>' + road_name + '</td></tr>' +
                        '<tr><td>Reduced Speed Limit:  </td><td>' + reduced_speed_limit + ' mph</td></tr>' +
                        '<tr><td>Workers Present: </td><td>' + workers_present + '</td></tr>' +
                        '<tr><td>Vehicle Impact: </td><td>' + vehicle_impact + '</td></tr>' +
                        lanes_text +
                        '</tbody>' +
                        '</table>';
                    document.getElementById("info-box").innerHTML = html
                });
            }

            var mypopup = false
            function openVisPopup() {
                //var url = 'RSZW_MapVisualizer.html'
                //var url = 'V2X_MapVisualizer.aspx'
                //console.log('openVisPopup')
                //document.getElementById('wz_visualization_iframe').setAttribute('src', url);
                // document.getElementById('wz_visualization_iframe').contentWindow.location.reload();
                // document.getElementById('WZVisualization').innerHTML = url
                // $('#WZVisualization').load(url)
                // $("#WZVisualization").load('V2X_MapVisualizer.aspx');
                // var mypopup = window.open(url, 'popup_window', 'width=1000,height=600,left=100,top=100,resizable=yes');
                //if (!mypopup) {
                //    alert('Visualization popup was blocked. Please enable popups for this site');
                //}
                //else {
                //    $('#VerificationButton').css('display', 'block');
                //}
            }
            function showContent() {
                toastr.options = {
                    "closeButton": true,
                    "debug": false,
                    "progressBar": true,
                    "preventDuplicates": false,
                    "positionClass": "toast-bottom-full-width",
                    "showDuration": "400",
                    "hideDuration": "1000",
                    "timeOut": "7000",
                    "extendedTimeOut": "1000",
                    "showEasing": "swing",
                    "hideEasing": "linear",
                    "showMethod": "fadeIn",
                    "hideMethod": "fadeOut"
                }
                var strmsg = document.getElementById("hdnParam").value;
                var errortype = document.getElementById("msgtype").value;

                if (errortype == "Success") {
                    toastr["success"](strmsg, "SUCCESS");
                }
                else if (errortype == "Error") {
                    toastr["error"](strmsg, "ERROR");
                }
                else if (errortype == "Info") {
                    toastr["info"](strmsg, "INFORMATION");
                }
                else {
                    toastr["error"](strmsg, "ERROR");
                }
            }

            var arrHead = new Array();	// array for header.
            arrHead = ['', 'Row Number', 'Marker Type', 'Marker Value'];
            arrHeadInit = ['Row Number', 'Marker Type', 'Marker Value'];

            function createTable() {
                var empTable = document.createElement('table');
                empTable.setAttribute('id', 'empTable'); // table id.

                var tr = empTable.insertRow(-1);
                for (var h = 0; h < arrHead.length; h++) {
                    var th = document.createElement('th'); // create table headers
                    th.innerHTML = arrHead[h];
                    tr.appendChild(th);
                }

                var div = document.getElementById('cont');
                div.appendChild(empTable);  // add the TABLE to the container.

                document.getElementById("addRow").addEventListener("click", addRow);
                // document.getElementById("addRow").addEventListener("click", addRow);
                // document.getElementById("bt").addEventListener("click", submitbtn);
            }

            function createInitialTable() {
                var initTable = document.createElement('table');
                initTable.setAttribute('id', 'initTable'); // table id.

                var tr = initTable.insertRow(-1);
                for (var h = 0; h < arrHeadInit.length; h++) {
                    var th = document.createElement('th'); // create table headers
                    th.innerHTML = arrHeadInit[h];
                    tr.appendChild(th);
                }

                var div = document.getElementById('contInit');
                div.appendChild(initTable);  // add the TABLE to the container.
                // document.getElementById("addRow").addEventListener("click", addRow);
                // document.getElementById("bt").addEventListener("click", submitbtn);
            }

            // delete TABLE row function.
            function removeRow(oButton) {
                var empTab = document.getElementById('empTable');
                empTab.deleteRow(oButton.parentNode.parentNode.rowIndex); // button -> td -> tr.
            }

            function addPopulateRow(row, marker, value) {
                var empTab = document.getElementById('empTable');

                var rowCnt = empTab.rows.length;   // table row count.
                var tr = empTab.insertRow(rowCnt); // the table row.
                tr = empTab.insertRow(rowCnt);

                var markerSelectList;

                var disabled = false
                if (marker == "Data Log" || marker == "RP")
                    disabled = true


                for (var c = 0; c < arrHead.length; c++) {
                    var td = document.createElement('td'); // table definition.
                    td = tr.insertCell(c);

                    if (c == 0) {      // the first column.
                        // add a button in every new row in the first column.
                        // var button = document.createElement('input');
                        //button.setAttribute('type', 'button');
                        //button.setAttribute('value', 'Remove');
                        //button.setAttribute('class', 'btnGridRemove');
                        var button = document.createElement('button');
                        button.setAttribute('type', 'submit');
                        var image = document.createElement('img');
                        image.setAttribute('src', './images/trash_can.png')
                        image.setAttribute('height', '20px')
                        button.appendChild(image)

                        // add button's 'onclick' event.
                        button.setAttribute('onclick', 'removeRow(this)');
                        if (disabled)
                            button.setAttribute('disabled', disabled)

                        td.appendChild(button);
                    }
                    else if (c == 1) {
                        var input = document.createElement("input");
                        input.id = "rowNumber";
                        input.type = "number"
                        input.min = rpRow + 1
                        input.max = numRows - 1
                        console.log('Min: ' + (rpRow + 1).toString() + ', Max: ' + (numRows - 1).toString())
                        td.appendChild(input);
                        input.value = parseInt(row)
                        if (disabled) {
                            input.setAttribute('disabled', disabled)
                            input.min = "0"
                            input.max = numRows
                        }
                    }
                    else if (c == 2) {
                        console.log(marker)
                        newarray = ["Data Log,Data Logging", "RP,Reference Point", "LC,Lane Closing", "LO,Lane Opening", "WP,Workers Present"]
                        var selectList = document.createElement("select");
                        selectList.id = "marker";
                        td.appendChild(selectList);
                        for (var i = 0; i < newarray.length; i++) {
                            var option = document.createElement("option");
                            option.setAttribute('type', 'option');
                            option.value = newarray[i].split(',')[0];
                            option.text = newarray[i].split(',')[1];
                            selectList.appendChild(option);
                        }
                        if (marker != null)
                            selectList.value = marker;
                        markerSelectList = selectList
                        if (disabled)
                            selectList.setAttribute('disabled', disabled)
                        selectList.setAttribute('onchange', 'updateMarkerValues(this)');
                    }
                    else if (c == 3) {
                        // valueList = values[marker]

                        var selectList = document.createElement("select");
                        selectList.id = "markervalue";
                        td.appendChild(selectList);

                        arr = [',', 'True, TRUE', 'False, FALSE', '1, Lane 1', '2, Lane 2', '3, Lane 3', '4, Lane 4', '5, Lane 5', '6, Lane 6', '7, Lane 7', '8, Lane 8']
                        for (var i = 0; i < arr.length; i++) {
                            var option = document.createElement("option");
                            option.setAttribute('type', 'option');
                            option.value = arr[i].split(',')[0];
                            option.text = arr[i].split(',')[1];
                            selectList.appendChild(option);
                        }
                        if (value != null)
                            selectList.value = value;
                        if (disabled)
                            selectList.setAttribute('disabled', disabled)
                    }
                    else {
                        // 2nd, 3rd and 4th column, will have textbox.

                    }
                }
                updateMarkerValues(markerSelectList)

            }

            function addRow() {
                var empTab = document.getElementById('empTable');

                var rowCnt = empTab.rows.length;
                var tr = empTab.insertRow(rowCnt);
                tr = empTab.insertRow(rowCnt);

                for (var c = 0; c < arrHead.length; c++) {
                    var td = document.createElement('td');
                    td = tr.insertCell(c);

                    if (c == 0) {
                        // add a button in every new row in the first column.
                        var button = document.createElement('input');
                        button.setAttribute('type', 'button');
                        button.setAttribute('value', 'Remove');
                        button.setAttribute('class', 'btnGridRemove');
                        button.setAttribute('onclick', 'removeRow(this)');

                        td.appendChild(button);
                    }
                    else if (c == 1) {
                        var input = document.createElement("input");
                        input.id = "rowNumber";
                        input.type = "number"
                        input.min = "0"
                        input.max = numRows
                        input.value = "1"
                        td.appendChild(input);
                    }
                    else if (c == 2) {
                        newarray = ["Data Log, Data Logging", "RP, Reference Point", "LC, Lane Closing", "LO, Lane Opening", "WP, Workers Present"]
                        var selectList = document.createElement("select");
                        selectList.id = "marker";
                        td.appendChild(selectList);
                        for (var i = 0; i < newarray.length; i++) {
                            var option = document.createElement("option");
                            option.setAttribute('type', 'option');
                            option.value = newarray[i].split(',')[0];
                            option.text = newarray[i].split(',')[1];
                            selectList.appendChild(option);
                        }
                        markerSelectList = selectList
                        selectList.setAttribute('onchange', 'updateMarkerValues(this)');
                    }
                    else if (c == 3) {
                        var selectList = document.createElement("select");
                        selectList.id = "markervalue";
                        td.appendChild(selectList);
                    }
                }
                updateMarkerValues(markerSelectList)

            }

            function updateMarkerValues(element) {
                var marker = element.value

                var lanes = [];
                var laneNames = []
                for (var i = 1; i <= numLanes; i++) {
                    lanes.push(i);
                }
                for (var i = 1; i <= 8; i++) {
                    laneNames.push("Lane " + i.toString());
                }
                var values_DL = ['True', 'False']
                var value_names_DL = ['TRUE', 'FALSE']

                var values_LO = lanes
                var value_names_LO = laneNames

                var values_LC = lanes
                var value_names_LC = laneNames

                var values_WP = ['True', 'False']
                var value_names_WP = ['TRUE', 'FALSE']

                var disabled = true
                var values = []

                if (marker == "Data Log") {
                    values = values_DL
                    valueNames = value_names_DL
                    disabled = true
                }
                else if (marker == "LO") {
                    values = values_LO
                    valueNames = value_names_LO
                    disabled = false
                }
                else if (marker == "LC") {
                    values = values_LC
                    valueNames = value_names_LC
                    disabled = false
                }
                else if (marker == "WP") {
                    values = values_WP
                    valueNames = value_names_WP
                    disabled = false
                }
                else {
                    values = []
                    valueNames = []
                    disabled = true
                }
                var tr = element.closest('tr');

                for (c = 0; c < tr.cells.length; c++) {
                    var element = tr.cells[c];
                    if (element.childNodes[0].id == 'markervalue') {
                        var value = element.childNodes[0].value;
                        for (i = element.childNodes[0].options.length - 1; i >= 0; i--) {
                            element.childNodes[0].options[i] = null;
                        }
                        for (var i = 0; i < values.length; i++) {
                            var option = document.createElement("option");
                            option.setAttribute('type', 'option');
                            option.value = values[i];
                            option.text = valueNames[i];
                            element.childNodes[0].appendChild(option);
                        }
                        if (values.indexOf(value) >= 0) element.childNodes[0].value = value

                        //if (disabled) {
                        //    element.childNodes[0].setAttribute('disabled', disabled)
                        //    element.childNodes[0].value = ""
                        //}
                        //else {
                        //    element.childNodes[0].removeAttribute('disabled')
                        //}
                    }

                }

            }

            function populateInitTable(arrValues) {
                console.log(arrValues)
                var initTable = document.getElementById('initTable');

                var rowCnt = initTable.rows.length;   // table row count.

                for (var i = 0; i < arrValues.length; i++) {
                    var tr = initTable.insertRow(i+1);
                    for (var c = 0; c < arrHeadInit.length; c++) {
                        var td = document.createElement('td'); // table definition.
                        // td = tr.insertCell(c);
                        // var th = document.createElement('th'); // create table headers
                        td.innerHTML = arrValues[i][c];
                        tr.appendChild(td)
                    }
                }
            }

            var numLanes;
            var numRows;
            var rpRow = 0;
            function fillTable() {
                if (document.contains(document.getElementById("initTable"))) document.getElementById("initTable").remove();
                createInitialTable()
                //if (document.contains(document.getElementById("empTable"))) document.getElementById("empTable").remove();
                //createTable()

                // arrValuesText = "3,64;1,Data Log,True;13,RP,;64,Data Log,False"
                //arrValuesText = "";
                //arrValuesText += "3,100;"
                //arrValuesText += "1,WP,True" // + ";"

                initialTable = []

                arrValuesText = document.getElementById('myHiddenoutputlist').value

                //console.log(arrValuesText);
                if (arrValuesText.trim() != "") {
                    arrValues = arrValuesText.split(";");
                    row = arrValues[0].split(",");
                    numLanes = parseInt(row[0])
                    numRows = parseInt(row[1])
                    arrValues = arrValues.slice(1)
                    //console.log(arrValues);
                    for (var i = 0; i < arrValues.length; i++) {
                        if (arrValues[i] == "'', ''" || arrValues[i] == "") continue;
                        row = arrValues[i].split(",");
                        if (row[1].trim().replace("'", "") == "RP")
                            rpRow = parseInt(row[0].trim().replace("'", ""));

                        initialTable.push(row)
                        // addPopulateRow(row[0].trim().replace("'", ""), row[1].trim().replace("'", ""), row[2].trim().replace("'", ""));
                    }
                    populateInitTable(initialTable)
                }
                // else addPopulateRow()
            }

            // function to extract and submit table data.
            function submitStuff() {

                //var arrValues = $('#wz_visualization_iframe').contents().find('#hiddenMarkers').val();
                var arrValues = $('#hiddenMarkers').val();
                markersList = arrValues.split(';');
                markers = [];
                for (i = 0; i < markersList.length; i++) {
                    if ((markersList[i]) != '')
                        markers.push(markersList[i].split(','))
                }

                errorMessages = validateMarkers(markers)
                if (errorMessages != '') {
                    document.getElementById("hdnParam").value = 'Marker Validation Failed: \n' + errorMessages.replaceAll('\n', '; ')
                    document.getElementById("msgtype").value = "Error"
                    showContent()

                    console.log("Markers: " + arrValues);
                    document.getElementById('hiddenMarkers').value = arrValues;

                    $('#updatePathDataButton').prop('disabled', true);
                    if (!$('#updatePathDataButton').hasClass('btnDisabled'))
                        $('#updatePathDataButton').addClass('btnDisabled');
                }
                else {
                    document.getElementById("hdnParam").value = "Markers Successfully Validated"
                    document.getElementById("msgtype").value = "Success"
                    showContent()

                    console.log("Markers: " + arrValues);
                    document.getElementById('hiddenMarkers').value = arrValues;

                    $('#updatePathDataButton').prop('disabled', false);
                    $('#updatePathDataButton').removeClass('btnDisabled');
                }

                // $('#updatePathDataButton').css('background', '#FF8500');
            }

            // Markers: [[row, marker, value],...]
            // Markers array MUST BE SORTED BY ROW NUMBER
            function validateMarkers(markers) {
                errorMessages = ''

                laneStat = [];
                wpStat = 0;
                gotRP = false;
                dataLogEnded = false;
                for (i = 0; i <= numLanes; i++)
                    laneStat.push(0)

                for (i = 0; i < markers.length; i++) {
                    currMarker = markers[i]
                    row = currMarker[0]
                    if (row == 0) {
                        if (currMarker[1] != 'Data Log' || currMarker[2] != 'True')
                            errorMessages += 'Missing Start of Data Log Marker\n'
                    }
                    else {
                        if (currMarker[1] == 'RP') {
                            gotRP = true;
                            if (currMarker[2] != '')
                                errorMessages += 'Reference Point Marker Should Have No Value. Value found: ' + currMarker[2] + '\n';
                        }
                        else if (currMarker[1] == 'LC') {
                            lane = currMarker[2]
                            if (!gotRP)
                                errorMessages += 'Marker found before reference point: ' + currMarker[1] + ' at row ' + row.toString() + '\n';
                            else if (dataLogEnded)
                                errorMessages += 'Marker found after end of data log: ' + currMarker[1] + ' at row ' + row.toString() + ' \n';

                            if (laneStat[lane] == 1)
                                errorMessages += 'Invalid Lane closure, Lane Not Open: ' + currMarker[1] + ' ' + lane + ' at row ' + row.toString() + '\n';
                            else
                                laneStat[lane] = 1
                        }
                        else if (currMarker[1] == 'LO') {
                            lane = currMarker[2]
                            if (!gotRP)
                                errorMessages += 'Marker found before reference point: ' + currMarker[1] + ' at row ' + row.toString() + '\n';
                            else if (dataLogEnded)
                                errorMessages += 'Marker found after end of data log: ' + currMarker[1] + ' at row ' + row.toString() + ' \n';

                            if (laneStat[lane] == 0)
                                errorMessages += 'Invalid Lane Opening, Lane Not Closed: ' + currMarker[1] + ' ' + lane + ' at row ' + row.toString() + '\n';
                            else
                                laneStat[lane] = 0
                        }
                        else if (currMarker[1] == 'WP') {
                            if (!gotRP)
                                errorMessages += 'Marker found before reference point: ' + currMarker[1] + ' at row ' + row.toString() + ' \n';
                            else if (dataLogEnded)
                                errorMessages += 'Marker found after end of data log: ' + currMarker[1] + ' at row ' + row.toString() + ' \n';

                            if (wpStat == 1 && currMarker[2] == 'True')
                                errorMessages += 'Invalid Worker Presence Marker, Workers Already Present: ' + currMarker[1] + ' ' + currMarker[2] + ' at row ' + row.toString() + '\n';
                            else if (wpStat == 0 && currMarker[2] == 'False')
                                errorMessages += 'Invalid Worker Presence Marker, Workers Already Not Present: ' + currMarker[1] + ' ' + currMarker[2] + ' at row ' + row.toString() + '\n';
                            else
                                wpStat = (wpStat - 1) * -1; // Turn 1 -> 0 and 0-> 1
                        }
                        else if (currMarker[1] == 'Data Log' && currMarker[2] == 'False')
                            dataLogEnded = true
                        else {
                            if (!gotRP)
                                errorMessages += 'Marker found before reference point: ' + currMarker[1] + ' at row ' + row.toString() + '\n';
                            else if (dataLogEnded)
                                errorMessages += 'Marker found after end of data log: ' + currMarker[1] + ' at row ' + row.toString() + ' \n';
                            errorMessages += 'Invalid Marker String: ' + currMarker[1] + ' found at row ' + row.toString() + '\n';
                        }
                    }
                }

                if (!gotRP)
                    errorMessages += 'Reference Point Not Found\n';
                if (!dataLogEnded)
                    errorMessages += 'Data Logging Stopped Marker Not Found\n';

                for (i = 1; i < laneStat.length; i++) {
                    if (laneStat[i] == 1) {
                        errorMessages += 'Lane Left Open at End of WZ, Lane #' + i.toString() + '\n';
                    }
                }
                if (wpStat != 0)
                    errorMessages += 'Workers Present at End of WZ\n';

                errorMessages = errorMessages.trimEnd('\n')

                return errorMessages
            }

            //fillTable()
        </script>
        <%--<script
            src="https://maps.googleapis.com/maps/api/js?key=api-key-here&callback=initMap">
        </script>--%>
    </form>
</body>
</html>
