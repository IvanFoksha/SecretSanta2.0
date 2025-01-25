from django.contrib import admin
from .models import Room, RoomUser

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')

@admin.register(RoomUser)
class RoomUserAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'joined_at')
    search_fields = ('room__name', 'user__username')