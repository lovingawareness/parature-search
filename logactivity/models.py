from django.db import models
from django.contrib.auth.models import User

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    path = models.TextField()

    def __str__(self):
        return self.path + ' accessed by ' + str(self.user) + ' at ' + str(self.created_at)
