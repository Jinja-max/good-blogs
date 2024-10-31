from django.contrib import admin
from . import models

# Register your models here.

myModels = [models.Author, models.Blog, models.Tag, models.Comment]

admin.site.register(myModels)
