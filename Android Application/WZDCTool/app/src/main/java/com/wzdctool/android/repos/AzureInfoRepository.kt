package com.wzdctool.android.repos

import com.microsoft.azure.storage.CloudStorageAccount
import com.microsoft.azure.storage.blob.CloudBlobClient
import com.microsoft.azure.storage.blob.CloudBlobContainer
import com.microsoft.azure.storage.blob.CloudBlockBlob
import com.wzdctool.android.Constants
import com.wzdctool.android.dataclasses.AzureInfoObj
import rx.subjects.BehaviorSubject
import java.io.FileInputStream

object AzureInfoRepository {

    val validLoginInfoSubject: BehaviorSubject<Boolean> = BehaviorSubject.create<Boolean>(true)

    val currentAzureInfoSubject: BehaviorSubject<AzureInfoObj> = BehaviorSubject.create<AzureInfoObj>()

    val currentConnectionStringSubject: BehaviorSubject<String> = BehaviorSubject.create<String>()

    // var savedAzure

    private fun createConnectionString(azureInfo: AzureInfoObj): String {
        return "DefaultEndpointsProtocol=https;" +
                "AccountName=${azureInfo.account_name};" +
                "AccountKey=${azureInfo.account_key};" +
                "EndpointSuffix=core.windows.net"
    }

    fun updateConnectionString(connectionString: String) {
        currentConnectionStringSubject.onNext(
            connectionString
        )
    }

    fun updateConnectionStringFromObj(azureInfo: AzureInfoObj) {
        currentConnectionStringSubject.onNext(
            createConnectionString(azureInfo)
        )
    }

    fun isConnectionStringValid(azureInfo: AzureInfoObj, update: Boolean): AzureInfoObj {
        if (azureInfo.account_name.isEmpty() || azureInfo.account_key.isEmpty())
            return azureInfo.copy(valid=false)

        val connectionString = createConnectionString(azureInfo)

        try {
            val storageAccount: CloudStorageAccount =
                CloudStorageAccount.parse(connectionString)
            val blobClient: CloudBlobClient = storageAccount.createCloudBlobClient()

            val containers: List<String> = listOf(Constants.AZURE_PATH_DATA_UPLOADS_CONTAINER, Constants.AZURE_PUBLISHED_CONFIG_FILES_CONTAINER)
            for (container in containers) if (!blobClient.getContainerReference(container).exists()) return azureInfo.copy(valid=false)
        }
        catch (e: Exception) {
            return azureInfo.copy(valid=false)
        }

        return azureInfo.copy(valid=true)
    }

    fun parseConnectionString(connectionString: String) {

    }

}