from github.MainClass import Github

from constants import (ProjectTypes, MAX_SKILLS, MAX_STARS,
    MIN_STARS, MIN_FORKS, MAX_FORKS, MAX_PROJECTS)
from helpers import get_last_month
from hub.models import Project, Skill, Language


class ProjectFinder(object):

    @classmethod
    def find_my_projects(cls, account, type):
        """Find projects for a user, based on hers/his needs: to practice or
        to learn. Save the data in the database.
        """
        connection = Github(login_or_token=account.github_token)

        # Find user Skills
        repos = connection.get_user().get_repos()
        cls.find_account_skills(account, repos)

        # Get wanted skills
        wanted_skills = Skill.objects.filter(account=account)
        if type == ProjectTypes.PRACTICE:
            wanted_skills = wanted_skills[:MAX_SKILLS]
        elif type == ProjectTypes.LEARN:
            wanted_skills.reverse()
            wanted_skills = wanted_skills[:MAX_SKILLS]

        # Search for projects based on what skills he wants to practice
        query = 'languages:%s' % wanted_skills
        stars = '%d..%d' % (MIN_STARS, MAX_STARS)
        forks = '%d..%d' % (MIN_FORKS, MAX_FORKS)
        pushed = '<=%s' % get_last_month()
        qualifiers = {'stars': stars, 'forks': forks, 'pushed': pushed}

        repos = connection.search_repositories(
            query=query, sort='stars', order='desc', **qualifiers)
        cls.find_account_projects(account, repos, type)

    @classmethod
    def find_account_skills(cls, account, repos):
        """Browser all user's repos and add the languages as skills."""
        i = 0
        repos_page = repos.get_page(i)
        while repos_page:
            cls.set_account_skills(account, repos)
            repos_page = repos.get_page(i + 1)
            i += 1

    @classmethod
    def find_account_projects(cls, account, repos, type):
        """Based on the search query, select the maximum number of projects."""
        i = 0
        repos_page = repos.get_page(i)
        while len(repos_page) < MAX_PROJECTS:
            i += 1
            next_repos = repos.get_page(i)
            if next_repos:
                repos_page.extend(next_repos)
            else:
                break
        cls.set_projects_languages(account, repos_page, type)

    @classmethod
    def set_projects_languages(cls, account, repos, type):
        for repo in repos:
            languages = repo.get_languages()
            project = Project(account=account, type=type,
                              name=repo.name, url=repo.html_url,
                              description=repo.description,
                              stars=repo.stargazers_count, forks=repo.forks)
            project.save()
            cls.set_languages(project, languages)
            project.save()

    @classmethod
    def set_account_skills(cls, account, repos):
        for repo in repos:
            languages = repo.get_languages()
            cls.set_skills(account, languages)
            account.save()

    @classmethod
    def set_languages(cls, project, languages):
        total_lines = sum([line for line in languages.itervalues()])
        for language, level in languages.iteritems():
            level = level / total_lines
            language = Language(project=project, name=language, percentage=level)
            language.save()

    @classmethod
    def set_skills(cls, account, languages):
        total_lines = sum([line for line in languages.itervalues()])
        for language, level in languages.iteritems():
            level = level / total_lines
            skill = Skill(account=account, name=language, level=level)
            skill.save()
