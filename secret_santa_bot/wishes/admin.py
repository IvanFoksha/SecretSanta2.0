from django.contrib import admin
from wish.models import Wish

@admin.register(Wish)
class WishAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'room', 'created_at')
    search_fields = ('text', 'user__username', 'room__name')