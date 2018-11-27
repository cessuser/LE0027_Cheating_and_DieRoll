from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from . import models
import random

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1


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



class GroupWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoff()


class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        pass


class Results(Page):
    def vars_for_template(self):
        self.player.set_final_payoff()

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
        self.player.participant.vars['all_m2_payoff'].append(self.player.payoff)


class MatchedOutcome(Page):
    form_fields = ['declare_gain']
    form_model = models.Player

    def before_next_page(self):
        self.participant.vars['all_declare_gain'].append(self.player.declare_gain)

class continueWaitPage(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        pass

    def is_displayed(self):
        return self.round_number == 1

page_sequence = [
    continueWaitPage,
    Introduction,
    DiceRolling,
    DiceRolling2,
    GroupWaitPage,
    MatchedOutcome,
    ResultsWaitPage,
    Results


]
