from django.db import models

# Create your models here.
class UsersCount(models.Model):
    Num_User = models.IntegerField(default=0)
    Group_Name = models.CharField(max_length=30)
    # def save(self,*args, **kwargs):
    #     self.Num_User += 1
    #     super().save()