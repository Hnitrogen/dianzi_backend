from django.urls import path , include 
from document.views import upload_file , GetFileList , streamify_file

urlpatterns = [
    path('file/upload/',upload_file),
    path('file/get/',GetFileList.as_view()), 
    path('file/download/<int:id>/',streamify_file), 
]