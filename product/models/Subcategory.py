
from django.db import models
from product.models.category import Category
from django.contrib.auth.models import User


class Subcategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, null=False, blank=False, on_delete=models.CASCADE, related_name='category', db_index=True)
    is_enable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('category', 'name',)

    def __str__(self):
        return self.name

class Subcategory_like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subcategory=models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username
