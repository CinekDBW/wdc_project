from django.contrib import admin
from .models import Post, Topic

admin.site.register(Topic)
admin.site.register(Post)