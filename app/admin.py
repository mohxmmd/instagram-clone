from django.contrib import admin
from app.models import Post,Stories,Message,Profile,DirectMessage

# Register your models here.

admin.site.register([Post, Stories, Message, DirectMessage])
