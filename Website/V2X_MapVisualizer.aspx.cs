using System;
using System.CodeDom;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
//using System.IO.Compression;
using System.Linq;
using System.Web.UI.WebControls;
using ICSharpCode.SharpZipLib.Zip;
using Microsoft.WindowsAzure.Storage; // Namespace for Storage Client Library
using Microsoft.WindowsAzure.Storage.Blob;
using Newtonsoft.Json;

namespace Neaera_Website_2018
{

    public partial class V2X_MapVisualizer : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {

            }

            if (!ClientScript.IsStartupScriptRegistered("googleMapScript"))
            {
                // Register Startup Script for Google Maps API
                string key = ConfigurationManager.AppSettings["GoogleMapsAPIKey"];
                string api_url = "https://maps.google.com/maps/api/js?key=" + key + "&libraries=geometry";
                string myScript = "<script type=\"text/javascript\" src=\"" + api_url + "\"> </script>";
                //string myScript = "&lt;script type=\"text/javascript\" src=\""+ ConfigurationManager.AppSettings["localhost"] + "\"&gt;&lt;/script&gt;";
                //this.Page.ClientScript.RegisterStartupScript(typeof(Page), "googleMapScript", myScript, true);
                Page.ClientScript.RegisterClientScriptInclude("googleMapScript", api_url);
            }
        }
    }
}