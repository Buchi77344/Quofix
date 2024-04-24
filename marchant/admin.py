from django.contrib import admin

# Register your models here.
from  marchant.models import MarchantUser ,Transaction ,MarchantNotification

admin.site.register(MarchantNotification)