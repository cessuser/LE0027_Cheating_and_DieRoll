from ._builtin import Page, WaitPage
from .models import Constants
from . import models


class Introduction(Page):
    pass

class DiceRolling(Page):
    form_fields = ['dice_value']
    form_model = models.Player

    def vars_for_template(self):
        self.player.payoff = 0


class Offer(Page):
    form_model = 'group'
    form_fields = ['kept']

    def is_displayed(self):
        return self.player.id_in_group == 1


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    def vars_for_template(self):
        return {
            'offer': Constants.endowment - self.group.kept,
        }

class Intro(Page):
    def is_displayed(self):
        return self.round_number == 1

page_sequence = [
    Intro,
    Introduction,
    DiceRolling,
    Offer,
    ResultsWaitPage,
    Results

]
