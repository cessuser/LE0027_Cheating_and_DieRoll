from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import xlrd
import random
author = 'Danlin Chen'

doc = """
match with previous 3 players and multiply 150 ECUs with the outcome 
"""


class Constants(BaseConstants):
    name_in_url = 'M3_die_match_progressive_dieroll'
    players_per_group = 3
    num_rounds = 10
    thrown = [1,2,3,4,5,6]
    reward = [100,200,300,400,500,600]
    file_location1 = "_static/data/M3_170811_1231.xlsx"
    file_location2 = "_static/data/M3_170823_1534.xlsx"
    file_location3 = "_static/data/M3_170908_1004.xlsx"
    file_location4 = "_static/data/M3_171005_1029.xlsx"

class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()
        if self.round_number == 1:
            workbook1 = xlrd.open_workbook(Constants.file_location1)
            workbook2 = xlrd.open_workbook(Constants.file_location2)
            workbook3 = xlrd.open_workbook(Constants.file_location3)
            workbook4 = xlrd.open_workbook(Constants.file_location4)
            sheet1 = workbook1.sheet_by_name('170811_1231')
            sheet2 = workbook2.sheet_by_name('170823_1534')
            sheet3 = workbook3.sheet_by_name('170908_1004')
            sheet4 = workbook4.sheet_by_name('171005_1029')
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
            index = 0
            while index < len(x1):
                groups[int(index/24)].append(sorted([x1[index], x1[index+1], x1[index+2]]))
                groups[int(index/24)].append(sorted([x2[index], x2[index + 1], x2[index + 2]]))
                groups[int(index/24)].append(sorted([x4[index], x4[index + 1], x4[index + 2]]))
                index += 3
            index = 0
            while index < len(x3):
                groups[int(index/36)].append(sorted([x3[index], x3[index+1], x3[index+2]]))
                index += 3

            for p in self.get_players():
                p.participant.vars['data'] = sorted(x1)
                p.participant.vars['groups'] = groups
                p.participant.vars['dices'] = [random.randint(1,6) for i in range(0, 10)]
                p.participant.vars['all_m3_payoff'] = []
                p.participant.vars['m2_payoff'] = 0
                p.roundPred_correct = False
                p.modelPred_correct = False
                p.participant.vars['matched_outcomes'] = []



class Group(BaseGroup):
    def set_final_payoff(self):
        player_pred = [[p, sum(p.participant.vars['matched_outcomes'])] for p in self.get_players()]
        player_pred = sorted(player_pred, key=lambda x: x[1], reverse=True)

        player_pred[0].append(1)
        player_pred[1].append(2)
        player_pred[2].append(3)


        if player_pred[0][0].modelPred == 1:
            player_pred[0][0].modelPred_correct = True
        if player_pred[1][0].modelPred == 2:
            player_pred[1][0].modelPred_correct = True
        if player_pred[2][0].modelPred == 3:
            player_pred[2][0].modelPred_correct = True

        for i in range(0,3):
            cur_player = player_pred[i][0]
            cur_player.payoff = 0
            cur_player.modelPred = False
            if cur_player.modelPred == i + 1:
                cur_player.modelPred_correct = True
            cur_player.chosen_round = random.randint(1, Constants.num_rounds)
            if cur_player.modelPred_correct:
                cur_player.payoff = cur_player.participant.vars['all_m3_payoff'][cur_player.chosen_round - 1] + 100
            else:
                cur_player.payoff = cur_player.participant.vars['all_m3_payoff'][cur_player.chosen_round - 1]

            cur_player.participant.vars['m3_payoff'] = cur_player.payoff





    def set_payoff(self):
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

        for i in range(0,3):
            cur_player = player_sorted[i]
            cur_player.payoff = 0
            cur_player.matched_payoff = 150 * cur_group[i]
            cur_player.participant.vars['matched_outcomes'].append(cur_player.matched_payoff)
            cur_player.payoff = cur_player.matched_payoff
            if cur_player.roundPred == Constants.players_per_group-i:
                cur_player.payoff += 100
                cur_player.roundPred_correct = True



class Player(BasePlayer):
    real_die_value = models.IntegerField() # virtual dice value report
    modelPred = models.IntegerField(choices=[(1, 'Top Third'), (2, 'Middle Third'), (3, 'Bottom Thrid')], widget=widgets.RadioSelect)
    roundPred = models.IntegerField(choices=[1, 2, 3], widget=widgets.RadioSelect)
    chosen_round = models.IntegerField()
    roundPred_correct = models.BooleanField()
    modelPred_correct = models.BooleanField()
    matched_payoff = models.IntegerField()
    matched_level = models.StringField()

    dice_value = models.IntegerField(min=1, max=6)

    def roll_die(self):
        self.real_die_value = random.randint(1,6)
