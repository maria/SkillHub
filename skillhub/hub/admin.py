from django.contrib import admin

from hub.models import Account, Tip, Tutorial, Skill, Project


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'github_url')


class TipAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


class TutorialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'url', 'description', 'stars', 'forks')


admin.site.register(Account, AccountAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Tip, TipAdmin)
admin.site.register(Tutorial, TutorialAdmin)
