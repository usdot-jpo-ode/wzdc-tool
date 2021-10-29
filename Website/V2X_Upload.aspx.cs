using System;
using System.Collections.Generic;
using System.Configuration;
using System.Globalization;
using System.IO;
//using System.IO.Compression;
using System.Linq;
using System.Text.RegularExpressions;
using System.Web;
using System.Web.Hosting;
using System.Web.UI;
using System.Web.UI.WebControls;
using Ionic.Zip;
// using Microsoft.Azure; // Namespace for Azure Configuration Manager
//using Microsoft.Azure.Storage; // Namespace for Storage Client Library
//using Microsoft.Azure.Storage.File; // Namespace for Azure Files
using Microsoft.WindowsAzure.Storage;
using Microsoft.WindowsAzure.Storage.Blob;
using Microsoft.WindowsAzure.Storage.File;
using Newtonsoft.Json;

namespace Neaera_Website_2018
{
    
    public partial class V2X_Upload : System.Web.UI.Page
    {
        protected void UploadButton_Click(object sender, EventArgs e)
        {
            System.Threading.Thread.Sleep(4000);
            // Retrieve storage account from connection string.
            CloudStorageAccount storageAccount = CloudStorageAccount.Parse(ConfigurationManager.ConnectionStrings["StorageConnectionString"].ConnectionString);

            // Create the blob client.
            CloudBlobClient blobClient = storageAccount.CreateCloudBlobClient();

            // Retrieve reference to a previously created container.
            CloudBlobContainer container = blobClient.GetContainerReference("workzoneuploads");

            // Retrieve reference to a blob named "myblob".
            CloudBlockBlob blockBlob = container.GetBlockBlobReference(Regex.Replace(file_uploadpath.PostedFile.FileName, @"[^a-zA-Z0-9.\-]", "-").ToLower());

            // Create or overwrite the "myblob" blob with contents from a local file.
            using (file_uploadpath.PostedFile.InputStream)
            {
                blockBlob.UploadFromStream(file_uploadpath.PostedFile.InputStream);
            }

            this.hdnParam.Value = "Uploaded data files";
            this.msgtype.Value = "Success";
            Page.ClientScript.RegisterStartupScript(this.GetType(), "CallMyFunction", "showContent();", true);

        }
    }
}