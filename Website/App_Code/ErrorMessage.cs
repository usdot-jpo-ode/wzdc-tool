using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace WZDCTool_Website.App_Code
{
    public class ErrorMessage
    {
        public string data_file;
        public string wz_id;
        public string error_message;

        public ErrorMessage(string data_file, string error_message)
        {
            this.data_file = data_file;
            this.error_message = error_message;
        }
    }
}