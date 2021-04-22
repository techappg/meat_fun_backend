from django.db import models

class Franchisses(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=30)
    message = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


