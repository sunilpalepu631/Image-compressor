# views.py

from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from .serializers import *
from rest_framework import status
from rest_framework.parsers import *
from django.core.files import File
from .models import CompressedImage
from rest_framework.views import APIView
import datetime 
from rest_framework import viewsets
from django.http import HttpResponse, HttpResponseNotFound
import os
from django.http import FileResponse
import boto3
from django.utils.crypto import get_random_string




class postImage(APIView):
    parser_classes([MultiPartParser, FormParser])

    def post(self, request):
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
    
            uploaded_image = request.FILES['image']
            
            im= Image.open(uploaded_image)

            height = request.data.get('height', im.height//2)
            width = request.data.get('width', im.width//2)
            quality = request.data.get('quality', 50)


            resized_image = im.resize((int(width),int(height))) 

            outputdir = 'compressedImages'
            current_time = datetime.datetime.now()

            filename = f"{current_time.strftime('%f')}_{uploaded_image.name}"
            
            image_stream = BytesIO()   #creating a empty byte object
            resized_image.save(image_stream, format='JPEG', quality=int(quality))   #saving resized image to image_stream object
            image_stream.seek(0)   #the cursor comes to starting point

            try:
                resized_image.save(f'{outputdir}/{filename}', format='JPEG', quality=int(quality))  #saves in compressedimages folder
                #saves original image in original_images folder

                #storing in s3 bucket
                file_path = f'{outputdir}/{filename}'   #path to the compressed image

          
                #need to upload the compressed image to the s3 bucket

                
        
                # Create a response with the image data
                response = HttpResponse(content=image_stream.read(), content_type='image/jpeg')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'   #attachment means it should be downloadable
                return response  #an image will be responsed in the body
                    
                
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





