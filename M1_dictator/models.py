from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
One player decides how to divide a certain amount between himself and the other
player.

See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.

"""


class Constants(BaseConstants):
    name_in_url = 'M1_dictator'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'M1_dictator/Instructions.html'

    # Initial amount allocated to the dictator
    endowment = 1000


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    test = models.IntegerField(widget=widgets.TextInput)

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = Constants.endowment - p1.kept
        p2.payoff = p1.kept
        p1.participant.vars['M1_payoff'] = p1.payoff + c(p1.dice_value * 100)
        p2.participant.vars['M1_payoff'] = p2.payoff + c(p2.dice_value * 100)


class Player(BasePlayer):
    kept = models.IntegerField(min=0, max=Constants.endowment,
                               label='decision')
    dice_value = models.IntegerField(min=1, max=6)
