from django.db import models
from django.contrib.auth.models import User

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    path = models.CharField(max_length=256)
    user_address = models.GenericIPAddressField(null=True)
    query_string = models.CharField(max_length=256, null=True)

    @property
    def path_full(self):
        return self.path + ('?' + self.query_string if self.query_string else '')

    def __str__(self):
        return self.path_full + ' accessed by ' + str(self.user or '') + ' at ' + str(self.created_at)
