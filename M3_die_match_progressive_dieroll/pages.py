from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from . import models
import random

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1


class RoundPred(Page):
    form_fields = ['roundPred']
    form_model = models.Player

    def vars_for_template(self):
        if self.round_number > 1:
            self.player.modelPred = self.player.participant.vars['modelPred_m3']
        return {
        'round_num': self.round_number
        }


class DiceRolling(Page):
    def vars_for_template(self):
        return {
            'round_num': self.round_number,
        }

class DiceRolling2(Page):
    def vars_for_template(self):
        self.player.roll_die()
        return{
            'roll': self.player.real_die_value,
            'round_num': self.round_number
        }


class ModelPred(Page):
    form_model = models.Player
    form_fields = ['modelPred']

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        self.player.participant.vars['modelPred_m3'] = self.player.modelPred

class GroupWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoff()


class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        pass


class Results(Page):
    def vars_for_template(self):
        self.group.set_final_payoff()

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class RealDiceRolling(Page):
    form_model = models.Player
    form_fields = ['dice_value']

    def vars_for_template(self):
        return {
            'round_num': self.round_number
        }

    def before_next_page(self):
        self.player.payoff += c(self.player.dice_value * 100)
        self.player.participant.vars['all_m3_payoff'].append(self.player.payoff)


class MatchedOutcome(Page):
    pass


page_sequence = [
    Introduction,
    ModelPred,
    RoundPred,
    DiceRolling,
    DiceRolling2,
    GroupWaitPage,
    MatchedOutcome,
    RealDiceRolling,
    ResultsWaitPage,
    Results


]
