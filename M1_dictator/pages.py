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
    form_model = models.Player
    form_fields = ['kept']



class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        message = 'You are assigned to group A and your choice will be implemented. '
        if self.player.id_in_group == 2:
            message = "You are assigned to group B and your choice will not be implemented."
        return {
            'message': message
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
