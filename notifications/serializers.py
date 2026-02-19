from .models import Notification
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    # Let make our notification shows username istead of ID number
    recipient = serializers.ReadOnlyField(source='recipient.username')
    actor = serializers.ReadOnlyField(source='actor.username')

    # Let make notification shows string representation of the target (e.g. "Post: my first day")
    target = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target', 'timestamp']