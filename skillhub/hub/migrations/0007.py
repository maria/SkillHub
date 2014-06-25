# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from constants import BadgeTypes, BadgeUrls
from hub.models import Badge


class Migration(SchemaMigration):

    def forwards(self, orm):
      badges_attributes = (
        {'type': BadgeTypes.FIRST_CONTRIBUTION, 'url': BadgeUrls.FIRST_CONTRIBUTION },
        {'type': BadgeTypes.TEN_CONTRIBUTIONS, 'url': BadgeUrls.TEN_CONTRIBUTIONS},
        {'type': BadgeTypes.FIVE_SKILLS, 'url': BadgeUrls.FIVE_SKILLS},
        )

      for badge_attribute in badges_attributes:
          badge = Badge(**badge_attribute)
          badge.save()

    models = {}

    complete_apps = ['hub']
