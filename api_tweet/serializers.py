from rest_framework import serializers
from coreapp.models import Tweet

class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ('id', 'text', 'Tweet_by')
        read_only_fields = ('id',)