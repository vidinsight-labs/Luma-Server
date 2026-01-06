"""
URL configuration for LumaServer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
from django.urls import path
from api.views.ProjectViews import (
    CreateProject,
    GetProjectList,
    GetProjectDetail,
    UpdateProject,
    DeleteProject, DownloadProject
)
from api.views.CollectionViews import (
    CreateCollection,
    GetCollectionList,
    GetCollectionDetail,
    DownloadCollection,
    DeleteCollection
)
from api.views.FileViews import (
    GetFileListByCollection,
    GetFileDetail,
    DownloadFile
)
from api.views.DeviceViews import (
    AddDevice,
    GetDeviceList,
    UpdateDevice,
    DeleteDevice,
    ReconnectCameras,
    DeleteAllPhotos,
    ResetDevices
)
from api.views.SettingViews import (
    GetSetting as GetCameraSetting,
    UpdateSetting as UpdateCameraSetting,
    GetFlashSetting,
    UpdateFlashSetting
)

urlpatterns = [
    path('api/create-project/', CreateProject.as_view(), name='create-project'),
    path('api/get-project-list', GetProjectList.as_view(), name='get-project-list'),
    path('api/get-project-detail/<int:project_id>', GetProjectDetail.as_view(), name='get-project-detail'),
    path('api/update-project/<int:project_id>', UpdateProject.as_view(), name='update-project'),
    path('api/delete-project/<int:project_id>', DeleteProject.as_view(), name='delete-project'),
    path('api/download-project/<int:project_id>', DownloadProject.as_view(), name='download-project'),

    # Collection endpoints
    path('api/create-collection/<int:project_id>', CreateCollection.as_view(), name='create-collection'),
    path('api/get-collection-list/<int:project_id>', GetCollectionList.as_view(), name='get-collection-list'),
    path('api/get-collection-detail/<int:collection_id>', GetCollectionDetail.as_view(), name='get-collection-detail'),
    path('api/download-collection/<int:collection_id>', DownloadCollection.as_view(), name='download-collection'),
    path('api/delete-collection/<int:collection_id>', DeleteCollection.as_view(), name='delete-collection'),

    # File endpoints
    path('api/get-file-list/<int:collection_id>', GetFileListByCollection.as_view(), name='get-file-list-by-collection'),
    path('api/get-file-detail/<int:file_id>', GetFileDetail.as_view(), name='get-file-detail'),
    path('api/download-file/<int:file_id>', DownloadFile.as_view(), name='download-file'),

    # Device endpoints
    path('api/add-device', AddDevice.as_view(), name='add-device'),
    path('api/get-device-list', GetDeviceList.as_view(), name='get-device-list'),
    path('api/update-device/<int:device_id>', UpdateDevice.as_view(), name='update-device'),
    path('api/delete-device/<int:device_id>', DeleteDevice.as_view(), name='delete-device'),
    path('api/reconnect-cameras', ReconnectCameras.as_view(), name='reconnect-cameras'),
    path('api/delete-all-photos', DeleteAllPhotos.as_view(), name='delete-all-photos'),
    path('api/reset-devices', ResetDevices.as_view(), name='reset-devices'),

    # Setting endpoints
    path('api/get-camera-setting', GetCameraSetting.as_view(), name='get-camera-setting'),
    path('api/update-camera-setting', UpdateCameraSetting.as_view(), name='update-camera-setting'),
    path('api/get-flash-setting', GetFlashSetting.as_view(), name='get-flash-setting'),
    path('api/update-flash-setting', UpdateFlashSetting.as_view(), name='update-flash-setting'),
]
