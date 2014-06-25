from django.db.models.signals import post_save

from hub.models import Account


def update_badges(sender, instance, **kwargs):
    GiveBadges.get_my_badges(instance)


post_save.connect(update_badges, sender=Account, dispatch_uid="update_account_badges")
