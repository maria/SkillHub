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

        # Search for projects based on what skills he wants to practice
        wanted_skills = cls.get_account_wanted_skills(account, type)
        # If the user doesn't have any skills and she/he wants to practice,
        # return none, let him start a project on his own / learn.
        if len(wanted_skills) == 0 and type == ProjectTypes.PRACTICE:
            return

        query = 'languages:%s' % wanted_skills
        # Settings to find an active project
        stars = '%d..%d' % (MIN_STARS, MAX_STARS)
        forks = '%d..%d' % (MIN_FORKS, MAX_FORKS)
        pushed = '<=%s' % get_last_month()
        qualifiers = {'stars': stars, 'forks': forks, 'pushed': pushed}
        # Search GH API for projects.
        repos = connection.search_repositories(
            query=query, sort='stars', order='desc', **qualifiers)

        # Save the projects which are a match for the user.
        cls.find_account_projects(account, repos, type)

    @classmethod
    def get_account_wanted_skills(cls, account, type):
        wanted_skills = Skill.objects.filter(account=account)

        # Return based on the activity the list of languages.
        if type == ProjectTypes.PRACTICE:
            wanted_skills = wanted_skills[:MAX_SKILLS]
        elif type == ProjectTypes.LEARN:
            wanted_skills.reverse()
            wanted_skills = wanted_skills[:MAX_SKILLS]

        return wanted_skills

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
            attributes = {'account': account, 'url': repo.html_url, 'type': type}

            if Project.objects.filter(**attributes):
                project = Project.objects.get(**attributes)
            else:
                project = Project(**attributes)

            attributes = {'name': repo.name, 'description': repo.description,
                         'stars': repo.stargazers_count, 'forks': repo.forks}

            for attribute, value in attributes.iteritems():
                setattr(project, attribute, value)

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
            # If exists, update the language attributes, else create a new entry.
            if Language.objects.filter(project=project, name=language):
                language = Language.objects.get(project=project, name=language)
            else:
                language = Language(project=project, name=language, percentage=level)

            language.save()

    @classmethod
    def set_skills(cls, account, languages):
        total_lines = sum([line for line in languages.itervalues()])
        for language, level in languages.iteritems():
            level = level / total_lines
            # If exits, update the skill attributes, else create a new entry.
            if Skill.objects.filter(account=account, name=language):
                skill = Skill.objects.get(account=account, name=language)
            else:
                skill = Skill(account=account, name=language, level=level)
            skill.save()
