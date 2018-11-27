from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import numpy

author = 'Danlin Chen'

doc = """
Risk Preference
"""


class Constants(BaseConstants):
    name_in_url = 'M4_risk_pref'
    players_per_group = None
    num_rounds = 1
    risk_choices_A = (2, 1.6)
    risk_choices_B = (3.85, 0.1)

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    selected_choice = models.IntegerField(min=1, max=11)
    selected_prob = models.IntegerField()
    option1 = models.StringField(choices=['A', 'B'], widget=widgets.RadioSelect)
    option2 = models.StringField(choices=['A', 'B'], widget=widgets.RadioSelect)
    option3 = models.StringField(choices=['A', 'B'], widget=widgets.RadioSelect)
    option4 = models.StringField(choices=['A', 'B'], widget=widgets.RadioSelect)
    option5 = models.StringField(choices=['A', 'B'], widget=widgets.RadioSelect)
    option6 = models.StringField(choices=['A', 'B'], widget=widgets.RadioSelect)
    option7 = models.StringField(choices=['A', 'B'], widget=widgets.RadioSelect)
    option8 = models.StringField(choices=['A', 'B'], widget=widgets.RadioSelect)
    option9 = models.StringField(choices=['A', 'B'], widget=widgets.RadioSelect)
    option10 = models.StringField(choices=['A', 'B'], widget=widgets.RadioSelect)
    option11 = models.StringField(choices=['A', 'B'], widget=widgets.RadioSelect)

    def set_payoff(self):
        self.payoff = 0
        choices = [self.option1, self.option2, self.option3, self.option4, self.option5, self.option6, self.option7,
                   self.option8, self.option9, self.option10, self.option11]
        self.selected_choice = random.randint(1, 11)
        probA = 100 - (self.selected_choice-1)*10
        probB = 100 - probA
        probA = probA / 100.0
        probB = probB / 100.0
        temp_pay = 0
        if choices[self.selected_choice-1] == 'A':
            temp_pay = numpy.random.choice(numpy.array([1.6, 2]), p=[probA, probB]) / self.session.config['real_world_currency_per_point']
        if choices[self.selected_choice-1] == 'B':
            temp_pay = numpy.random.choice(numpy.array([0.1, 3.85]), p=[probA, probB]) / self.session.config['real_world_currency_per_point']
        self.payoff = temp_pay
        self.participant.vars['M4_payoff'] = self.payoff
        self.participant.vars['M4_payoff_real_currency'] = self.payoff * self.session.config['real_world_currency_per_point']





