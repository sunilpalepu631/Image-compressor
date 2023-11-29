# image_compression_app/models.py
from django.db import models

class CompressedImage(models.Model):
    
    image = models.ImageField(upload_to='original_images/')
    
   