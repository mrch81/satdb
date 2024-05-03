#!/usr/bin/env python

# Imports

from django.contrib import admin

from .models import Payload
from .models import Launcher
from .models import Owner
from .models import Satellite

# Register your models here.

class SatelliteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner' )


class OwnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')


class LauncherAdmin(admin.ModelAdmin):
    list_display = ('id', 'launcher_type', 'launch_date')


class PayloadAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'satellite', 'type')


admin.site.register(Satellite, SatelliteAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Launcher, LauncherAdmin)
admin.site.register(Payload, PayloadAdmin)