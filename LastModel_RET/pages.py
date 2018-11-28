from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from . import models

class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoff()
        self.group.set_final_payoff()

class Results(Page):
    def vars_for_template(self):

        return {
            'pay1': self.player.participant.vars['M1_payoff'],
            'pay2': self.player.participant.vars['m2_payoff'],
            'pay3': self.player.participant.vars['m3_payoff'],
            'pay4': self.player.participant.vars['M4_payoff_real_currency'],
            'pay5': self.player.participant.vars['M5_payoff'],
            'total': int(self.player.final_ECUs),
            'total_real': self.player.final_ECUs * self.session.config['real_world_currency_per_point']
        }

class Survey(Page):
    form_model = models.Player
    form_fields = ['it1', 'it2', 'it3', 'it4', 'it5', 'it6', 'it7', 'it8', 'it9', 'it10']


class Survey1(Page):
    form_model = models.Player
    form_fields = ['understanding',
                   "understanding_stage", "specify_understanding", "gender", "age", 'student', 'study', 'major']


page_sequence = [
    ResultsWaitPage,
    Survey,
    Survey1,
    Results
]
