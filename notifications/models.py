from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actions'
    )

    verb = models.CharField(max_length=255)

    # Now let setup Generic Foreign Key here
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    # Let store the ID of the object
    target_object_id = models.PositiveIntegerField()

    # Let handle actual link to the object
    target = GenericForeignKey('target_content_type', 'target_object_id')

    timestamp = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.actor} {self.verb} {self.target}"
