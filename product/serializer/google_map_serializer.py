from rest_framework import serializers

class map_serializer(serializers.Serializer):
    origins_lat = serializers.CharField(required=True)
    origins_long = serializers.CharField(required=True)
    dest_lat = serializers.CharField(required=True)
    dest_long = serializers.CharField(required=True)