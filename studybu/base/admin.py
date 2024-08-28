from django.contrib import admin
from . models import Room,Topic,Message
# Register your models here.

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)

# The Django admin application can use your models to automatically build a site area that you can use to create, view, update, and delete records