from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass

class Results(Page):
    def vars_for_template(self):
        self.group.set_payoff()
        self.group.set_final_payoff()
        return {
            'pay1': self.player.participant.vars['M1_payoff'],
            'pay2': self.player.participant.vars['m2_payoff'],
            'pay3': self.player.participant.vars['m3_payoff'],
            'pay4': self.player.participant.vars['M4_payoff'],
            'pay5': self.player.participant.vars['M5_payoff'],
            'total': self.player.payoff
        }



page_sequence = [
    ResultsWaitPage,
    Results
]
