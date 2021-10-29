<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="V2X_Upload.aspx.cs" Inherits="Neaera_Website_2018.V2X_Upload" %>

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
    <style>
        .upload {
            margin: 4px;
        }

        #uploadContainer {
            margin-left: 20%;
            font-size: 1rem;
        }

        #movingCar {
            height: 100px;
            width: 100px;
            position: relative;
            transform: rotate(90deg);
            opacity: 0;
        }

        .animateCar {
            animation-name: example;
            animation-duration: 3s;
        }
        @keyframes example {
            0%   {left:0px; top:-75px; transform: rotate(90deg); opacity: 1;}
            60%  {left:100%; top:-75px; transform: rotate(90deg); opacity: 1;}
            65%  {left:100%; top:-75px; transform: rotate(0deg); opacity: 1;}
            100%  {left:100%; top:-1000px; transform: rotate(0deg); opacity: 1;}
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
                            <h2 align="left">V2X TMC Data Collection Website </h2>
                        </div>
                    </div>
                    <div class="grid-row">
                        <div class="tablet:grid-col-8">
                            <p align="left">
                                Work Zone Data Exchange - Upload Work Zone Data
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <ul id="menu-top" class="top-nav top-navbar-nav top-navbar-right">
                <li><a href="V2x_Home.aspx">HOME</a></li>
                <li><a href="V2X_ConfigCreator.aspx">CONFIGURATION</a></li>
                <li><a href="V2X_Upload.aspx" class="menu-top-active" onclick="return false;">UPLOAD</a></li>
                <li><a href="V2X_Verification.aspx">VERIFICATION</a></li>
                <li><a href="V2X_Published.aspx">PUBLISHED</a></li>
                <li><a href="V2X_Logs.aspx">LOGGING</a></li>
            </ul>
        </div>

        <div class="form-style-2">
            <div class="grid-container">
                <h1 class="text-center">Work Zone Data Upload</h1>
                <div class="form-style-2-heading">Upload File</div>
                <div id="uploadContainer">
                    <asp:Label ID="lbl_fileupload" class="upload" runat="server">Please select a path data (CSV) file to upload</asp:Label>
                    <asp:FileUpload ID="file_uploadpath" class="upload" ClientIDMode="Static" runat="server" accept=".csv" /><br />
                    <div id="wzInfoDiv" class="upload" style="font-size: 15px;">
                        <table>
                            <tr>
                                <td>Work Zone Description: </td>
                                <td id="descriptionCell"></td>
                            </tr>
                            <tr>
                                <td>Road Name: </td>
                                <td id="roadNameCell"></td>
                            </tr>
                        </table>
                    </div>
                    <asp:Button ID="UploadButton" class="upload" runat="server" ClientIDMode="Static" Text="Upload" onClientClick="animateCar()" OnClick="UploadButton_Click" />
                    <div id="movingCar">
                        <img src="./images/random_car.png" alt="Car" width="100" height="100"/>
                    </div>
                </div>
            </div>
            <input type="hidden" id="hdnParam" runat="server" clientidmode="Static" value="This is my message" />
            <input type="hidden" id="msgtype" runat="server" clientidmode="Static" />
        </div>
        <script>
            if ($('#file_uploadpath').val().length < 1) {
                $('#UploadButton').prop('disabled', true);
                $('#UploadButton').css('background', 'gray');
                $('#UploadButton').css('cursor', '');
            }
            else {
                $('#UploadButton').prop('disabled', false);
                $('#UploadButton').css('background', '#FF8500');
                $('#UploadButton').css('cursor', 'pointer');
            }
            $('#file_uploadpath').change(function () {
                filename = $('#file_uploadpath').val().replace(/^.*[\\\/]/, '').replace('.zip', '')
                parts = filename.split('--');
                $('#descriptionCell').html(parts[1]);
                $('#roadNameCell').html(parts[2]);
                if ($('#file_uploadpath').val().length < 1) {
                    $('#UploadButton').prop('disabled', true);
                    $('#UploadButton').css('background', 'gray');
                    $('#UploadButton').css('cursor', '');
                }
                else {
                    $('#UploadButton').prop('disabled', false);
                    $('#UploadButton').css('background', '#FF8500');
                    $('#UploadButton').css('cursor', 'pointer');
                }
            });

            function animateCar() {
                $('#movingCar').addClass('animateCar')
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
    </form>
</body>
</html>
