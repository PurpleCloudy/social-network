from django.db import models
from django.contrib.auth.models import User

# Create your models here.
user = models.ForeignKey(User)
text = models.TextField()
date = models.DateTimeField(auto_now=False)