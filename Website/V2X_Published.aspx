<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="V2X_Published.aspx.cs" Inherits="Neaera_Website_2018.V2X_Published" %>

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
    <!-- Redesign Styles -->
    <link rel="stylesheet" href="css/redesign_styles.css">
    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

    <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
    <script src="assets_v2x/js/uswds.min.js"></script>
    <script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/css/toastr.min.css" rel="stylesheet" />
    <%--<link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.3.2/css/bootstrap.min.css" rel="stylesheet" />--%>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/js/toastr.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/pretty-checkbox@3.0/dist/pretty-checkbox.min.css" rel="stylesheet" />
    <style>
        #map {
            height: 400px; /* The height is 400 pixels */
            width: 100%; /* The width is the width of the web page */
        }

        .upload {
            margin: 4px;
        }

        .partialCenter {
            margin-left: 20%;
            margin-top: 10px
        }

        #downloadChoiceDiv {
            margin-top: 10px;
        }

        .downloadChoice {
            margin-top: 10px;
        }

        .btnDisabled {
            background: grey !important;
        }

        #info-box {
            background-color: white;
            border: 1px solid black;
            font-size: 15px;
            width: 300px;
        }

        #listConfigurationFiles {
            margin-left: 20%;
            width: 400px;
        }

        #wzInfoDiv {
            margin-left: 20%;
            margin-top: 10px;
        }

        #downloadChoiceDiv {
            margin-left: 20%;
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
    </style>
</head>
<body>
    <form id="form1" method="post" runat="server">
        <div id="top-info">
            <div class="grid-container">
                <div class="hero-intro">
                    <div class="grid-row">
                        <div class="tablet:grid-col-8">
                            <h2 align="left">V2X TMC Data Collection Website</h2>
                        </div>
                    </div>
                    <div class="grid-row">
                        <div class="tablet:grid-col-8">
                            <p align="left">
                                Work Zone Data Exchange - Get Work Zone Data
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <ul id="menu-top" class="top-nav top-navbar-nav top-navbar-right">
                <li><a href="V2x_Home.aspx">HOME</a></li>
                <li><a href="V2X_ConfigCreator.aspx">CONFIGURATION</a></li>
                <li><a href="V2X_Upload.aspx">UPLOAD</a></li>
                <li><a href="V2X_Verification.aspx">VERIFICATION</a></li>
                <li><a href="V2X_Published.aspx" class="menu-top-active" onclick="return false;">PUBLISHED</a></li>
                <li><a href="V2X_Logs.aspx">LOGGING</a></li>
            </ul>
        </div>

        <div class="form-style-2">
            <div class="grid-container">
                <h1 class="text-center">Published Work Zone Data</h1>
                <div class="form-style-2-heading">Choose Work Zone to Download</div>
                <div>
                    <div>
                        <h3 style="margin-left: 20%; margin-bottom: 5px">Choose a work zone and specify messages to download</h3>
                        <asp:ListBox ID="listConfigurationFiles" AutoPostBack="True" OnSelectedIndexChanged="listConfigurationFiles_SelectedIndexChanged" runat="server"></asp:ListBox>
                    </div>
                    <div id="wzInfoDiv" class="partialCenter">
                        <asp:Table runat="server">
                            <asp:TableRow>
                                <asp:TableCell>Description: </asp:TableCell>
                                <asp:TableCell ID="tableDescriptionCell"></asp:TableCell>
                            </asp:TableRow>
                            <asp:TableRow>
                                <asp:TableCell>Road Name: </asp:TableCell>
                                <asp:TableCell ID="tableRoadNameCell"></asp:TableCell>
                            </asp:TableRow>
                            <asp:TableRow>
                                <asp:TableCell>Start Date: </asp:TableCell>
                                <asp:TableCell ID="tableStartDateCell"></asp:TableCell>
                            </asp:TableRow>
                            <asp:TableRow>
                                <asp:TableCell>End Date: </asp:TableCell>
                                <asp:TableCell ID="tableEndDateCell"></asp:TableCell>
                            </asp:TableRow>
                        </asp:Table>
                    </div>
                    <div id="downloadChoiceDiv">
                        <div class="pretty p-default p-curve p-fill downloadChoice">
                            <input type="checkbox" id="wzdx_checkbox" runat="server" onclick="checkboxClicked()" />
                            <div class="state">
                                <label>Work Zone Data Exchange message (WZDx), type = geojson</label>
                            </div>
                        </div>
                        <br />
                        <div class="pretty p-default p-curve p-fill downloadChoice">
                            <input type="checkbox" id="rsm_xml_checkbox" runat="server" onclick="checkboxClicked()" />
                            <div class="state">
                                <label>XML Roadside Safety Message (RSM), type = xml</label>
                            </div>
                        </div>
                        <br />
                        <div class="pretty p-default p-curve p-fill downloadChoice">
                            <input type="checkbox" id="rsm_uper_checkbox" runat="server" onclick="checkboxClicked()" />
                            <div class="state">
                                <label>Binary Roadside Safety Message (RSM), type = uper</label>
                            </div>
                        </div>
                        <br />
                        <asp:Button ID="DownloadButton" class="downloadChoice" runat="server" ClientIDMode="Static" Text="Download Work Zone Data" OnClick="DownloadButton_Click" /><br />
                         <asp:Button ID="DeletePublishWZButton" class="downloadChoice btnDisabled" runat="server" ClientIDMode="Static" Text="Delete Published Work Zone Data" OnClick="DeletePublishWZButton_Click" OnClientClick="return confirm('Are you sure you want to DELETE this published this work zone? This cannot be undone')" disabled/><br />
                    </div>
                    <input type="hidden" id="hdnParam" runat="server" clientidmode="Static" value="This is my message" />
                    <input type="hidden" id="msgtype" runat="server" clientidmode="Static" />
                </div>
            </div>
        </div>
        <div class="form-style-4">
            <div id="map"></div>
            <div id="info-box"></div>
            <div id="geojsonStringDiv" runat="server" style="display: none;"></div>
        </div>
        <script>
            var map;
            function initMap() {
                var boulder = { lat: 40.93977, lng: -105.185182 };
                map = new google.maps.Map(
                    document.getElementById('map'), {
                        zoom: 4,
                        center: boulder,
                        mapTypeId: google.maps.MapTypeId.HYBRID
                    }
                );
                center_display = document.getElementById('info-box')
                map.controls[google.maps.ControlPosition.TOP_CENTER].push(center_display);
                checkboxClicked();
                //initEvents();
            }
            initMap()

            function loadGeoJsonString(geoString) {
                var geojson = JSON.parse(geoString);
                map.data.addGeoJson(geojson);
                zoom(map);
                loadJsonInfo();
                //openVisPopup();
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

            function loadJsonInfo() {
                var infowindow_json = new google.maps.InfoWindow({
                    content: "hello"
                });
                //map.data.setStyle(function (feature) {
                //    var color = 'black';
                //    if (feature.getProperty('isColorful')) {
                //        color = feature.getProperty('color');
                //    }
                //    return /** @type {!google.maps.Data.StyleOptions} */({
                //        fillColor: color,
                //        strokeColor: color,
                //        strokeWeight: 2
                //    });
                //});
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
                        lanes_text += '<tr><td>Lane ' + lanes[i]['lane_number'] + '(' + lanes[i]['lane_type'] + '): </td><td>' + lanes[i]['lane_status'] + '</td></tr>';
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
            function checkboxClicked() {
                if ($('#wzdx_checkbox').prop("checked") == false && $('#rsm_xml_checkbox').prop("checked") == false && $('#rsm_uper_checkbox').prop("checked") == false) {
                    $('#DownloadButton').prop('disabled', true);
                    $('#DownloadButton').css('background', 'gray');
                    $('#DownloadButton').css('cursor', '');
                }
                else {
                    $('#DownloadButton').prop('disabled', false);
                    $('#DownloadButton').css('background', '#FF8500');
                    $('#DownloadButton').css('cursor', 'pointer');
                }
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
        </script>
        <%--<script
            src="https://maps.googleapis.com/maps/api/js?key=api-key-here&callback=initMap">
        </script>--%>
    </form>
</body>
</html>
