from constants import BadgeTypes
from hub.models import Badge, AccountBadge, Contribution


class GiveBadges(object):

    @classmethod
    def get_my_badges(cls, account):

        if len(account.skills) > 5:
            badge = Badge.objects.get(type=BadgeTypes.FIVE_SKILLS)
            cls._set_badge(account, badge)

        contributions = Contribution.objects.filter(account=account)

        if len(contributions) > 1:
            badge = Badge.objects.get(type=BadgeTypes.FIRST_CONTRIBUTION)
            cls._set_badge(account, badge)

        if len(contributions) > 10:
            badge = Badge.objects.get(type=BadgeTypes.TEN_CONTRIBUTIONS)
            cls._set_badge(account, badge)

    @classmethod
    def _set_badge(cls, account, badge):
        if not AccountBadge.objects.filter(account=account, badge=badge):
            account_badge = AccountBadge(account=account, badge=badge)
            account_badge.save()
