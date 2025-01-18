from django.db import models
from django.utils.text import slugify

# Category
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image_url = models.URLField(null=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

# when printing model gives the title
    def __str__(self):
        return self.title

class AboutUs(models.Model):
    content = models.TextField()
