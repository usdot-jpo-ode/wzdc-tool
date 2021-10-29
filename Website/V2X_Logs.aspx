<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="V2X_Logs.aspx.cs" Inherits="Neaera_Website_2018.V2X_Logs" Async="True"%>

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

        .fixed_header tbody{
              display:block;
              overflow:auto;
              height:800px;
              width:100%;
        }
        .fixed_header thead tr{
            display:block;
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
                                View Log Messages
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
                <h1 class="text-center">Error Messages (past 24 Hours)</h1>
                <div>
                    <div id="wzInfoDiv" class="partialCenter" style="height: 800px; width: 100%">
                        <asp:Literal ID="logTable" runat="server" />
                    </div>
                    <input type="hidden" id="hdnParam" runat="server" clientidmode="Static" value="This is my message" />
                    <input type="hidden" id="msgtype" runat="server" clientidmode="Static" />
                </div>
            </div>
        </div>
        <script>
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
