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
    name_in_url = 'M5_number_add4'
    players_per_group = 3
    num_rounds = 30

    nums1 = [30, 86, 45, 21, 63, 23, 77, 34, 96, 27, 22, 47, 58, 21, 37, 27, 59, 83, 73, 36, 35, 51, 78, 72, 30, 85, 25, 14, 62, 83]
    nums2 = [21, 32, 46, 100, 91, 44, 21, 11, 39, 40, 27, 56, 83, 56, 95, 79, 15, 34, 41, 68, 67, 40, 12, 84, 35, 78, 52, 22, 69, 72]


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.group_randomly()

        for p in self.get_players():
            p.participant.vars['nums1'] = Constants.nums1
            p.participant.vars['nums2'] = Constants.nums2
            p.participant.vars['ans'] = []
            for i in range(0,Constants.num_rounds):
                p.participant.vars['ans'].append(Constants.nums1[i] + Constants.nums2[i])
            if self.round_number == 1:
                p.participant.vars['M5_round4Pay'] = 0
                p.participant.vars['n_correct4_M5'] = 0

class Group(BaseGroup):
    def set_payoff(self):
        player_sorted = [[p, p.participant.vars['n_correct4_M5']] for p in self.get_players()]
        player_sorted = sorted(player_sorted, key=lambda x:x[1])

        for i in range(0, Constants.players_per_group):
            cur_player = player_sorted[i][0]
            cur_player.payoff = 0
            cur_player.rank = 3 - i
            if cur_player.participant.vars['roundPred'] == 3 - i:
                print("enter player: ", cur_player)
                cur_player.payoff = 100
            cur_player.payoff += c(player_sorted[i][1] * 150)
            cur_player.participant.vars['M5_round4Pay'] = cur_player.payoff


class Player(BasePlayer):
    answer = models.IntegerField() # player answer
    correct = models.IntegerField() # if correct
    n_correct = models.IntegerField() # number of correct
    roundPred = models.IntegerField(choices=[1, 2, 3], widget=widgets.RadioSelect)
    modelPred = models.IntegerField()

    rank = models.IntegerField()


    def check_correct(self):
        if self.round_number == 1:
            self.participant.vars['n_correct4_M5'] = 0
        if self.answer == Constants.nums1[self.round_number-1] + Constants.nums2[self.round_number-1]:
            self.correct = 1
            self.participant.vars['n_correct4_M5'] += 1
        else:
            self.correct = 0
        self.n_correct = self.participant.vars['n_correct4_M5']


