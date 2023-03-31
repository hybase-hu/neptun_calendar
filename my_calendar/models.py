import datetime


from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class NeptunUser(models.Model):
    calendar = models.FileField(upload_to="calendar", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_calendar = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class NeptunClass:
    def __init__(self,start,end,desc,local):
        self.start =  datetime.datetime.strptime(start, '%Y.%m.%d. %H:%M:%S')
        #self.start = start
        self.end = datetime.datetime.strptime(end, '%Y.%m.%d. %H:%M:%S')
        #self.end = end
        self.desc = desc
        self.local = local

    def get_length(self):
        return (self.end - self.start).seconds / 60

