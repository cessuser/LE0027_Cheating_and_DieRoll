from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Danlin Chen'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'M5_number_add1'
    players_per_group = 3
    num_rounds = 30

class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            nums1 = [59, 62, 10, 50, 17, 34, 42, 75, 13, 32, 93, 55, 94, 31, 100, 92, 56, 44, 17, 94, 68, 94, 12, 89, 92, 76, 96, 21, 65, 50]
            nums2 = [51, 68, 97, 13, 93, 68, 16, 76, 16, 46, 90, 80, 38, 52, 40, 27, 34, 81, 70, 64, 21, 43, 35, 52, 73, 22, 24, 93, 40, 24]
            for p in self.get_players():
                p.participant.vars['nums1'] = nums1
                p.participant.vars['nums2'] = nums2
                p.participant.vars['ans'] = []
                for i in range(0,Constants.num_rounds):
                    p.participant.vars['ans'].append(nums1[i] + nums2[i])
                p.participant.vars['M5_round1Pay'] = 0
                p.participant.vars['n_correct1_M5'] = 0


class Group(BaseGroup):
    def set_payoff(self):
        player_sorted = [[p, p.participant.vars['n_correct1_M5']] for p in self.get_players()]
        player_sorted = sorted(player_sorted, key=lambda x:x[1])

        for i in range(0, Constants.players_per_group):
            cur_player = player_sorted[i][0]
            cur_player.payoff = 0
            cur_player.rank = 3 - i
            if cur_player.participant.vars['roundPred'] == 3 - i:
                print("enter player: ", cur_player)
                cur_player.payoff = 100
            cur_player.payoff += c(player_sorted[i][1] * 150)
            cur_player.participant.vars['M5_round1Pay'] = cur_player.payoff
            cur_player.participant.vars['M5_modelPred'] = cur_player.modelPred


class Player(BasePlayer):
    answer = models.IntegerField() # player answer
    correct = models.IntegerField() # if correct
    n_correct = models.IntegerField() # number of correct
    modelPred = models.IntegerField(choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], widget=widgets.RadioSelect)
    roundPred = models.IntegerField(choices=[1, 2, 3], widget=widgets.RadioSelect)

    rank = models.IntegerField()


    def check_correct(self):
        if self.round_number == 1:
            self.participant.vars['n_correct1_M5'] = 0
        if self.answer == self.participant.vars['ans'][self.round_number-1]:
            self.correct = 1
            self.participant.vars['n_correct1_M5'] += 1
        else:
            self.correct = 0
        self.n_correct = self.participant.vars['n_correct1_M5']


