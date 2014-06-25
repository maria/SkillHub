import arrow
from github.MainClass import Github

from constants import (ProjectTypes, MAX_SKILLS, MAX_STARS,
    MIN_STARS, MIN_FORKS, MAX_FORKS, MAX_PROJECTS)
from helpers import get_last_month
from hub.models import Project, Skill, Language, Contribution


class ProjectFinder(object):

    @classmethod
    def sync_account(cls, account):
        cls.find_my_contributions(account)
        cls.find_my_projects(account, ProjectTypes.PRACTICE)
        cls.find_my_projects(account, ProjectTypes.LEARN)
        account.synced_at = arrow.utcnow().datetime
        account.save()

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

        # We need the names for the GH query.
        wanted_languages = [skill.name.lower() for skill in wanted_skills]
        query = 'language:%s' % ','.join(wanted_languages)

        # Set query to find an active project
        stars = '%d..%d' % (MIN_STARS, MAX_STARS)
        forks = '%d..%d' % (MIN_FORKS, MAX_FORKS)
        pushed = '>%s' % get_last_month()
        qualifiers = {'stars': stars, 'forks': forks, 'pushed': pushed}

        # Search GH API for projects.
        repos = connection.search_repositories(
            query=query, sort='stars', order='desc', **qualifiers)

        # Save the projects which are a match for the user.
        cls.find_account_projects(account, repos, type)

    @classmethod
    def find_my_contributions(cls, account):
        """Find and save the user contributions. A contribution is a merged
        Pull Request opened by the user.
        """
        connection = Github(login_or_token=account.github_token)

        # Set query to find contributions
        qualifiers = {'is': 'merged', 'type': 'pr',
                      'author': account.user.username}

        # Search GH API for projects.
        issues = connection.search_issues(
            query='', sort='updated', order='desc', **qualifiers)

        i = 0
        issues_page = issues.get_page(i)
        while issues_page:
            for issue in issues_page:

                attributes = {'account': account, 'title': issue.title,
                              'url': issue.html_url,
                              'repo': issue.repository.name,
                              'repo_url': issue.repository.html_url,
                              'merged': issue.updated_at}

                if not Contribution.objects.filter(**attributes):
                    contribution = Contribution(**attributes)
                    contribution.save()
            i += 1
            issues_page = issues.get_page(i)

    @classmethod
    def get_account_wanted_skills(cls, account, type):
        wanted_skills = Skill.objects.filter(account=account).extra(order_by=['-level'])

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

            # Set new attributes on project.
            attributes = {'name': repo.name, 'description': repo.description,
                         'stars': repo.stargazers_count, 'forks': repo.forks}

            for attribute, value in attributes.iteritems():
                setattr(project, attribute, value)
            project.save()

            # Set languages on project.
            cls.set_languages(project.id, languages)

    @classmethod
    def set_account_skills(cls, account, repos):
        for repo in repos:
            languages = repo.get_languages()
            cls.set_skills(account.id, languages)

    @classmethod
    def set_languages(cls, project_id, languages):
        total_lines = sum([line for line in languages.itervalues()])
        for language, level in languages.iteritems():
            level = (level * 100.0) / total_lines

            # If exists, update the language attributes, else create a new entry.
            attributes = {'project_id': project_id, 'name': language}

            if Language.objects.filter(**attributes):
                language = Language.objects.get(**attributes)
                language.percentage = level
            else:
                language = Language(percentage=level, **attributes)
            language.save()

    @classmethod
    def set_skills(cls, account_id, languages):
        total_lines = sum([line for line in languages.itervalues()])
        for language, level in languages.iteritems():
            level = (level * 100.0) / total_lines
            # If exits, update the skill attributes, else create a new entry.
            attributes = {'account_id': account_id, 'name': language}
            if Skill.objects.filter(**attributes):
                skill = Skill.objects.get(**attributes)
                skill.level = level
            else:
                skill = Skill(level=level, **attributes)
            skill.save()
