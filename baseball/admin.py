from django.contrib import admin
from .models import Team, Player, TeamQuestion, PlayerQuestion

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(TeamQuestion)
admin.site.register(PlayerQuestion)
