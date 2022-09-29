from django.db import models

# Create your models here.
class Post(models.Model):
    num1 = models.IntegerField(blank=True, null=True)
    num2 = models.TextField(blank=True, null=True)
    num3 = models.IntegerField(blank=True, null=True)
    num4 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.num1) +' , ' + str(self.num2) + (' , ')+ str(self.num3)+ (' , ') + str(self.num4)