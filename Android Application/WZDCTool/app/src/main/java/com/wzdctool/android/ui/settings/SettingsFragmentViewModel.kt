package com.wzdctool.android.ui.settings

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.navigation.fragment.NavHostFragment.findNavController
import androidx.navigation.fragment.findNavController
import com.wzdctool.android.R
import com.wzdctool.android.dataclasses.AzureInfoObj
import com.wzdctool.android.repos.AzureInfoRepository.currentAzureInfoSubject
import com.wzdctool.android.repos.AzureInfoRepository.isConnectionStringValid
import com.wzdctool.android.repos.ConfigurationRepository
import com.wzdctool.android.repos.DataClassesRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class SettingsViewModel : ViewModel() {

    val connectionStringValid = MutableLiveData<AzureInfoObj>();

    // Save azure settings. Only call if settings are valid
    fun saveSettings(azureInfo: AzureInfoObj) {
        currentAzureInfoSubject.onNext(azureInfo)
        // updateConnectionStringFromObj(azureInfo)
    }

    // Check azure info against saved hash value
    fun verifyUpdateAzureInfo(azureInfo: AzureInfoObj) {
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val isValid = isConnectionStringValid(azureInfo, false)
                connectionStringValid.postValue(isValid)
            }
            catch (e: Exception) {

                connectionStringValid.postValue(azureInfo.copy(valid=false))
            }

        }
    }

}