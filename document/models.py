from django.db import models
from django.utils.timezone import now

class Document(models.Model):   
    title = models.CharField(max_length=255)
    # file = models.FileField(upload_to='docs/')
    createtime = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.title
