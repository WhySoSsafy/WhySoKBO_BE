from django.contrib import admin
from .models import Team, TeamTag, Player, PlayerTag, PlayerSeasonStat, Question, Choice


class TeamTagInline(admin.StackedInline):
    model = TeamTag
    extra = 0


class PlayerTagInline(admin.StackedInline):
    model = PlayerTag
    extra = 0


class PlayerSeasonStatInline(admin.StackedInline):
    model = PlayerSeasonStat
    extra = 0


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [TeamTagInline]
    list_display = ['name', 'region', 'stadium']
    search_fields = ['name', 'region']


@admin.register(TeamTag)
class TeamTagAdmin(admin.ModelAdmin):
    list_display = ['team', 'passion', 'fan_culture', 'winning', 'underdog', 'analytic']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    inlines = [PlayerTagInline, PlayerSeasonStatInline]
    list_display = ['name_ko', 'team', 'position', 'number', 'is_active', 'is_recommendable']
    list_filter = ['team', 'position', 'is_active', 'is_recommendable']
    search_fields = ['name_ko']


@admin.register(PlayerTag)
class PlayerTagAdmin(admin.ModelAdmin):
    list_display = ['player', 'power', 'contact', 'ace', 'clutch', 'charisma']


@admin.register(PlayerSeasonStat)
class PlayerSeasonStatAdmin(admin.ModelAdmin):
    list_display = ['player', 'season_year']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['quiz_type', 'number', 'category', 'question_text', 'input_type', 'is_conditional']
    list_filter = ['quiz_type', 'input_type']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'label', 'key', 'display_order']
    list_filter = ['question__quiz_type']
