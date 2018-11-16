from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import time


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1


class TaskPage(Page):
    form_fields = ['answer']
    form_model = models.Player
    timeout_seconds = 60

    def is_displayed(self):
        if self.round_number == 1:
            self.player.participant.vars['remaining_time'] = 60
        self.player.participant.vars['time_onLoad'] = time.time()
        return self.player.participant.vars['remaining_time'] > 0 and 1 <= self.round_number <= Constants.num_rounds

    def get_timeout_seconds(self):
        print("remain time: ", self.participant.vars['remaining_time'])
        return self.player.participant.vars['remaining_time']

    def vars_for_template(self):
        return {
            'shown_num1': Constants.nums1[self.round_number - 1],
            'shown_num2': Constants.nums2[self.round_number - 1]
        }

    def before_next_page(self):
        self.player.check_correct()
        spent = time.time() - self.player.participant.vars['time_onLoad']
        self.player.participant.vars['remaining_time'] = self.player.participant.vars['remaining_time'] - spent
        if self.timeout_happened:
            self.player.participant.vars['remaining_time'] = 0


class ModelPred(Page):
    form_model = models.Player
    form_fields = ['modelPred']

    def is_displayed(self):
        return self.round_number == 1


class RoundPred(Page):
    form_model = models.Player
    form_fields = ['roundPred']

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        self.player.participant.vars['roundPred'] = self.player.roundPred

class ResultWaitPage(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        pass


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        self.group.set_payoff()
        return{
            'n_correct': self.player.participant.vars['n_correct1_M5']
        }




page_sequence = [
    Introduction,
    ModelPred,
    RoundPred,
    TaskPage,
    ResultWaitPage,
    Results
]
