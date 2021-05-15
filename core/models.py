from django.db import models

# Create your models here.

class Repeary(models.Model):
    name=models.CharField(max_length=500,verbose_name="Bakım Modu")
    repear=models.BooleanField(verbose_name="Bakım Modu",default=False)

    
    def __str__(self):
        return self.name
    
    def repair_status(self):
        if self.repear:
            return "Açık"
        else:
            return "Kapalı"

