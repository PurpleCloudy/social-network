from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SubscribeModel(models.Model):
    self_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'self_user')
    other_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'other_user')