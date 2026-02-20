from rest_framework import serializers
from utangerapp.models import *

class UtangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utang
        fields = '__all__'