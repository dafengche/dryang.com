from django.contrib import admin

from badminton.models import Player, CostType, Cost, Record


class RecordAdmin(admin.ModelAdmin):
    filter_horizontal = ('players',)

admin.site.register(Player)
admin.site.register(CostType)
admin.site.register(Cost)
admin.site.register(Record, RecordAdmin)
