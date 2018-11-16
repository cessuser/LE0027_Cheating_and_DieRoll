from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from . import models


class Introduction(Page):
    pass

class RiskElicitation(Page):
    form_model = models.Player
    form_fields = ['option1', 'option2', 'option3', 'option4', 'option5', 'option6', 'option7', 'option8', 'option9',
                   'option10', 'option11']

    def before_next_page(self):
        self.player.set_payoff()


page_sequence = [
    Introduction,
    RiskElicitation,
]
