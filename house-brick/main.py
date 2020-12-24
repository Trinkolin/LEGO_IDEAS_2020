#!/usr/bin/env pybricks-micropython
import random
import threading

import utime
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor)
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import SoundFile, Font
from pybricks.messaging import BluetoothMailboxServer, TextMailbox
from pybricks.parameters import Port, Direction, Color
from pybricks.tools import wait, DataLog

import constants

# global variables (the robot is restarted everyday so a simple array is enough)
color_scanned_today = []


server = BluetoothMailboxServer()
mbox = TextMailbox('greeting', server)
server.wait_for_connection()

# set up the ev3
ev3 = EV3Brick()

# set up the speaker
ev3.speaker.set_speech_options('fr', 'm1', 150, 35)
ev3.speaker.set_volume(100, which='_all_')
ev3.speaker.beep()

big_font = Font(size=16)

ev3.screen.set_font(big_font)

# set up the sensors
doorbell_sensor = TouchSensor(Port.S1)
color_sensor = ColorSensor(Port.S2)
music_sensor = TouchSensor(Port.S4)
time_sensor = TouchSensor(Port.S3)

# set up the motors
back_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
front_motor = Motor(Port.D)


# check time if top of the clock (say time and run motors if needed)
def check_time(current_hour, h, mi):
    if current_hour != h and mi == 0:
        current_hour = h

        t_say_hour = threading.Thread(target=say_hour, args=(h,))
        t_run_motors = threading.Thread(target=run_motors_for_time)

        t_say_hour.start()
        t_run_motors.start()
    return current_hour


# say hour for thread
def say_hour(h):
    say = 'Il est {} heures.'.format(h)
    ev3.speaker.say(say)


# run motos for thread
def run_motors_for_time():
    # back motor starts
    back_motor.run_time(36, 2900)
    # front motor starts
    front_motor.run_time(83, 10000)
    # back motor stops
    back_motor.run_time(-36, 2900)


# countdown to christmas method
def countdown_to_christmas_time(h, mi, sec):
    countdown_hour = 23 - h
    countdown_min = 59 - mi
    countdown_sec = 59 - sec
    return countdown_hour, countdown_min, countdown_sec


# new sensor needed
def say_time(d, h, mi, sec):
    ev3.speaker.say('Il est {} heures et {} minutes'.format(h, mi))

    if d == 24:
        countdown_hour, countdown_min, countdown_sec = countdown_to_christmas_time(h, mi, sec)
        ev3.speaker.say(
            'Il reste {} et {} minutes avant Noël'.format(countdown_hour, countdown_min))


def draw_christmas_snow():
    ev3.screen.print("          Joy                ")
    ev3.screen.print("                x                    ")
    ev3.screen.print("              _  _                   ")
    ev3.screen.print("            _  _  _                  ")
    ev3.screen.print("          _  _  _  _                 ")
    ev3.screen.print("          [+] | | [+]                ")
    wait(1000)

    ev3.screen.clear()

    ev3.screen.print("          Joyeux                     ")
    ev3.screen.print("      *         x                    ")
    ev3.screen.print("              _  _       *           ")
    ev3.screen.print("            _  _  _          *       ")
    ev3.screen.print("  *       _  _  _  _                 ")
    ev3.screen.print("          [+] | | [+]                ")
    wait(1000)

    ev3.screen.clear()

    ev3.screen.print("          Joyeux No                  ")
    ev3.screen.print("  *             x           *        ")
    ev3.screen.print("         *    _  _                   ")
    ev3.screen.print("            _  _  _     *            ")
    ev3.screen.print("   *      _  _  _  _                 ")
    ev3.screen.print("          [+] | | [+]         *      ")

    wait(1000)
    ev3.screen.clear()

    ev3.screen.print("          Joyeux Noël                ")
    ev3.screen.print("*               x           *        ")
    ev3.screen.print("         *    _  _                   ")
    ev3.screen.print("            _  _  _       *          ")
    ev3.screen.print("   *       _  _  _  _         *      ")
    ev3.screen.print("          [+] | | [+]      *         ")


# greet color for m and d
def greet_color_selected(m, d):
    wait(100)
    color = color_sensor.color()

    if ((color in constants.POSSIBLE_COLORS and color not in color_scanned_today) or (
            color not in constants.POSSIBLE_COLORS)):
        ev3.speaker.say('Bienvenue! Place - toi devant le scan de couleur')

    while color not in constants.POSSIBLE_COLORS:
        color = color_sensor.color()

    ev3.speaker.play_file(SoundFile.MAGIC_WAND)
    ev3.screen.clear()
    ev3.screen.draw_text(5, 5, 'Ta couleur est le {}'.format(color))

    if color not in color_scanned_today:
        ev3.speaker.say("Bonjour {}".format(constants.COLOR_PERSON[color]))

        # count down month / day and say how many days are remaining
        if m == 12:
            ev3.speaker.say('Nous sommes le {} décembre.'.format(d))
            if d in constants.EVENTS:
                ev3.speaker.say(constants.EVENTS[d])
            ev3.speaker.say('Il reste {} jours avant Noël '.format(25 - d))
        else:
            count_month = 12 - m
            ev3.speaker.say("Il reste {} avant Noël".format(count_month))

        # Check event for Color people
        if color in constants.COLOR_EVENTS:
            events_color = constants.COLOR_EVENTS[color]
            if d in events_color:
                ev3.speaker.say(events_color[d])

        # Ask the surprise to be given
        ev3.speaker.play_file(SoundFile.HORN_1)
        mbox.send("give_surprise")

        color_scanned_today.append(color)
    else:
        # the color person has already got the surprise
        ev3.speaker.play_file(SoundFile.GENERAL_ALERT)
        ev3.speaker.say(random.choice(constants.SAY_RANDOM_ALREADY_SCANNED))


# listen for messages
def listen_message(current_hour):
    while True:
        mbox.wait()
        message = mbox.read()
        if message in constants.ALLOWED_MESSAGES:
            if message == constants.SAY_TIME:
                y, m, d, h, mi, sec = utime.localtime()[0:6]
                if h == 23:
                    d = d + 1
                    h = 0
                else:
                    h = h + 1
                if m == 0:
                    current_hour = check_time(current_hour, h, mi)
                say_time(d, h, mi, sec)
            elif message == constants.OPEN_THE_DOOR:
                y, m, d, h, mi, sec = utime.localtime()[0:6]
                if h == 23:
                    d = d + 1
                greet_color_selected(m, d)


# check for user action and time
def check_user_action(current_hour):
    has_been_completely_scanned = False

    while True:
        wait(100)

        # check time each second
        y, m, d, h, mi, sec = utime.localtime()[0:6]
        # adjust time to europe
        if h == 23:
            d = d + 1
            h = 0
        else:
            h = h + 1

        # check time for top of clock and update current hour is needed
        current_hour = check_time(current_hour, h, mi)

        # only if not everybody has gotten its surprise
        if not has_been_completely_scanned:
            if doorbell_sensor.pressed():
                ev3.speaker.play_file(SoundFile.BOING)
                ev3.speaker.play_file(SoundFile.BOING)
                greet_color_selected(m, d)

        # check if music sensor has been pressed for christmas music
        if music_sensor.pressed():
            wait(100)
            mbox.send("ask_christmas_music")

        # check if time sensor has been pressed for telling time
        if time_sensor.pressed():
            say_time(d, h, mi, sec)

        # only if it's christmas eve
        if d == 24:
            countdown_hour, countdown_min, countdown_sec = countdown_to_christmas_time(h, mi, sec)
            if countdown_hour == 0:
                if countdown_min == 0:
                    ev3.speaker.say('Il reste {} secondes avant Noël'.format(countdown_sec))
                    wait(countdown_sec * 1000)
                    mbox.send("ask_we_wish_you_a_merry_christmas_music")
                else:
                    ev3.speaker.say('Il reste {} minutes avant Noël'.format(countdown_min))


def main():
    current_hour = 0
    t1 = threading.Thread(target=listen_message, args=(current_hour,))
    t1.start()

    t2 = threading.Thread(target=check_user_action, args=(current_hour,))
    t2.start()

    while True:
        wait(1000)


# Launch main method
main()
