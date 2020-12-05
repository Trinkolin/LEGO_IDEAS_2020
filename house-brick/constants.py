from pybricks.parameters import Color

# general constants
BONNE_FETE = 'Bonne fête'

EVENTS = {6: 'Joyeuse Saint Nicolas',
          24: 'Nous sommes la veille de Noël',
          25: 'Joyeux Noël'}

# customized constants
RED_IS = 'Lulu'
BLUE_IS = 'Fifi'
YELLOW_IS = 'Toto'

EVENTS_RED_PERSON = {5: BONNE_FETE}
EVENTS_BLUE_PERSON = {5: BONNE_FETE}
EVENTS_YELLOW_PERSON = {5: BONNE_FETE}

COLOR_EVENTS = {Color.RED: EVENTS_RED_PERSON, Color.BLUE: EVENTS_BLUE_PERSON, Color.YELLOW: EVENTS_YELLOW_PERSON}

SAY_RANDOM_ALREADY_SCANNED = ["Tu es déjà venu aujourd'hui"]

POSSIBLE_COLORS = [Color.RED, Color.BLUE, Color.YELLOW]
COLOR_PERSON = {Color.RED: RED_IS, Color.BLUE: BLUE_IS, Color.YELLOW: YELLOW_IS}

SAY_TIME = 'say_time'
OPEN_THE_DOOR = 'open_the_door'

ALLOWED_MESSAGES = [SAY_TIME, OPEN_THE_DOOR]

