from django.contrib import admin

from GameModel import models


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


class MagazinesAdmin(admin.ModelAdmin):
    list_display = ('title', 'domain', 'platform', 'enable')
    fields = ('title', 'domain', 'list_url_template', 'platform', 'enable')


class SerialAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fields = ('title',)


admin.site.register(models.MagzineScores, MagzineScoresAdmin)
admin.site.register(models.Subjects, SubjectsAdmin)
admin.site.register(models.Shelf, ShelfAdmin)
admin.site.register(models.Platforms, PlatformsAdmin)
admin.site.register(models.Magazines, MagazinesAdmin)
admin.site.register(models.Serial, SerialAdmin)
