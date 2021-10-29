<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="V2X_ConfigCreator.aspx.cs" Inherits="Neaera_Website_2018.V2X_ConfigCreator" %>

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
    <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
    <script src="assets_v2x/js/uswds.min.js"></script>
    <script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>

    <link href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/css/toastr.min.css" rel="stylesheet" />
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/js/toastr.min.js"></script>
    <style>
        /* Set the size of the div element that contains the map */
        #map {
            height: 100%; /* The height is 400 pixels */
            width: 100%; /* The width is the width of the web page */
        }

        .point {
            display: inline-block;
            border: solid;
            text-align: center;
            font-size: 15px;
        }

        #start_point {
            display: inline-block;
            background-color: #6BDF78;
            width: 300px;
        }

        #end_point {
            display: inline-block;
            background-color: #e45757;
            width: 300px;
        }

        .point_label {
            display: inline-block;
            width: 10px;
            text-align: right;
        }

        .title {
            font-size: 30px;
            margin-block-start: .2em;
            margin-block-end: .2em;
        }

        .tab-pane {
            border-style: double;
            border-color: lightgrey;
            height: 700px;
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

        #configstatus {
            border: 1px solid;
            padding: 10px;
            /*box-shadow: 5px 10px 20px blue inset;
            border-radius: 5px;*/
            width: 100%;
        }


        .calendarWrapper {
            background-color: #4CCAEF;
            padding: 10px;
            display: inline-block;
        }

        .myCalendar {
            background-color: #f2f2f2;
            width: 256px;
            height: 200px;
            border: none !important;
        }

            .myCalendar a {
                text-decoration: none;
            }

            .myCalendar .myCalendarTitle {
                font-weight: bold;
                height: 40px;
                line-height: 40px;
                background-color: blue;
                color: #ffffff;
                border: none !important;
            }

            .myCalendar th.myCalendarDayHeader {
                height: 25px;
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
    </style>

    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
    <link rel="stylesheet" href="/resources/demos/style.css">
    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    <script>
        $(function () {
            $("#tabs").tabs();
        });
    </script>
     <script type="text/javascript">
        function myconfirmbox(value) {
            var val = value;
            if (val == true)
            { 
                document.getElementById("hidden_confirmoverwrite").value = "true";
            }
            else if (val== false)
            {
                document.getElementById("hidden_confirmoverwrite").value = "false";
            }
            document.getElementById('<%= btnSaveConfirm.ClientID %>').click();
        }
     </script>
   

    <style>
        * {
            box-sizing: border-box;
        }

        /* Create three equal columns that floats next to each other */
        .column {
            float: left !important;
            width: 40% !important;
            padding: 5px !important;
            margin-left: 10px;
        }

        .column_tab2 {
            float: left !important;
            width: 30% !important;
            padding: 5px !important;
            margin-left: 10px;
        }

        .column_tab2_narrow {
            float: left !important;
            width: 23% !important;
            padding: 5px !important;
            margin-left: 10px;
        }

        .column_tab3 {
            float: left !important;
            width: 23% !important;
            padding: 5px !important;
            margin-left: 10px;
        }
        /* Clear floats after the columns */
        .row:after {
            content: "";
            display: table;
            clear: both;
        }

        .btnGridRemove {
            background-color: white !important;
            color: blue !important;
        }
    </style>


</head>
<body>
    <form id="form1" runat="server">
        <div id="top-info">
            <div class="grid-container">
                <div class="hero-intro">
                    <div class="grid-row">
                        <div class="tablet:grid-col-8" style="box-sizing: content-box;">
                            <h2 align="left">V2X TMC Data Collection Website </h2>
                        </div>
                    </div>
                    <div class="grid-row">
                        <div class="tablet:grid-col-8">
                            <p align="left">
                                Work Zone Data Exchange - Enter Information
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <ul id="menu-top" class="top-nav top-navbar-nav top-navbar-right">
                <li><a href="V2x_Home.aspx">HOME</a></li>
                <li><a href="V2X_ConfigCreator.aspx" class="menu-top-active" onclick="return false;">CONFIGURATION</a></li>
                <li><a href="V2X_Upload.aspx">UPLOAD</a></li>
                <li><a href="V2X_Verification.aspx">VERIFICATION</a></li>
                <li><a href="V2X_Published.aspx">PUBLISHED</a></li>
                <li><a href="V2X_Logs.aspx">LOGGING</a></li>
            </ul>
        </div>
        <div class="form-style-2">
            <div class="grid-container">
                <h1 class="text-center">Work Zone Configuration V1.0</h1>
                <div id="Tabs" role="tabpanel">
                    <ul class="nav nav-tabs nav-tabs-alt" id="myTab" role="tablist">

                        <li class="nav-item">
                            <a class="nav-link active" id="home-tab" data_id="1" data-toggle="tab" href="#home" role="tab" aria-controls="home" aria-selected="false">Configuration File</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" id="profile-tab" data_id="2" data-toggle="tab" href="#profile" role="tab" aria-controls="profile" aria-selected="false">Configuration Data</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" id="contact-tab" data_id="3" data-toggle="tab" href="#contact" role="tab" aria-controls="contact" aria-selected="false">Map Location</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" id="submit-tab" data_id="4" data-toggle="tab" href="#submitoptions" role="tab" aria-controls="submitoptions" aria-selected="true">Additional Information</a>
                        </li>

                        <li class="nav-item">
                            <a class="nav-link" id="lane-tab" data_id="5" data-toggle="tab" href="#laneoptions" role="tab" aria-controls="laneoptions" aria-selected="false">Lane Options</a>
                        </li>
                         <li class="nav-item">
                            <a class="nav-link" id="metadata-tab" data_id="6" data-toggle="tab" href="#metadata" role="tab" aria-controls="metadata" aria-selected="false">Metadata</a>
                        </li>
                        <li class="nav-item">
                            <div id="configstatus">
                                <asp:TextBox BackColor="Transparent" BorderStyle="None" Width="1000px" Font-Bold="true" runat="server" Text="Config status : Empty File (not saved or loaded configuration file)" ID="txtConfigType"></asp:TextBox>
                            </div>
                        </li>
                    </ul>
                    <div class="tab-content" id="myTabContent" style="overflow: no-display;">
                        <%--**********************begin - tab 1***********************--%>
                        <div class="tab-pane fade show active" id="home" role="tabpanel" aria-labelledby="home-tab">
                            <div class="form-style-2-heading" style="margin-top: 15px;">Create a new configuration file</div>
                            <label>
                                <span style="display: inline;">Work Zone Description</span>
                                <asp:TextBox CssClass="input-field" Text="" ID="txt_workzonedescription" MaxLength="20" onchange="javascript:update_filename();" runat="server"> </asp:TextBox>
                            </label>
                            <label>
                                <asp:Label Text="Road Name" runat="server" Style="padding-left: 7%;"></asp:Label>
                                <input type="text" class="input-field" name="field1" value="" id="txtRoadName" maxlength="20" onchange="javascript:update_filename();" runat="server" />
                            </label>
                            <label>
                                <asp:Label Text="Road #" runat="server" Style="padding-left: 11%;"></asp:Label>
                                <input type="text" class="input-field" name="field1" value="" id="txtRoadNumber" runat="server" style="width: 50px;" />
                            </label>
                            <div>
                                <asp:Label ID="lbl_filesave" runat="server" Text="File Name (auto generated - WZ description + Road Name.json) : " CssClass="input-field"></asp:Label>
                                <asp:TextBox ID="txtFilepath_configSave" runat="server" Text="" Width="400px"></asp:TextBox>
                            </div>
                            <div class="form-style-2-heading" style="margin-top: 30px">Import a configuration file</div>
                            <div class="row">
                                <div class="column">
                                    Select an existing configuration file:
                                       <asp:ListBox ID="listConfigurationFiles" runat="server" Style="width: 75%; margin-top: 5px; height: 350px; margin-left: 10px;" onchange="clearSelected('listPublishedConfigurationFiles')" OnSelectedIndexChanged="listConfigurationFiles_SelectedIndexChanged"></asp:ListBox>
                                </div>
                                <div class="column" style="width: 15% !important;">
                                    <div class="row">
                                        <asp:Button ID="btnImportConfig" runat="server" Text="Import" Style="margin-left: 8%;" OnClick="btnImportConfig_Click"/>
                                    </div>
                                    <%--<div class="row">
                                        <asp:button id="btndownloadfile_tab1" runat="server" text="downloadfile" onclick="btndownloadfile_click"/>
                                    </div>--%>
                                </div>
                                <div class="column">
                                    <asp:Label Text="Select a published configuration file:" runat="server" Style="padding-bottom: 5%">  </asp:Label>
                                    <asp:ListBox ID="listPublishedConfigurationFiles" runat="server" Style="margin-top: 5px; height: 350px; width: 75%;" onchange="clearSelected('listConfigurationFiles')" OnSelectedIndexChanged="listPublishedConfigurationFiles_SelectedIndexChanged"></asp:ListBox>
                                </div>
                            </div>
                            <div class="navBtnContianer">
                                <input id="Next_tab1" type="button" value="Next >" class="btn btn-primary nextBtn" style="margin-left: 50px; margin-right: 25px; float: right;" onclick="doTab('Next')" />
                            </div>
                        </div>
                        <%--*********************end - tab 1**************************--%>
                        <%--**********************begin - tab 2***********************--%>
                        <div class="tab-pane fade" id="profile" role="tabpanel" aria-labelledby="profile-tab">
                            <%--<h1 class="text-center">Work Zone Information</h1>--%>
                            <div class="form-style-4">
                                <div class="grid-container">
                                    <div class="row">
                                        <div class="column_tab2">
                                            <div class="form-style-4-heading">Lane Information</div>
                                            <label for="field1"><span>Number of Lanes (1-8)<span class="required">*</span></span><asp:DropDownList ID="dd_numberoflanes" CssClass="ddfieldsize" runat="server" onchange="initLaneType()"></asp:DropDownList></label>
                                            <label for="field4"><span>Vehicle Path Data Lane (1-8)<span class="required">*</span></span><asp:DropDownList ID="dd_avgvehicledatapath" CssClass="ddfieldsize" runat="server"></asp:DropDownList></label>
                                            <%--add label - Left lane is lane 1--%>
                                            <label for="field1">
                                                <span>Avg Lane Width(m)<span class="required">*</span></span><asp:TextBox ID="AvgLaneWidth" CssClass="speedconfig" onkeypress="return validateFloatKeyPress(this,event);" Style="width: 50px; margin-top: 10px;" runat="server"></asp:TextBox>

                                            </label>


                                            <label for="field1">
                                                <span>Approach Lane Padding(m):<span class="required">*</span></span>
                                                <asp:TextBox ID="AppLanePadding" CssClass="speedconfig" Style="width: 50px; margin-top: 10px;" onkeypress="return validateFloatKeyPress(this,event);" runat="server"></asp:TextBox></label>

                                            <label for="field1">
                                                <span>WorkZone Lane Padding(m):<span class="required">*</span></span>
                                                <asp:TextBox ID="WorkZoneLanePadding" CssClass="speedconfig" Style="width: 50px; margin-top: 10px;" onkeypress="return validateFloatKeyPress(this,event);" runat="server"></asp:TextBox></label>

                                        </div>
                                        <div class="column_tab2">
                                            <div class="form-style-4-heading">Speed Limits (5-90 mph)</div>
                                            <label for="field1"><span>Normal Speed<span class="required">*</span></span><asp:DropDownList ID="dd_normalspeed" CssClass="ddfieldsize" runat="server"></asp:DropDownList></label>
                                            <label for="field4"><span>At the Ref. Point(start of WZ)<span class="required">*</span></span><asp:DropDownList ID="dd_AtreferencePoint" CssClass="ddfieldsize" runat="server"></asp:DropDownList></label>
                                            <label for="field1"><span>When Workers are Present<span class="required">*</span></span><asp:DropDownList ID="dd_WhenWorkersArePresent" CssClass="ddfieldsize" runat="server"></asp:DropDownList></label>
                                        </div>
                                        <div class="column_tab2">
                                            <div class="form-style-4-heading">Work Zone Type</div>
                                            <label for="field1">
                                                <span>Cause Code* <span class="required">*</span></span>
                                                <asp:TextBox class="input-field" ID="txtCauseCode" onkeypress="return validateFloatKeyPress(this,event);" Text="" runat="server" /></label>
                                            <label for="field4">
                                                <span>SubCause Code</span><asp:TextBox class="input-field" onkeypress="return validateFloatKeyPress(this,event);" ID="txtsubcausecode" Text="" runat="server" />
                                            </label>
                                        </div>
                                    </div>

                                </div>
                            </div>
                            <div class="form-style-4">
                                <div class="grid-container" style="margin-top: -40px;">
                                    <div class="row">
                                        <asp:ScriptManager ID="ScriptManager1" runat="server"></asp:ScriptManager>
                                        <div class="column_tab2">
                                            <div class="form-style-4-heading">Start Date</div>
                                            <p>
                                                <asp:UpdatePanel ID="UpdatePanel1" runat="server">
                                                    <ContentTemplate>
                                                        <asp:Calendar ID="Calendar_BeginDate" runat="server" DayNameFormat="FirstLetter" Font-Names="Tahoma" Font-Size="14px" NextMonthText=">" PrevMonthText="<" SelectMonthText="»" SelectWeekText="›" CssClass="myCalendar" CellPadding="0">
                                                            <OtherMonthDayStyle ForeColor="#b0b0b0" />
                                                            <DayStyle CssClass="myCalendarDay" ForeColor="#2d3338" />
                                                            <DayHeaderStyle CssClass="myCalendarDayHeader" ForeColor="#2d3338" />
                                                            <SelectedDayStyle Font-Bold="True" Font-Size="12px" CssClass="myCalendarSelector" />
                                                            <TodayDayStyle CssClass="myCalendarToday" />
                                                            <SelectorStyle CssClass="myCalendarSelector" />
                                                            <NextPrevStyle CssClass="myCalendarNextPrev" ForeColor="White" />
                                                            <TitleStyle CssClass="myCalendarTitle" />
                                                        </asp:Calendar>
                                                    </ContentTemplate>
                                                </asp:UpdatePanel>
                                            </p>
                                            <div class="form-style-4-heading">Start Time(HH:MM:SS) Sample:11:22 or 13:22"</div>
                                            <article>
                                                <div class="demo">
                                                    <p>
                                                        <input id="TimeBegin" type="text" class="time" runat="server" onkeypress="return formatTime(this,event)" maxlength="8" />
                                                    </p>
                                                </div>
                                            </article>
                                        </div>
                                        <div class="column_tab2">
                                            <div class="form-style-4-heading">Days of week</div>
                                            <asp:CheckBoxList ID="chkDaysOfWeek" runat="server" RepeatDirection="Horizontal" TextAlign="Left">
                                                <asp:ListItem Selected="False">Sun</asp:ListItem>
                                                <asp:ListItem Selected="False">Mon</asp:ListItem>
                                                <asp:ListItem Selected="False">Tues</asp:ListItem>
                                                <asp:ListItem Selected="False">Wed</asp:ListItem>
                                                <asp:ListItem Selected="False">Thurs</asp:ListItem>
                                                <asp:ListItem Selected="False">Fri</asp:ListItem>
                                                <asp:ListItem Selected="False">Sat</asp:ListItem>
                                            </asp:CheckBoxList>
                                        </div>
                                        <div class="column_tab2">
                                            <div class="form-style-2-heading">End Date</div>
                                            <p>

                                                <asp:UpdatePanel ID="UpdatePanel2" runat="server">
                                                    <ContentTemplate>
                                                        <asp:Calendar ID="Calendar_enddate" runat="server" DayNameFormat="FirstLetter" Font-Names="Tahoma" Font-Size="14px" NextMonthText=">" PrevMonthText="<" SelectMonthText="»" SelectWeekText="›" CssClass="myCalendar" CellPadding="0">
                                                            <OtherMonthDayStyle ForeColor="#b0b0b0" />
                                                            <DayStyle CssClass="myCalendarDay" ForeColor="#2d3338" />
                                                            <DayHeaderStyle CssClass="myCalendarDayHeader" ForeColor="#2d3338" />
                                                            <SelectedDayStyle Font-Bold="True" Font-Size="12px" CssClass="myCalendarSelector" />
                                                            <TodayDayStyle CssClass="myCalendarToday" />
                                                            <SelectorStyle CssClass="myCalendarSelector" />
                                                            <NextPrevStyle CssClass="myCalendarNextPrev" ForeColor="White" />
                                                            <TitleStyle CssClass="myCalendarTitle" />
                                                        </asp:Calendar>
                                                    </ContentTemplate>
                                                </asp:UpdatePanel>

                                            </p>
                                            <div class="form-style-2-heading">End Time(HH:MM:SS) Sample:11:22 or 13:22"</div>
                                            <p>
                                                <input id="TimeEnd" type="text" class="time" runat="server" onkeypress="return formatTime(this,event)" maxlength="8" />
                                            </p>
                                        </div>
                                        <div class="column_tab2" style="float: right;">
                                        </div>
                                    </div>

                                </div>
                            </div>
                            <div class="navBtnContianer">
                                <input id="Previous_Tab2" type="button" value="< Previous" class="btn btn-primary prevBtn" onclick="doTab('Previous')" />
                                <input id="Next_tab2" type="button" value="Next >" class="btn btn-primary nextBtn" style="float: right;" onclick="doTab('Next')" />
                            </div>
                        </div>
                        <%--*********************end - tab 2**************************--%>
                        <%--**********************begin - tab 3***********************--%>
                        <div class="tab-pane fade" id="contact" role="tabpanel" aria-labelledby="contact-tab">
                            <div id="mapbuilder" class="form-style-4" runat="server" style="height: 600px">
                                <div class="form-style-4-heading">Location Information</div>
                                <div id="mapControlsDiv">
                                    <button type="button" onclick="clear_markers()" style="font-size: 16px">Clear Markers</button>
                                    <input id="pac-input" class="controls" type="text" placeholder="Search Box" style="width: 500px; margin-left: 20px; font-size: 15px;" />
                                </div>
                                <div id="map"></div>
                                <asp:TextBox ID="start_lat_hidden" runat="server" Style="display: none"></asp:TextBox>
                                <asp:TextBox ID="start_lng_hidden" runat="server" Style="display: none"></asp:TextBox>
                                <asp:TextBox ID="end_lat_hidden" runat="server" Style="display: none"></asp:TextBox>
                                <asp:TextBox ID="end_lng_hidden" runat="server" Style="display: none"></asp:TextBox>
                                <div id="container">
                                    <div class="grid-container" style="display: none;">
                                        <div id="start_point" class="point">
                                            <p class="title">Starting Point</p>
                                            <label for="lat" class="point_label">Lat: </label>
                                            <input type="text" name="lat" id="start_lat" disabled="disabled" runat="server" />
                                            <label for="long" class="point_label">Long: </label>
                                            <input type="text" name="long" id="start_lng" disabled="disabled" runat="server" />
                                        </div>
                                        <div id="end_point" class="point">
                                            <p class="title">Ending Point</p>
                                            <label for="lat" class="point_label">Lat: </label>
                                            <input type="text" name="lat" id="end_lat" disabled="disabled" runat="server" /><br />
                                            <label for="long" class="point_label">Long: </label>
                                            <input type="text" name="long" id="end_lng" disabled="disabled" runat="server" /><br />
                                        </div>
                                    </div>

                                </div>
                            </div>
                            <div class="navBtnContianer">
                                <input id="Previous_Tab3" type="button" value="< Previous" class="btn btn-primary prevBtn" onclick="doTab('Previous')" />
                                <input id="Next_tab3" type="button" value="Next >" class="btn btn-primary nextBtn" style="float: right;" onclick="doTab('Next')" />
                            </div>
                        </div>
                        <%--*********************end - tab 3 **************************--%>

                        <%--**********************begin - tab 4***********************--%>
                        <div class="tab-pane fade" id="submitoptions" role="tabpanel" aria-labelledby="submit-tab" style="overflow: auto; overflow-x: hidden; overflow-y: auto;">
                            <div class="form-style-4">
                                <div class="grid-container">
                                    <div class="row">
                                        <div>
                                            <label for="field1"><span>Beginning Cross Street</span><asp:TextBox class="input-field" ID="txtBeginningCrossStreet" MaxLength="500" Text="" runat="server" Width="700px" /></label>
                                            <label for="field1"><span>Ending Cross Street</span><asp:TextBox class="input-field" ID="txtEndingCrossStreet" MaxLength="500" Text="" runat="server" Width="700px" /></label>
                                        </div>

                                        <div class="column_tab2">
                                            <label for="field1">
                                                <span style="margin-left: -5%;">Begin Mile Post</span>
                                                <asp:TextBox class="input-field" ID="txtBeginMilePost" onkeypress="return validateFloatKeyPress(this,event);" Text="" runat="server" Style="width: 100px; margin-left: -10px" /></label>
                                        </div>
                                        <div class="column_tab2">
                                            <label for="field1">
                                                <span>End Mile Post</span>
                                                <asp:TextBox class="input-field" ID="txtEndMilePost" onkeypress="return validateFloatKeyPress(this,event);" Text="" runat="server" Style="width: 100px; margin-left: -90px" /></label>
                                        </div>

                                    </div>
                                    <div class="row">
                                        <%--<div class="form-style-4-heading">Event Status</div>--%>
                                        <label for="field1">
                                            <span>Event Status</span></label>
                                        <div class="column_tab2">
                                            <asp:CheckBoxList ID="chEventStatus" runat="server" RepeatDirection="Horizontal" TextAlign="Right" CellSpacing="20" Width="500" RepeatLayout="Table" CssClass="checkboxlist_nowrap">
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="False">Planned</asp:ListItem>
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="False">Pending</asp:ListItem>
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="False">Active</asp:ListItem>
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="False">Cancelled</asp:ListItem>
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="False">Completed</asp:ListItem>
                                            </asp:CheckBoxList>
                                        </div>
                                    </div>

                                    <div class="row">
                                        <label for="field1"><span>Direction</span></label>
                                        <div class="column_tab2">
                                            <asp:CheckBoxList ID="chDirection" runat="server" RepeatDirection="Horizontal" TextAlign="Right" CellSpacing="20" Width="500" RepeatLayout="Table" CssClass="checkboxlist_nowrap">
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="False">Northbound</asp:ListItem>
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="False">Eastbound</asp:ListItem>
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="False">Southbound</asp:ListItem>
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="False">Westbound</asp:ListItem>
                                            </asp:CheckBoxList>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="column_tab2_narrow">
                                            <label for="field1"><span style="padding-bottom: 10px; margin-left: -20px;">Beginning Accuracy</span></label>
                                            <asp:CheckBoxList ID="chkBeginningAccuracy" runat="server" RepeatDirection="Vertical" TextAlign="Right" CellSpacing="20" Width="500" RepeatLayout="Table" CssClass="checkboxlist_nowrap">
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="True">Estimated</asp:ListItem>
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="False">Verified</asp:ListItem>
                                            </asp:CheckBoxList>
                                        </div>
                                        <div class="column_tab3">
                                            <label for="field1"><span style="padding-bottom: 10px; margin-left: -20px;">Ending Accuracy</span></label>
                                            <asp:CheckBoxList ID="chkEndingAccuracy" runat="server" RepeatDirection="Vertical" TextAlign="Right" CellSpacing="20" Width="500" RepeatLayout="Table" CssClass="checkboxlist_nowrap">
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="True">Estimated</asp:ListItem>
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="False">Verified</asp:ListItem>
                                            </asp:CheckBoxList>
                                        </div>
                                        <div class="column_tab3">
                                            <label for="field1"><span style="padding-bottom: 10px; margin-left: -20px;">Start Date Accuracy</span></label>
                                            <asp:CheckBoxList ID="chkStartDateAccuracy" runat="server" RepeatDirection="Vertical" TextAlign="Right" CellSpacing="20" Width="500" RepeatLayout="Table" CssClass="checkboxlist_nowrap">
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="True">Estimated</asp:ListItem>
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="False">Verified</asp:ListItem>
                                            </asp:CheckBoxList>
                                        </div>
                                        <div class="column_tab3">
                                            <label for="field1"><span style="padding-bottom: 10px; margin-left: -20px;">End Date Accuracy</span></label>
                                            <asp:CheckBoxList ID="chkEndDateAccuracy" runat="server" RepeatDirection="Vertical" TextAlign="Right" CellSpacing="20" RepeatLayout="Table" CssClass="checkboxlist_nowrap">
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="True">Estimated</asp:ListItem>
                                                <asp:ListItem onclick="MutExChkList(this);" Selected="False">Verified</asp:ListItem>
                                            </asp:CheckBoxList>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div>
                                            <div class="column">
                                                <div class="form-style-2-heading" style="margin-top: 15px; margin-left: -10%; width: 500px;">Work Types - Add a single work type or multiple</div>
                                                <div>
                                                    <input type="button" id="addRow" value="Add a type of work" />
                                                </div>

                                                <div id="cont" style="margin-left: 80%; width: 800px; margin-top: -13%;"></div>
                                                <!-- the container to add the TABLE -->
                                                <p>
                                                    <input type="button" id="bt" value="Submit Data" hidden="hidden" />
                                                </p>

                                                <p id='output' runat="server" hidden="hidden">
                                                </p>
                                                <asp:HiddenField runat="server" ID="myHiddenoutputlist" />
                                                <div hidden="hidden">
                                                    <asp:DropDownList ID="ddTypeOfWork" runat="server"></asp:DropDownList>
                                                </div>

                                            </div>
                                        </div>

                                    </div>
                                    <div class="navBtnContianer">
                                        <input id="Previous_Tab4" type="button" value="< Previous" class="btn btn-primary prevBtn" onclick="doTab('Previous')" />
                                         <input id="Next_tab4" type="button" value="Next >" class="btn btn-primary nextBtnAddInfo" style="float: right;" onclick="doTab('Next')" />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <%--*********************end - tab 4 **************************--%>
                        <%--**********************begin - tab 5***********************--%>
                        <div class="tab-pane fade" id="laneoptions" role="tabpanel" aria-labelledby="lane-tab" style="overflow: auto; overflow-x: hidden; overflow-y: auto;">
                            <div class="form-style-4">
                                <div class="grid-container">
                                    <div class="row">
                                        <div>
                                            <div class="column">
                                                <div class="form-style-2-heading" style="margin-top: 15px; margin-left: -10%; width: 500px;">Lane Restrictions</div>
                                                <div>
                                                    <input type="button" id="addRow_LaneRestriction" value="Add a Lane Restriction" />
                                                </div>

                                                <div id="cont_LaneRestriction" style="margin-left: 80%; width: 800px; margin-top: -13%;"></div>
                                                <!-- the container to add the TABLE -->
                                                <p>
                                                    <input type="button" id="bt_LaneRestriction" value="Submit Data" hidden="hidden" />
                                                </p>

                                                <p id='P1' runat="server" hidden="hidden">
                                                </p>
                                                <asp:HiddenField runat="server" ID="Hidden_list_LaneRestriction" />
                                                <div hidden="hidden">
                                                    <asp:DropDownList ID="ddRestrictionTypes" runat="server"></asp:DropDownList>
                                                    <asp:DropDownList ID="ddRestrictionUnits" runat="server"></asp:DropDownList>
                                                    <asp:DropDownList ID="ddNumberofLanes" runat="server"></asp:DropDownList>
                                                    
                                                </div>

                                            </div>
                                        </div>

                                    </div>
                                    <div class="row">
                                        <div>
                                            <div class="column">
                                                <div class="form-style-2-heading" style="margin-top: 30px; margin-left: -10%; width: 500px;">Lane Types</div>
                                                <div id="cont_LaneType" style="margin-left: 80%; width: 800px; margin-top: -13%;"></div>
                                                <p>
                                                    <input type="button" id="bt_LaneType" value="Submit Data" hidden="hidden" />
                                                </p>

                                                <p id='P2' runat="server" hidden="hidden">
                                                </p>
                                                <asp:HiddenField runat="server" ID="HiddenLaneType" />
                                                <div hidden="hidden">
                                                    <asp:DropDownList ID="ddLaneTypes" runat="server"></asp:DropDownList>
                                                </div>

                                            </div>
                                        </div>

                                    </div>

                                    <div class="navBtnContianer">
                                        <input id="Previous_Tab5" type="button" value="< Previous" class="btn btn-primary prevBtn" onclick="doTab('Previous')" />
                                        <input id="Next_tab" type="button" value="Next >" class="btn btn-primary nextBtnAddInfo" style="float: right;" onclick="doTab('Next')" />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <%--**********************end - tab 5**********************--%>

                        <%--**********************begin - tab 6***********************--%>
                        <div class="tab-pane fade" id="metadata" role="tabpanel" aria-labelledby="lane-tab" style="overflow: auto; overflow-x: hidden; overflow-y: auto;">
                            <div class="form-style-4">
                                <div class="grid-container">
                                    <div class="row">
                                        <div>
                                            <div class="column">
                                                <div class="form-style-2-heading" style="margin-top: 15px; margin-left: -10%; width: 500px;">Metadata</div>
                                                <label for="field1"><span>Issuing Organization<span class="required">*</span></span><asp:TextBox class="input-field" ID="txtIssuingOrganization" MaxLength="500" Text="" runat="server" Width="700px" /></label>
                                                <label for="field1">
                                                    <span>WZ Location Method</span></label>
                                                <div class="column_tab2">
                                                    <asp:CheckBoxList ID="ck_WZLocationmethod" runat="server" RepeatDirection="Horizontal" TextAlign="Right" CellSpacing="20" Width="800" RepeatLayout="Table" CssClass="checkboxlist_nowrap" Enabled ="false">
                                                        <asp:ListItem onclick="MutExChkList(this);"  Value ="channeldevicemethod" Selected="True">channel-device-method</asp:ListItem>
                                                        <asp:ListItem onclick="MutExChkList(this);" Value="signmethod" Selected="False">sign-method</asp:ListItem>
                                                        <asp:ListItem onclick="MutExChkList(this);" Value="junctionmethod" Selected="False">junction-method</asp:ListItem>
                                                        <asp:ListItem onclick="MutExChkList(this);" Value="unknown" Selected="False">unknown</asp:ListItem>
                                                        <asp:ListItem onclick="MutExChkList(this);" Value="other" Selected="False">other</asp:ListItem>
                                                    </asp:CheckBoxList>
                                                </div>
                                                <label for="field1"><span>Linear Referencing Type</span><asp:TextBox class="input-field" ID="txtIrsType" MaxLength="500" Text="" runat="server" Width="700px" /></label>
                                                <label for="field1"><span>Location Verify Method</span><asp:TextBox class="input-field" ID="txtLocationVerifyMethod" MaxLength="500" Text="" runat="server" Width="700px" /></label>
                                                <label for="field1"><span style="width: 250px">Data Feed Update Frequency (s)</span><asp:TextBox class="input-field" ID="txtDataFeedFrequencyMethod" MaxLength="500" Text="" runat="server" Width="700px" onkeypress="return isNumberKey(event)"/></label>
                                                <label for="field1"><span>Contact Name<span class="required">*</span></span><asp:TextBox class="input-field" ID="txtContactName" MaxLength="500" Text="" runat="server" Width="700px" /></label>
                                                <label for="field1"><span>Contact Email<span class="required">*</span></span><asp:TextBox class="input-field" ID="txtContactEmail" MaxLength="500" Text="" runat="server" Width="700px" /></label>
                                            </div>
                                        </div>

                                    </div>
                                  
                                    <div class="navBtnContianer">
                                        <input id="Previous_Tab6" type="button" value="< Previous" class="btn btn-primary prevBtn" onclick="doTab('Previous')" />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <%--**********************end - tab 6**********************--%>

                        <div style="margin-left: 30%;">
                            <input type="hidden" id="hdnParam" runat="server" clientidmode="Static" value="This is my message" />
                            <input type="hidden" id="msgtype" runat="server" clientidmode="Static" />
                            <input type="hidden" id="hidden_confirmoverwrite" runat="server" clientidmode="Static" />
                            <asp:Button ID="btnSave" runat="server" Text="Save" OnClick="btnSave_Click1" ForeColor="black" OnClientClick="javascript:check_requiredfields()" />
                            <asp:Button ID="btnSaveConfirm" runat="server" Text="Save"  OnClick="btnSaveConfirm_Click1" ForeColor="black" style="display:none"   />
                            <asp:Button ID="btnPublishFile" runat="server" Text="Publish" OnClick="btnPublishFile_Click" ForeColor="Gray" />
                            <asp:Button ID="btnDownloadFile" runat="server" Text="DownloadFile" Enabled="false" OnClick="btnDownloadFile_Click" ForeColor="Gray" />
                            <asp:Button ID="btnClearFields" runat="server" Text="Clear Fields" Enabled="true" OnClick="btnClearFields_Click" ForeColor="White" />
                            <asp:TextBox ID="txtRequiredFields_Valid" runat="server" Style="display: none"></asp:TextBox>
                            <asp:TextBox ID="txtRequiredFields_Text" runat="server" Style="display: none"></asp:TextBox>
                        </div>
                    </div>

                </div>
                <%--Div grid-container--%>
            </div>
            <%--Div form-style-2--%>

            <%--************ files for tab control and forward and back buttons **********************************--%>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
            <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
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

                function isNumberKey(evt) {
                    var charCode = (evt.which) ? evt.which : evt.keyCode;
                    if (charCode > 31 && (charCode < 48 || charCode > 57))
                        return false;
                    return true;
                }
            </script>
            <%--************END files for tab control and forward and back buttons **********************************--%>
            <script>
                var map
                var startEndMarkers = []
                function initMap() {
                    // The location of Uluru
                    var boulder = { lat: 40.472939, lng: -104.969202 };
                    // The map, centered at Uluru
                    map = new google.maps.Map(
                        document.getElementById('map'), { zoom: 10, center: boulder }
                    );

                    //center_display = document.getElementById('container')
                    //map.controls[google.maps.ControlPosition.TOP_CENTER].push(center_display);

                    google.maps.event.addListener(map, 'click', function (event) {
                        if (event.placeId != null) return
                        var order = ''
                        if (startEndMarkers.length == 0) {
                            order = 'Start Location'
                            document.getElementById('start_lat').value = event.latLng.lat()
                            $('#start_lat_hidden').val(event.latLng.lat())
                            document.getElementById('start_lng').value = event.latLng.lng()
                            $('#start_lng_hidden').val(event.latLng.lng())
                        }
                        else if (startEndMarkers.length == 1) {
                            order = 'End Location'
                            document.getElementById('end_lat').value = event.latLng.lat()
                            $('#end_lat_hidden').val(event.latLng.lat())
                            document.getElementById('end_lng').value = event.latLng.lng()
                            $('#end_lng_hidden').val(event.latLng.lng())
                        }
                        else {
                            return
                        }
                        var url_string = "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
                        if (order == 'Start Location') {
                            url_string = "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
                        }
                        var marker = new google.maps.Marker({
                            position: event.latLng,
                            map: map,
                            icon: {
                                url: url_string
                            },
                            draggable: true
                        });
                        startEndMarkers.push(marker)
                        var infowindow = new google.maps.InfoWindow({
                            content: order
                        });
                        marker.addListener('click', function () {
                            infowindow.open(map, marker);
                        });
                        // #infowindow.open(map, marker);
                        google.maps.event.addListener(marker, 'drag', function () {
                            order = infowindow.getContent()
                            if (order == 'Start Location') {
                                document.getElementById('start_lat').value = marker.getPosition().lat()
                                $('#start_lat_hidden').val(marker.getPosition().lat())
                                document.getElementById('start_lng').value = marker.getPosition().lng()
                                $('#start_lng_hidden').val(marker.getPosition().lng())
                            }
                            else {
                                document.getElementById('end_lat').value = marker.getPosition().lat()
                                $('#end_lat_hidden').val(marker.getPosition().lat())
                                document.getElementById('end_lng').value = marker.getPosition().lng()
                                $('#end_lng_hidden').val(marker.getPosition().lng())
                            }
                        });
                    });
                    initAutocomplete();
                    //updateMarkers();
                }
                initMap()

                function clearSelected(id) {
                    var elements = document.getElementById(id).options;

                    for (var i = 0; i < elements.length; i++) {
                        elements[i].selected = false;
                    }
                }

                function updateMarkers() {
                    startEndMarkers = []
                    start_lat = document.getElementById('<%=start_lat_hidden.ClientID%>').value
                    start_lng = document.getElementById('<%=start_lng_hidden.ClientID%>').value
                    end_lat = document.getElementById('<%=end_lat_hidden.ClientID%>').value
                    end_lng = document.getElementById('<%=end_lng_hidden.ClientID%>').value
                    if (start_lat != 0 && start_lng != 0 && end_lat != 0 && end_lng != 0) {
                        //var position_start = { lat: $('#start_lat_hidden').val(), lng: $('#start_lng_hidden').val() };
                        //var position_end = { lat: $('#end_lat_hidden').val(), lng: $('#end_lng_hidden').val() };
                        var position_start = new google.maps.LatLng(start_lat, start_lng)
                        var position_end = new google.maps.LatLng(end_lat, end_lng)

                        document.getElementById('start_lat').value = start_lat
                        document.getElementById('start_lng').value = start_lng
                        document.getElementById('end_lat').value = end_lat
                        document.getElementById('end_lng').value = end_lng

                        //map = document.getElementById("map");
                        //document.getElementById('start_lat').value = '12345678'
                        var order = 'Start Location'
                        var url_string = "http://maps.google.com/mapfiles/ms/icons/green-dot.png";
                        var marker = new google.maps.Marker({
                            position: position_start,
                            map: map,
                            icon: {
                                url: url_string
                            },
                            draggable: true
                        });
                        startEndMarkers.push(marker)
                        var infowindow = new google.maps.InfoWindow({
                            content: order
                        });
                        marker.addListener('click', function () {
                            infowindow.open(map, marker);
                        });
                        google.maps.event.addListener(marker, 'drag', function () {
                            order = infowindow.getContent()
                            if (order == 'Start Location') {
                                document.getElementById('start_lat').value = marker.getPosition().lat()
                                $('#start_lat_hidden').val(marker.getPosition().lat())
                                document.getElementById('start_lng').value = marker.getPosition().lng()
                                $('#start_lng_hidden').val(marker.getPosition().lng())
                            }
                            else {
                                document.getElementById('end_lat').value = marker.getPosition().lat()
                                $('#end_lat_hidden').val(marker.getPosition().lat())
                                document.getElementById('end_lng').value = marker.getPosition().lng()
                                $('#end_lng_hidden').val(marker.getPosition().lng())
                            }
                        });

                        order = 'End Location'
                        url_string = "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
                        var marker2 = new google.maps.Marker({
                            position: position_end,
                            map: map,
                            icon: {
                                url: url_string
                            },
                            draggable: true
                        });
                        startEndMarkers.push(marker2)
                        var infowindow2 = new google.maps.InfoWindow({
                            content: order
                        });
                        marker.addListener('click', function () {
                            infowindow.open(map, marker);
                        });
                        google.maps.event.addListener(marker2, 'drag', function () {
                            order = infowindow2.getContent()
                            if (order == 'Start Location') {
                                document.getElementById('start_lat').value = marker2.getPosition().lat()
                                $('#start_lat_hidden').val(marker2.getPosition().lat())
                                document.getElementById('start_lng').value = marker2.getPosition().lng()
                                $('#start_lng_hidden').val(marker2.getPosition().lng())
                            }
                            else {
                                document.getElementById('end_lat').value = marker2.getPosition().lat()
                                $('#end_lat_hidden').val(marker2.getPosition().lat())
                                document.getElementById('end_lng').value = marker2.getPosition().lng()
                                $('#end_lng_hidden').val(marker2.getPosition().lng())
                            }
                        });
                        center_lat = (parseFloat(start_lat) + parseFloat(end_lat)) / 2
                        center_lon = (parseFloat(start_lng) + parseFloat(end_lng)) / 2
                        centerLocation = new google.maps.LatLng(center_lat, center_lon);
                        map.setCenter(centerLocation);
                        //map.setZoom(10)
                        var start_location = new google.maps.LatLng(parseFloat(start_lat), parseFloat(start_lng));
                        var end_location = new google.maps.LatLng(parseFloat(end_lat), parseFloat(end_lng));
                        
                        var $mapDiv = $('#map');
                        var mapDim = { height: $mapDiv.height(), width: $mapDiv.width() };
                        var bounds = new google.maps.LatLngBounds();
                        bounds.extend(start_location);
                        bounds.extend(end_location);
                        zoom = getBoundsZoomLevel(bounds, mapDim)
                        map.setZoom(zoom)
                    }
                    var strmsg = document.getElementById("hdnParam").value;
                    if (strmsg != "This is my message") showContent();
                    // TODO: Move to location and zoom level for markers
                }

                function getBoundsZoomLevel(bounds, mapDim) {
                    var WORLD_DIM = { height: 256, width: 256 };
                    var ZOOM_MAX = 21;

                    function latRad(lat) {
                        var sin = Math.sin(lat * Math.PI / 180);
                        var radX2 = Math.log((1 + sin) / (1 - sin)) / 2;
                        return Math.max(Math.min(radX2, Math.PI), -Math.PI) / 2;
                    }

                    function zoom(mapPx, worldPx, fraction) {
                        return Math.floor(Math.log(mapPx / worldPx / fraction) / Math.LN2);
                    }

                    var ne = bounds.getNorthEast();
                    var sw = bounds.getSouthWest();

                    var latFraction = (latRad(ne.lat()) - latRad(sw.lat())) / Math.PI;

                    var lngDiff = ne.lng() - sw.lng();
                    var lngFraction = ((lngDiff < 0) ? (lngDiff + 360) : lngDiff) / 360;

                    var latZoom = zoom(mapDim.height, WORLD_DIM.height, latFraction);
                    var lngZoom = zoom(mapDim.width, WORLD_DIM.width, lngFraction);

                    return Math.min(latZoom, lngZoom, ZOOM_MAX);
                }

                function initAutocomplete() {
                    //libraries=places&
                    //var map = new google.maps.Map(document.getElementById('map'), {
                    //    center: { lat: -33.8688, lng: 151.2195 },
                    //    zoom: 13,
                    //    mapTypeId: 'roadmap'
                    //});

                    // Create the search box and link it to the UI element.
                    var controlDiv = document.getElementById('mapControlsDiv');
                    var input = document.getElementById('pac-input');
                    var searchBox = new google.maps.places.SearchBox(input);
                    map.controls[google.maps.ControlPosition.TOP_CENTER].push(controlDiv);

                    // Bias the SearchBox results towards current map's viewport.
                    map.addListener('bounds_changed', function () {
                        searchBox.setBounds(map.getBounds());
                    });

                    var markers = [];
                    // Listen for the event fired when the user selects a prediction and retrieve
                    // more details for that place.
                    searchBox.addListener('places_changed', function () {
                        var places = searchBox.getPlaces();

                        if (places.length == 0) {
                            return;
                        }

                        // Clear out the old markers.
                        markers.forEach(function (marker) {
                            marker.setMap(null);
                        });
                        markers = [];

                        // For each place, get the icon, name and location.
                        var bounds = new google.maps.LatLngBounds();
                        places.forEach(function (place) {
                            if (!place.geometry) {
                                //console.log("Returned place contains no geometry");
                                return;
                            }
                            var icon = {
                                url: place.icon,
                                size: new google.maps.Size(71, 71),
                                origin: new google.maps.Point(0, 0),
                                anchor: new google.maps.Point(17, 34),
                                scaledSize: new google.maps.Size(25, 25)
                            };

                            // Create a marker for each place.
                            markers.push(new google.maps.Marker({
                                map: map,
                                icon: icon,
                                title: place.name,
                                position: place.geometry.location
                            }));

                            if (place.geometry.viewport) {
                                // Only geocodes have viewport.
                                bounds.union(place.geometry.viewport);
                            } else {
                                bounds.extend(place.geometry.location);
                            }
                        });
                        map.fitBounds(bounds);
                    });
                }

                document.onfullscreenchange = function (event) {
                    let target = event.target;
                    let pacContainerElements = document.getElementsByClassName("pac-container");
                    if (pacContainerElements.length > 0) {
                        let pacContainer = document.getElementsByClassName("pac-container")[0];
                        if (pacContainer.parentElement === target) {
                            //console.log("Exiting FULL SCREEN - moving pacContainer to body");
                            document.getElementsByTagName("body")[0].appendChild(pacContainer);
                        } else {
                            //console.log("Entering FULL SCREEN - moving pacContainer to target element");
                            target.appendChild(pacContainer);
                        }
                    } else {
                        //console.log("FULL SCREEN change - no pacContainer found");

                    }
                };
                function clear_markers() {
                    for (var i = 0; i < startEndMarkers.length; i++) {
                        startEndMarkers[i].setMap(null);
                    }
                    startEndMarkers = [];
                }

            </script>


            <!--Load the API from the specified URL
* The async attribute allows the browser to render the page while the API loads
* The key parameter will contain your own API key (which is not needed for this tutorial)
* The callback parameter executes the initMap() function
-->
            <%--<script
                src='https://maps.googleapis.com/maps/api/js?key=api-key-here&libraries=places&callback=initMap'>
            </script>--%>
            <script>


</script>
            <script type="text/javascript" src="/js/configcreatorscripts.js"></script>
    </form>
</body>
</html>
