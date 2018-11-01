from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import xlrd
import random
import numpy

author = 'Danlin Chen'

doc = """
match with previous 3 players and multiply 150 ECUs with the outcome 
"""


class Constants(BaseConstants):
    name_in_url = 'M2_die_match'
    players_per_group = 3
    num_rounds = 10
    thrown = [1,2,3,4,5,6]
    reward = [c(100),c(200),c(300),c(400),c(500),c(600)]
    file_location1 = "_static/data/170711_1143.xlsx"
    file_location2 = "_static/data/170711_1334.xlsx"
    file_location3 = "_static/data/170908_1146.xlsx"
    file_location4 = "_static/data/171006_0927.xlsx"

    prob = 0

class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()
        if self.round_number == 1:
            workbook1 = xlrd.open_workbook(Constants.file_location1)
            workbook2 = xlrd.open_workbook(Constants.file_location2)
            workbook3 = xlrd.open_workbook(Constants.file_location3)
            workbook4 = xlrd.open_workbook(Constants.file_location4)
            sheet1 = workbook1.sheet_by_name('170711_1143')
            sheet2 = workbook2.sheet_by_name('170711_1334')
            sheet3 = workbook3.sheet_by_name('170908_1146')
            sheet4 = workbook4.sheet_by_name('171006_0927')
            x1 = []
            x2 = []
            x3 = []
            x4 = []
            groups = [[], [], [], [], [], [], [], [], [], []]
            for value in sheet1.col_values(7):
                if isinstance(value, float):
                    x1.append(int(value))
            for value in sheet2.col_values(7):
                if isinstance(value, float):
                    x2.append(int(value))
            for value in sheet3.col_values(7):
                if isinstance(value, float):
                    x3.append(int(value))
            for value in sheet4.col_values(7):
                if isinstance(value, float):
                    x4.append(int(value))
            print("x1: ", x1)
            index = 0
            while index < len(x1):
                groups[int(index/24)].append(sorted([x1[index], x1[index+1], x1[index+2]]))
                groups[int(index/24)].append(sorted([x2[index], x2[index + 1], x2[index + 2]]))
                groups[int(index/24)].append(sorted([x4[index], x4[index + 1], x4[index + 2]]))
                index += 3
            index = 0
            while index < len(x4):
                groups[int(index/36)].append(sorted([x3[index], x3[index+1], x3[index+2]]))
                index += 3

            for p in self.get_players():
                p.participant.vars['data'] = sorted(x1)
                p.participant.vars['groups'] = groups
                p.participant.vars['dices'] = [random.randint(1,6) for i in range(0, 10)]
                p.participant.vars['all_m2_payoff'] = []
                p.participant.vars['m2_payoff'] = 0
                p.participant.vars['matched_outcomes'] = []
                p.participant.vars['all_declare_gain'] = []


class Group(BaseGroup):

    def set_groupAmount(self, round):
        tot = sum([p.participant.vars['all_declare_gain'][round-1] for p in self.get_players()])
        print('set group amount: ', self.get_players())

        return tot/Constants.players_per_group

    def set_payoff(self):
        for p in self.get_players():
            p.payoff = 0
        dice_sort = [[p, p.real_die_value] for p in self.get_players()]
        dice_sort = sorted(dice_sort, key=lambda x:x[1])
        player_sorted = [0,0,0]
        p1_index = 0
        p2_index = 1
        p3_index = 2
        if dice_sort[0][1] == dice_sort[1][1] and random.randint(0,1): # flip with p2
            temp = p1_index
            p1_index = p2_index
            p2_index= temp
        if dice_sort[0][1] == dice_sort[2][1] and random.randint(0,1): # flip with p3
            temp = p1_index
            p1_index = p3_index
            p3_index = temp
        if dice_sort[1][1] == dice_sort[2][1] and random.randint(0,1):
            temp = p2_index
            p2_index = p3_index
            p3_index = temp
        player_sorted[p1_index] = dice_sort[0][0]
        player_sorted[p2_index] = dice_sort[1][0]
        player_sorted[p3_index] = dice_sort[2][0]

        round_groups = player_sorted[0].participant.vars['groups'][self.round_number-1]
        cur_group = random.sample(round_groups, 1)[0]

        # set matched level & matched payoff
        player_sorted[0].matched_level = '3rd'  # low
        player_sorted[1].matched_level = '2nd'  # medium
        player_sorted[2].matched_level = '1st'  # high

        player_sorted[0].matched_payoff = 150*cur_group[0] #low
        player_sorted[1].matched_payoff = 150*cur_group[1] #medium
        player_sorted[2].matched_payoff = 150*cur_group[2] #high

        player_sorted[0].participant.vars['matched_outcomes'].append(player_sorted[0].matched_payoff)
        player_sorted[1].participant.vars['matched_outcomes'].append(player_sorted[1].matched_payoff)
        player_sorted[2].participant.vars['matched_outcomes'].append(player_sorted[2].matched_payoff)

        print([[p, p.payoff, p.real_die_value] for p in player_sorted])



class Player(BasePlayer):
    real_die_value = models.IntegerField() # virtual dice value report
    chosen_round = models.IntegerField()

    matched_payoff = models.FloatField()
    matched_level = models.StringField()

    declare_gain = models.IntegerField()

    if_deduct = models.BooleanField()

    def check_declare_gain(self):
        self.if_deduct = numpy.random.choice(numpy.array([True, False]), p=[0.1, 0.9])

        if self.if_deduct:
            self.matched_payoff = self.matched_payoff * 0.5
            self.participant.vars['matched_outcomes'][self.round_number - 1] = self.matched_payoff

    def roll_die(self):
        self.real_die_value = random.randint(1,6)
        print(self.real_die_value)

    def set_final_payoff(self):
        self.chosen_round = random.randint(1, Constants.num_rounds)
        groupAmount = self.group.set_groupAmount(self.chosen_round)
        self.payoff = c(self.participant.vars['matched_outcomes'][self.chosen_round-1] - self.participant.vars['all_declare_gain'][self.chosen_round-1]*0.1) + groupAmount
        self.participant.vars['chosen_round_m2'] = self.chosen_round
        self.participant.vars['m2_payoff'] = self.payoff
        print("set final: ", self.matched_payoff, self.payoff, self.participant.vars['matched_outcomes'] )