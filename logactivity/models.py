from django.db import models
from django.contrib.auth.models import User

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    path = models.TextField()
    user_address = models.GenericIPAddressField(null=True)
    query_string = models.TextField(null=True)

    def __str__(self):
        return self.path + (self.query_string or '') + ' accessed by ' + str(self.user or '')
