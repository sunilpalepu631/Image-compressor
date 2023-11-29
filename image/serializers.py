from rest_framework import serializers
from .models import CompressedImage

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompressedImage
        fields = '__all__'

