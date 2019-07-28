from django.contrib import admin

from updates.models import Level, Set, History, Version


admin.site.register(Level)
admin.site.register(Set)
admin.site.register(History)
admin.site.register(Version)
