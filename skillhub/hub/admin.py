from django.contrib import admin

from hub.models import Account, Tip, Tutorial, Skill


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'github_url')


class TipAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


class TutorialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level')


admin.site.register(Account, AccountAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Tip, TipAdmin)
admin.site.register(Tutorial, TutorialAdmin)
