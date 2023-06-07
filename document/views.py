from django.http import JsonResponse
from django.http import HttpResponse
from document.models import Document
from .serializer import DocumentSerializer 
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES:
        my_file = request.FILES['my_file']
        print(str(my_file))
        target_path = '/Users/hnitro/Desktop/dianzi/docs/' + str(my_file)
        # 增加系统IO，但是方便哥们实现
        with open(target_path, 'wb+') as destination:
            for chunk in my_file.chunks():
                destination.write(chunk)
        
        # 数据库归档
        doc = Document.objects.create(title=str(my_file)) 
        doc.save() 

        return JsonResponse({'result': 'success'}) 
        # dd = Document(request.POST,request.FILES)
        # print(request.POST)  
        # name = dd.title 
        # file = dd.file 

        # file = request.FILES 
        # print(file) 

        # doc = Document(title=name,file=file) 
        # doc.save() 
        # return JsonResponse({'result': 'success'})  
    else:   return JsonResponse({'result': 'invalid method'})

# 字符流下载
import os
@csrf_exempt
def streamify_file(request,id): 
        doc = Document.objects.get(id=id) 
        title = doc.title 

        file_path = '/Users/hnitro/Desktop/dianzi/docs/' + title  
        print(file_path) 
        filename = title  
        with open(file_path,'rb') as f: 
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

# def download_file(request):
#     file_path = '/path/to/file'  # 文件路径
#     filename = 'my_file.txt'  # 下载文件的名称

#     with open(file_path, 'rb') as f:
#         response = FileResponse(f)
#         response['Content-Disposition'] = f'attachment; filename="{filename}"'
#         return response
        # return JsonResponse({'result':file_path})
        # if os.path.exists(file_path): 
        #     with open(file_path, 'rb') as fh:
        #         resp = FileResponse(fh, content_type='text/plain')
        #         resp['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        #         return resp
        # else: return JsonResponse({'result':'File dose not exisit !'})

# 获取列表
class GetFileList(APIView):
    @csrf_exempt
    def get(self,request): 
        if request.method == 'GET':
            doc = Document.objects.all() 
            serializer = DocumentSerializer(doc,many=True) 
            return JsonResponse(serializer.data,safe=False) 
        else:   return JsonResponse({'result': 'invalid method'})