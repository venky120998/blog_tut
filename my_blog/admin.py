from django.contrib import admin
from my_blog.models import Post, Category, AboutUs

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    search_fields = ('title', 'content')
    list_filter = ('category', 'created_at')

admin.site.register(model_or_iterable=Post, admin_class=PostAdmin)
admin.site.register(model_or_iterable=Category)
admin.site.register(model_or_iterable=AboutUs)