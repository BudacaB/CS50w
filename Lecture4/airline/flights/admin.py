from django.contrib import admin

from .models import Flight, Airport, Passenger

# Register your models here.

# different configs for the admin interface
class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration")

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",) # special way of manipulating many-to-many relationships with this attribute

admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin) # register the Flight but use the FlightAdmin settings
admin.site.register(Passenger, PassengerAdmin)
