from django.contrib import admin

from updates.forms import AdminLevelForm
from updates.models import Level, Set, History, Version


class LevelAdmin(admin.ModelAdmin):
    form = AdminLevelForm


admin.site.register(Level, LevelAdmin)
admin.site.register(Set)
admin.site.register(History)
admin.site.register(Version)
