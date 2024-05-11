#!/usr/bin/env python

"""Django's Admin models are defined here."""

from django.contrib import admin

from .models import Launcher, Owner, Payload, Satellite


class SatelliteAdmin(admin.ModelAdmin):
    """Admin view for Satellite model."""

    list_display = ('id', 'name', 'sat_id', 'tle_date', 'line1', 'line2')


class OwnerAdmin(admin.ModelAdmin):
    """Admin view for Owner model."""

    list_display = ('id', 'name', 'country')


class LauncherAdmin(admin.ModelAdmin):
    """Admin view for Launcher model."""

    list_display = ('id', 'launcher_type', 'launch_date')


class PayloadAdmin(admin.ModelAdmin):
    """Admin view for Payload model."""

    list_display = ('id', 'provider', 'satellite', 'type')


admin.site.register(Satellite, SatelliteAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Launcher, LauncherAdmin)
admin.site.register(Payload, PayloadAdmin)
