from django.contrib import admin

from hub.models import Account, Tip, Skill


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'github_url')


class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'account',  'name', 'level')


class TipAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

admin.site.register(Account, AccountAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Tip, TipAdmin)
