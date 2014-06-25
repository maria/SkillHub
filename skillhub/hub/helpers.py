import arrow

from constants import ProjectTypes, MAX_PROJECTS
from hub.models import Project


def get_last_month():
    now = arrow.utcnow()
    if now.month != 1:
        last_month = now.replace(month=(now.month - 1))
    else:
        last_month = now.replace(year=(now.year - 1), month=12)
    return last_month.format("YYYY-MM-DD")


def get_last_day():
    now = arrow.utcnow()
    if now.day - 1 >= 1:
        last_day = now.replace(day=(now.day - 1))
    else:
        last_day = now.replace(month=(now.month - 1), day=31)
    return last_day.datetime


def get_projects(account, type):
    projects = Project.objects.filter(account=account, type=type).extra(
        order_by=['-updated_at'])[:MAX_PROJECTS]
    # Group project in pair of two, so we can display them in a table.
    return zip(projects[0::2], projects[1::2])
