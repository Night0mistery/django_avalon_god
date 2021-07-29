from django.contrib import admin
from .models import Player, Room, Rule
# Register your models here.
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'id', 'role', 'room', 'user', 'vote', 'action')
    list_filter = ('player_name', 'role', 'room')
    fieldsets = (
        (None, {
            'fields': ('player_name', 'role', 'id')
        }),
        ('Availability', {
            'fields': ('room', 'user')
        }),
        ('Vote and Action',{
            'fields': ('vote', 'action')
        })
    )


class PlayerInline(admin.TabularInline):
    model = Player

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'player_num', 'Lady_in_the_lake', 'max_num', 'status')
    list_filter = ('status', 'max_num', 'Lady_in_the_lake')
    inlines = [PlayerInline]

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('rule_num', 'tasks', 'roles')

"""
admin.site.register(Player, PlayerAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Rule, RuleAdmin)
"""


# create superuser
# python manage.py createsuperuser