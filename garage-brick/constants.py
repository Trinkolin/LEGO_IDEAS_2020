SERVER = 'orange-brick'

JINGLE_BELLS = ['E4/4', 'E4/4', 'E4/2', 'E4/4',
                'E4/4', 'E4/2', 'E4/4', 'G4/4',
                'C4/4.', 'D4/8', 'E4/1']

LET_IT_SNOW = ['B4/8', 'A4/8', 'G4/4', 'G4/8',
               'F4/8', 'E4/4', 'E4/8', 'D4/8',
               'C4/1', 'G3/8', 'G3/8', 'G4/8',
               'G4/8', 'F4/4', 'E4/4', 'D4/8',
               'C4/4', 'G3/1']

CHRISTMAS_SONGS = [
    JINGLE_BELLS,
    LET_IT_SNOW
]

# messages that can be received
ASK_CHRISTMAS_MUSIC = 'ask_christmas_music'
GIVE_SURPRISE = 'give_surprise'
WISH_MERRY_CHRISTMAS = 'ask_we_wish_you_a_merry_christmas_music'

ALLOWED_MESSAGES = [ASK_CHRISTMAS_MUSIC, GIVE_SURPRISE, WISH_MERRY_CHRISTMAS]

# messages that can be sent
OPEN_THE_DOOR = 'open_the_door'
SAY_TIME = 'say_time'