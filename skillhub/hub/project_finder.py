from github.MainClass import Github

from constants import MAX_PROJECTS, ProjectTypes, MAX_SKILLS
from hub.models import Project, Skill, Language


class ProjectFinder(object):

    @classmethod
    def find_my_projects(cls, account, type):
        """Find projects for a user, based on hers/his needs: to practice or
        to learn. Save the data in the database.
        """
        connection = Github(login_or_token=account.github_token)

        # Skills
        repos = connection.get_user().get_repos()
        cls.find_account_skills(account, repos)
        account.save()
        # Wanted skills
        wanted_skills = Skill.objects.filter(account=account)
        if type == ProjectTypes.PRACTICE:
            wanted_skills = wanted_skills[MAX_SKILLS:]
        elif type == ProjectTypes.LEARN:
            wanted_skills = wanted_skills[:MAX_SKILLS]

        # Search for projects
        search = {'sort': 'stars', 'order': 'desc',
                  'query': 'languages:%s' % wanted_skills}
        repos = connection.search_repositories(**search)
        cls.find_account_projects(account, repos)

    @classmethod
    def find_account_skills(cls, account, repos):
        i = 0
        repos_page = repos.get_page(i)
        while repos_page:
            cls.set_account_skills(account, repos)
            repos_page = repos.get_page(i + 1)
            i += 1

    @classmethod
    def find_account_projects(cls, account, repos):
        i = 0
        repos_page = repos.get_page(i)
        while len(repos_page) < MAX_PROJECTS:
            i += 1
            repos_page.append(repos.get_page(i))
        cls.set_projects_languages(account, repos_page)

    @classmethod
    def set_projects_languages(cls, account, repos):
        for repo in repos:
            languages = repo.get_languages()
            project = Project(account=account)
            cls.set_languages(project, languages)
            project.save()

    @classmethod
    def set_account_skills(cls, account, repos):
        for repo in repos:
            languages = repo.get_languages()
            cls.set_skills(account, languages)
            account.save()

    @classmethod
    def set_skills(cls, account, languages):
        total_lines = sum([line for line in languages.itervalues()])
        for language, level in languages.iteritems():
            level = level / total_lines
            skill = Skill(account=account, name=language, level=level)
            skill.save()


    @classmethod
    def set_languages(cls, project, languages):
        total_lines = sum([line for line in languages.itervalues()])
        for language, level in languages.iteritems():
            level = level / total_lines
            language = Language(project=project, name=language, percentage=level)
            language.save()
