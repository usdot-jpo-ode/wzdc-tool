using System;
using System.Collections.Generic;
using System.Text;
using Azure;
using Azure.Core;
using Azure.Identity;
using Microsoft.Rest.Azure.Authentication;
using Microsoft.ApplicationInsights;
using Azure.Monitor.Query;
using RestSharp;
using System.Configuration;
using System.Net;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using WZDCTool_Website.App_Code;
using System.Linq;

namespace Neaera_Website_2018
{

    public partial class V2X_Logs : System.Web.UI.Page
    {
        protected async void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                getLogData();
            }
        }        

        public void getLogData()
        {
            string[] headers = new string[] {
                "time",
                "severity",
                "data file name",
                "message",
            };
            int[] widths = new int[]
            {
                150,
                50,
                200,
                500,
            };
            //string[][] fields = new string[][] {
            //    new string[] {
            //        "time",
            //        "severity",
            //        "message",
            //        "source"
            //    },
            //    new string[] {
            //        "time",
            //        "severity",
            //        "message",
            //        "source"
            //    }
            //};
            //string table_text = generateLogTable(headers, fields);
            //logTable.Text = table_text;

            string jsonResponse = QueryAppInsights("exceptions | where timestamp > ago(2d)"); // 
            var result = JsonConvert.DeserializeObject<JToken>(jsonResponse);
            if (result == null)
            {
                this.hdnParam.Value = $"Failed to query logs";
                this.msgtype.Value = "Error";
                Page.ClientScript.RegisterStartupScript(this.GetType(), "CallMyFunction", "showContent();", true);
                return;
            }

            // Check if data returned from query
            if (result["tables"] == null)
            {
                logTable.Text = generateLogTable(headers, widths, new List<string[]>());
                return;
            }
            JToken table = ((JArray)result["tables"])[0];

            JArray columns = (JArray)table["columns"];

            Dictionary<string, int> keys = new Dictionary<string, int>();

            int i = 0;
            foreach (JToken col in columns)
            {
                keys.Add((string)col["name"], i);
                i++;
            }

            JArray rows = (JArray)table["rows"];
            List<string[]> logData = new List<string[]>();
            foreach (JToken row in rows)
            {
                string innerMessage = (string)row[keys["innermostMessage"]];

                int start = innerMessage.IndexOf('{');
                int end = innerMessage.IndexOf('}') + 1;
                if (start != -1 && end != -1 && start < end)
                {
                    innerMessage = innerMessage.Substring(start, (end - start));
                }

                ErrorMessage messageObj = new ErrorMessage("unknown", innerMessage);
                try
                {
                    messageObj = JsonConvert.DeserializeObject<ErrorMessage>(innerMessage);
                }
                finally
                {
                    if (messageObj == null)
                    {
                        messageObj = new ErrorMessage("unknown", innerMessage);
                    }
                }

                logData.Add(new string[]
                {
                        (string)row[keys["timestamp"]],
                        (string)row[keys["severityLevel"]],
                        messageObj.data_file,
                        messageObj.error_message,
                });
            }
            logData.Sort(delegate (string[] row1, string[] row2) { return row2[0].CompareTo(row1[0]); });
            for (int index = logData.Count - 1; index > 0; index--)
            {
                if (logData[index].SequenceEqual(logData[index - 1]))
                {
                    logData.RemoveAt(index);
                }
            }
            logTable.Text = generateLogTable(headers, widths, logData);
        }

        private string QueryAppInsights(string query)
        {

            var client = new RestClient(String.Format("https://api.applicationinsights.io/v1/apps/{0}/query?query={1}", ConfigurationManager.AppSettings["GenerateMessagesAppInsightsID"], Uri.EscapeUriString(query)));
            client.Timeout = -1;
            var request = new RestRequest(Method.GET);
            request.AddHeader("x-api-key", ConfigurationManager.AppSettings["GenerateMessagesAppInsightsAPIKey"]);
            //request.AddHeader("Content-Type", "application/json");
            //request.AddParameter("application/json", data, ParameterType.RequestBody);
            IRestResponse response = client.Execute(request);
            HttpStatusCode statusCode = response.StatusCode;
            int numericStatusCode = (int)statusCode;
            return response.Content;
        }

        private string generateLogTable(string[] headers, int[] widths, List<string[]> fields)
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("<table cellpadding='5' cellspacing='0' style='border: 1px solid #ccc;font-size: 9pt;font-family:Arial;' class='fixed_header'>");

            // Headers
            sb.Append("<tr>");
            foreach (string header in headers)
            {
                sb.Append("<th style='background-color: #B8DBFD;border: 1px solid #ccc'>" + header + "</th>");
            }
            sb.Append("</tr>");

            //Add Data Rows
            foreach (string[] row in fields)
            {
                sb.Append("<tr>");
                int index = 0;
                foreach (string field in row)
                {
                    sb.Append($"<td style='width:{widths.GetValue(index)}px;border: 1px solid #ccc'>" + field + "</td>");
                    index++;
                }
                sb.Append("</tr>");
            }

            //Table end
            sb.Append("</table>");

            return sb.ToString();
        }

    //GET /v1/apps/3de5a420-6cb0-4150-99f6-51f627804720/query?query=exceptions HTTP/1.1
    //Host: api.applicationinsights.io
    //x-api-key: dib8j8mm2rleswvj14q2j7a0ariv6ygdgg7056c5

    }
}