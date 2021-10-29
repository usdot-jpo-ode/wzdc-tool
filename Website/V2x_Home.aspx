<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="V2x_Home.aspx.cs" Inherits="Neaera_Website_2018.V2x_Home" %>

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
  
</head>
<body>
    <form id="form1" runat="server">
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
              Work Zone Data Exchange
            </p>
            <!--<button onclick="window.location.href = 'what_you_need_to_know.html'" class="usa-button usa-button--outline usa-button--big float-left">EXPLORE</button>-->
          </div>
        </div>
      </div>
		</div> <!-- /.grid-container -->
  </div>
        <section id="middle-info">
    <div class="grid-container" style="max-width: 60%;">
      <h1 class="text-center">V2X WorkZone Data Exchange</h1>
      <div class="grid-row">
        <%--<div class="grid-col-12 tablet:grid-col-4">
          <a class="link-box" href="RSM_Translator_WZDx.aspx"
            <h3>V2X Translator from RSM to WzDx </h3>
            <div class="smallIconContainer margin-x-auto">
             
            </div>
            <p>
              Take your RSM file and translate that to a WZDx file
            </p>
          </a>
        </div>--%> <!-- /.grid-col -->
       <div class="grid-col-12 tablet:grid-col-4" style="width: 25%; min-width: 250px; margin-top: 20px">
          <a class="link-box" href="V2X_ConfigCreator.aspx">
            <h3>Configuration Creator</h3>
            <div class="smallIconContainer margin-x-auto">
              <%--<img src="images/svgs/SDC_Icon_Get_Started.svg" alt="">--%>
            </div>
            <p>
              Create your config file
            </p>
          </a>
        </div> <!-- /.grid-col -->
       <div class="grid-col-12 tablet:grid-col-4" style="width: 25%; min-width: 250px; margin-top: 20px">
          <a class="link-box" href="V2X_Upload.aspx">
            <h3>Upload Data Files</h3>
            <div class="smallIconContainer margin-x-auto">
              <%--<img src="images/svgs/SDC_Icon_Get_Started.svg" alt="">--%>
            </div>
            <p>
              Upload Work Zone Data Collection Files
            </p>
          </a>
        </div> <!-- /.grid-col -->
       <div class="grid-col-12 tablet:grid-col-4" style="width: 25%; min-width: 250px; margin-top: 20px">
          <a class="link-box" href="V2X_Verification.aspx">
            <h3>Verification, Visualization and Work Zone Editing</h3>
            <div class="smallIconContainer margin-x-auto">
              <%--<img src="images/svgs/SDC_Icon_Get_Started.svg" alt="">--%>
            </div>
            <p>
              Verify, Visualize and Editing Work Zone Data
            </p>
          </a>
        </div> <!-- /.grid-col -->
       <div class="grid-col-12 tablet:grid-col-4" style="width: 25%; min-width: 250px; margin-top: 20px">
          <a class="link-box" href="V2X_Published.aspx">
            <h3>View Published Work Zones</h3>
            <div class="smallIconContainer margin-x-auto">
              <%--<img src="images/svgs/SDC_Icon_Get_Started.svg" alt="">--%>
            </div>
            <p>
              View Published Work Zones and Data
            </p>
          </a>
        </div> <!-- /.grid-col -->
       <div class="grid-col-12 tablet:grid-col-4" style="width: 25%; min-width: 250px; margin-top: 20px">
          <a class="link-box" href="V2X_Logs.aspx">
            <h3>View Logs</h3>
            <div class="smallIconContainer margin-x-auto">
              <%--<img src="images/svgs/SDC_Icon_Get_Started.svg" alt="">--%>
            </div>
            <p>
              View Message Generation Log Messages
            </p>
          </a>
        </div> <!-- /.grid-col -->

      </div> <!-- /.grid-row -->
    </div>
  </section>
  <section id="bottom-info" class="bg-primary-lighter">
    <div class="grid-container margin-top-7 padding-bottom-7 padding-top-2">
      <div class="grid-row flex-align-stretch">
        <div class="tablet:grid-col-9">
          <h2>V2X project Details</h2>
          <p>
              Description of V2X Project
            </p>
        </div>
      </div>
    </div>
  </section>
</main>
<footer role="contentinfo">
  <div id="footer"></div>
</footer>
<script src="assets_v2x/js/uswds.min.js"></script>
    </form>
</body>
</html>
