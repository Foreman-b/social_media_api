from .serializers import NotificationSerializer
from .models import Notification
from rest_framework import permissions, generics, status


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        """Let filter the notifications so that each user only see their own
        orderby "-timestap (which shows it in descending order last notification to come first)
        """
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')