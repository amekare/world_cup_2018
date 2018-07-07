from django.db.models.signals import post_save
from django.dispatch import receiver
from dashboard.views import update_gamblers, update_gamblers2

from dashboard.models import Bet


@receiver(post_save, sender=Bet)
def scores_updates(sender, **kwargs):
    bet = kwargs['instance']
    if bet.source.name == 'Oficial':
        #update_first_round(bet.match.stage)
        update_gamblers()
        update_gamblers2()

