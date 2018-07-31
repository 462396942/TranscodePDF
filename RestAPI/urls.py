from django.urls import path, re_path, include
from RestAPI.views import (
    fileAPI
)

# RestAPI

urlpatterns = [
	path('file', fileAPI.GetFileAPI, name="api-file"),
	path('file/pdf', fileAPI.GeneratePDF, name="api-file-pdf"),
]

