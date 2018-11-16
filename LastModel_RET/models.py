from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from django import forms
author = 'Danlin Chen'

doc = """
Your app description
"""
OPTIONS = (
    ("Module1", "module 1"),
    ("Module 2", "module 2"),
    ("Module 3", "module 3"),
)
OPTIONS1 = (
    ("No Major or Pre-College","No Major or Pre-College"),
    ("Arts/Humanities/Education","Arts/Humanities/Education"),
    ("Business/Management (including MBA)","Business/Management (including MBA)"),
    ("Politics","Politics"),
    ("Psychology","Psychology"),
    ("Other Social Sciences","Other Social Sciences"),
    ("Law School (but not pre-law)","Law School (but not pre-law)"),
    ("Medical/Nursing (but not pre-med)","Medical/Nursing (but not pre-med)"),
    ("Math/Engineering/Computer Science/Science","Math/Engineering/Computer Science/Science"),
)


class Constants(BaseConstants):
    name_in_url = 'LastModel_RET'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def set_payoff(self):
        for p in self.get_players():
            p.payoff = 0
        player_lst = [[p, p.participant.vars['M5_round1Pay'] + p.participant.vars['M5_round5Pay']] for p in self.get_players()]
        player_lst = sorted(player_lst, key=lambda x: x[1])
        num_players = len(self.get_players())
        print('player lst', player_lst)
        for i in range(0,len(self.get_players())):
            payoffs = [player_lst[i][0].participant.vars['M5_round1Pay'],
                       player_lst[i][0].participant.vars['M5_round2Pay'],
                       player_lst[i][0].participant.vars['M5_round3Pay'],
                       player_lst[i][0].participant.vars['M5_round4Pay'],
                       player_lst[i][0].participant.vars['M5_round5Pay']]

            print('player id: ', i, ' ', payoffs)
            player_lst[i][0].chosen = random.randint(0,len(payoffs)-1)
            player_lst[i][0].payoff = payoffs[player_lst[i][0].chosen]
            if player_lst[i][0].participant.vars['M5_modelPred'] == 3 and i < num_players/3:
                player_lst[i][0].payoff += 100
            if player_lst[i][0].participant.vars['M5_modelPred'] == 2 and num_players/3 <= i < num_players*2/3:
                player_lst[i][0].payoff += 100
            if player_lst[i][0].participant.vars['M5_modelPred'] == 1 and num_players*2/3<= i < num_players*2/3:
                player_lst[i][0].payoff += 100

            player_lst[i][0].participant.vars['M5_payoff'] = player_lst[i][0].payoff

    def set_final_payoff(self):
        for p in self.get_players():
            p.final_ECUs = 0
            p.final_ECUs = p.participant.vars['M1_payoff'] + p.participant.vars['m2_payoff'] + p.participant.vars['m3_payoff'] \
                       + p.participant.vars['M4_payoff'] + p.participant.vars['M5_payoff']

class Player(BasePlayer):
    final_ECUs = models.CurrencyField()
    payoff = models.CurrencyField()

    chosen = models.IntegerField()

    it1 = models.StringField(choices=["Never justified",
                                      "Rarely justified",
                                      "Sometimes justified",
                                      "Always justified"],
                             label="Avoiding paying the fare on public transport.",
                             widget=widgets.RadioSelect)
    it2 = models.StringField(choices=["Never justified",
                                      "Rarely justified",
                                      "Sometimes justified",
                                      "Always justified"],
                             label="Cheating on taxes if you have a chance.",
                             widget=widgets.RadioSelect)
    it3 = models.StringField(choices=["Never justified",
                                      "Rarely justified",
                                      "Sometimes justified",
                                      "Always justified"],
                             label="Driving faster than the speed limit.",
                             widget=widgets.RadioSelect)
    it4 = models.StringField(choices=["Never justified",
                                      "Rarely justified",
                                      "Sometimes justified",
                                      "Always justified"],
                             label="Keeping money you found in the street",
                             widget=widgets.RadioSelect)
    it5 = models.StringField(choices=["Never justified",
                                      "Rarely justified",
                                      "Sometimes justified",
                                      "Always justified"],
                             label="Lying in your own interests.",
                             widget=widgets.RadioSelect)
    it6 = models.StringField(choices=["Never justified",
                                      "Rarely justified",
                                      "Sometimes justified",
                                      "Always justified"],
                             label=" Not reporting accidental damage you have done to a parked car.",
                             widget=widgets.RadioSelect)
    it7 = models.StringField(choices=["Never justified",
                                      "Rarely justified",
                                      "Sometimes justified",
                                      "Always justified"],
                             label="Throwing away litter in a public place.",
                             widget=widgets.RadioSelect)
    it8 = models.StringField(choices=["Never justified",
                                      "Rarely justified",
                                      "Sometimes justified",
                                      "Always justified"],
                             label="Driving under the influence of alcohol.",
                             widget=widgets.RadioSelect)
    it9 = models.StringField(choices=["Never justified",
                                      "Rarely justified",
                                      "Sometimes justified",
                                      "Always justified"],
                             label=" Making up a job application.",
                             widget=widgets.RadioSelect)
    it10 = models.StringField(choices=["Never justified",
                                       "Rarely justified",
                                       "Sometimes justified",
                                       "Always justified"],
                              label="Buying something you know is stolen.",
                              widget=widgets.RadioSelect)

    age = models.IntegerField()
    student = models.StringField(label='Are you a full-time student?', choices=['Yes', 'No'],
                                 widget=widgets.RadioSelect)
    study = models.StringField(label='What is the highest level of study you have completed?	',
                               choices=["Undergrad 1st year", "Undergrad 2nd year", "Undergrad 3rd year",
                                        "Undergrad 4th year",
                                        "Graduate 1st year", "Graduate 2nd year", "Graduate 3rd year or above"])
    gender = models.StringField(label=" What is your gender?", choices=['Men', 'Women', 'Other'])
    understanding = models.IntegerField(label=" How well did you understand the experimental instructions?",
                                        widget=widgets.RadioSelectHorizontal,
                                        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    understanding_stage = models.StringField(label="",
                                             widget=forms.CheckboxSelectMultiple(choices=OPTIONS), )
    specify_understanding = models.StringField(
        label='Please specify the problem(s) you had in understanding the experimental instructions.',
        widget=widgets.TextInput)
    major = models.StringField(label="",
                               widget=forms.CheckboxSelectMultiple(choices=OPTIONS1))
