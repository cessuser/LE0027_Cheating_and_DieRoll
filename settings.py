from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.002,
    'participation_fee': 0.00,
    'doc': "",
}

SESSION_CONFIGS = [
    {
        'name': 'cheating_entitlement',
        'display_name': "Cheating_Entitlement",
        'num_demo_participants': 6,
        'app_sequence': ['M1_dictator', 'M2_die_match', 'M3_die_match_progressive', 'M4_risk_pref', 'M5_number_add1',
                         'M5_number_add2', 'M5_number_add3', 'M5_number_add4', 'M5_number_add5', 'LastModel'],
    },
    {
        'name': 'M1_dictator',
        'display_name': "M1_dictator",
        'num_demo_participants': 2,
        'app_sequence': ['M1_dictator'],
    },
    {
        'name': 'M2_die_match',
        'display_name': "M2_die_match",
        'num_demo_participants': 3,
        'app_sequence': ['M2_die_match'],
    },
    {
        'name': 'M3_die_match',
        'display_name': "M3_die_match",
        'num_demo_participants': 3,
        'app_sequence': ['M3_die_match_progressive'],
    },
    {
        'name': 'M4_risk',
        'display_name': "M4_risk",
        'num_demo_participants': 3,
        'app_sequence': ['M4_risk_pref'],
    },
    {
        'name': 'M5_number_task1',
        'display_name': "M5_number_task1",
        'num_demo_participants': 3,
        'app_sequence': ['M5_number_add1'],
    },
    {
        'name': 'M5_number_task2',
        'display_name': "M5_number_task2",
        'num_demo_participants': 3,
        'app_sequence': ['M5_number_add1', 'M5_number_add2'],
    },
    {
        'name': 'M5_number_task3',
        'display_name': "M5_number_task3",
        'num_demo_participants': 3,
        'app_sequence': ['M5_number_add1', 'M5_number_add3'],
    },
    {
        'name': 'M5_number_task4',
        'display_name': "M5_number_task4",
        'num_demo_participants': 3,
        'app_sequence': ['M5_number_add1', 'M5_number_add4'],
    },
    {
        'name': 'M5_number_task5',
        'display_name': "M5_number_task5",
        'num_demo_participants': 3,
        'app_sequence': ['M5_number_add1', 'M5_number_add5'],
    },
    {
        'name': 'M23',
        'display_name': "M23_test",
        'num_demo_participants': 3,
        'app_sequence': ['M2_die_match', 'M3_die_match_progressive'],
    }

]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True

ROOMS = []


# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# Consider '', None, and '0' to be empty/false
# DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})
DEBUG = 1
DEMO_PAGE_INTRO_HTML = """ """

# don't share this with anybody.
SECRET_KEY = 'wl_6r27l8&3%u4%%=c1h6tdr+k26*d)vl%j8(9!t4ei@-lle8!'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
