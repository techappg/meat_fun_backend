from django.db import models

from product.models.category import Category
#
#
# class blog_Category(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True,)
#     updated_at = models.DateTimeField(auto_now=True)
#     # is_enable = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.name

SEMESTER_CHOICES = (
    ("left", "left"),
    ("right", "right"),
    ("center", "center"),
)

class Blog(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    image = models.FileField(upload_to='media/', null=False, blank=False)
    image_positions = models.CharField(max_length=50, choices=SEMESTER_CHOICES, default='left')
    is_enable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title