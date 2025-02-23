from rest_framework import serializers
from .models import CRMModel, CustomField, CRMRecord


class CRMModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRMModel
        fields = "__all__"


class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = "__all__"


class CRMRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRMRecord
        fields = "__all__"
