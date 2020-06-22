from django.contrib import admin

from GameModel.models import MagzineScores, Shelf, Subjects, Platforms


class MagzineScoresAdmin(admin.ModelAdmin):
    list_display = ('id', 'gameId', 'magazine', 'score', 'subject', 'url')
    fields = ('gameId', 'magazine', 'score', 'subject', 'url')


class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('subject', 'edition', 'publishDateStr', 'currency', 'price', 'platform', 'saleArea', 'latestPrice')


class ShelfAdmin(admin.ModelAdmin):
    fields = ('officialGameIds', 'keyword')


class PlatformsAdmin(admin.ModelAdmin):
    list_display = ('platform', 'countryArea', 'countryAreaName')
    fields = ('platform', 'countryArea', 'countryAreaName', 'url')


admin.site.register(MagzineScores, MagzineScoresAdmin)
admin.site.register(Subjects, SubjectsAdmin)
admin.site.register(Shelf, ShelfAdmin)
admin.site.register(Platforms, PlatformsAdmin)
