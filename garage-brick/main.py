#!/usr/bin/env pybricks-micropython

# The server must be started before the client!
import random
import threading
 
from pybricks.ev3devices import (Motor, InfraredSensor, UltrasonicSensor)
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxClient, TextMailbox
from pybricks.parameters import Port, Button
from pybricks.tools import wait

import constants

# set up the client
client = BluetoothMailboxClient()
mbox = TextMailbox('greeting', client)
client.connect(constants.SERVER)

# set up the ev3
ev3 = EV3Brick()

# set up the speaker
ev3.speaker.set_speech_options('fr', 'm1', 150, 35)
ev3.speaker.beep()

# set up the sensors
ir_sensor = InfraredSensor(Port.S4)
ultrasonic_sensor = UltrasonicSensor(Port.S3)

# set up the motors
back_motor = Motor(Port.B)
treadmill_motor = Motor(Port.A)


# react to infrared signals
def react_to_infrared():
    while True:
        buttons = ir_sensor.keypad()
        if Button.LEFT_UP in buttons:
            mbox.send(constants.SAY_TIME)
        elif Button.RIGHT_UP in buttons:
            mbox.send(constants.OPEN_THE_DOOR)
        elif Button.RIGHT_DOWN in buttons:
            ev3.speaker.play_file(SoundFile.BOING)
            ev3.speaker.play_file(SoundFile.BOING)


# receive message from the house brick
def receive_message():
    while True:
        mbox.wait()
        message = mbox.read()
        if message in constants.ALLOWED_MESSAGES:
            # the surprise distribution can start
            if message == constants.GIVE_SURPRISE:
                # check first time distance
                distance = ultrasonic_sensor.distance()
                has_changed_distance = False
                wait(100)

                # run sound and the back motor (slow because I demolished some chocolates while testing ^^)
                ev3.speaker.play_file(SoundFile.AIR_RELEASE)
                back_motor.run_angle(50, 350)

                # check if the distance has changed, if so run the treadmill for distribution
                # otherwise retry
                while not has_changed_distance:
                    wait(100)
                    current_distance = ultrasonic_sensor.distance()
                    if current_distance != distance:
                        ev3.speaker.play_file(SoundFile.MAGIC_WAND)
                        has_changed_distance = True
                        treadmill_motor.run_time(90, 5000)
                        ev3.speaker.say('Bon appétit')
                        back_motor.run_angle(-50, 250)
                    else:
                        ev3.speaker.play_file(SoundFile.AIR_RELEASE)
                        back_motor.run_angle(50, 350)
            # play some random christmas music
            elif message == constants.ASK_CHRISTMAS_MUSIC:
                ev3.speaker.play_notes(random.choice(constants.CHRISTMAS_SONGS))
            # wish a merry christmas
            elif message == constants.WISH_MERRY_CHRISTMAS:
                ev3.speaker.say("Joyeux Noël")


def main():
    t1 = threading.Thread(target=react_to_infrared, args=())
    t1.start()
    
    t2 = threading.Thread(target=receive_message, args=())
    t2.start()

    while True:
        wait(1000)


main()
