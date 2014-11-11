from django.contrib import admin

from badminton.models import Player, CostType, Cost, Game, ContributionType, Contribution


class GameAdmin(admin.ModelAdmin):
    filter_horizontal = ('players',)

admin.site.register(Player)
admin.site.register(CostType)
admin.site.register(Cost)
admin.site.register(Game, GameAdmin)
admin.site.register(ContributionType)
admin.site.register(Contribution)
