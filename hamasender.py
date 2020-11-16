#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import sys

gpiopin = 17
repeatcnt = 10

# Other options, depends on the system
#PULSE_S = 450
#PULSE_L = 1400
PULSE_S = 400
PULSE_L = 1200
PULSE_V = 3400

codes = {
    '1_off':   'SSSSVVSSSLSLSLSLSLSLSSSSSLSSSLSSSSSSSSSLSSSSSSSSSSSSSLSLSSSLSSSLSLSLSLSSSLSLSLSLSSSSSSS',
    '1_on':    'SSSSVVSSSLSLSLSLSLSLSSSSSLSSSLSSSSSSSSSLSSSSSSSSSSSSSLSLSSSLSSSLSLSLSLSLSSSSSSSSSLSLSLS',
    '2_off':   'SSSSVVSSSLSLSLSLSLSLSSSSSLSSSLSSSSSSSSSLSSSSSSSSSSSSSLSLSSSLSSSLSLSLSLSLSSSLSLSSSLSSSSS',
    '2_on':    'SSSSVVSSSLSLSLSLSLSLSSSSSLSSSLSSSSSSSSSLSSSSSSSSSSSSSLSLSSSLSSSLSLSLSLSSSLSSSSSLSSSLSLS',
    '3_off':   'SSSSVVSSSLSLSLSLSLSLSSSSSLSSSLSSSSSSSSSLSSSSSSSSSSSSSLSLSSSLSSSLSLSLSLSSSSSLSLSLSLSSSSS',
    '3_on':    'SSSSVVSSSLSLSLSLSLSLSSSSSLSSSLSSSSSSSSSLSSSSSSSSSSSSSLSLSSSLSSSLSLSLSLSLSLSSSSSSSSSLSLS',
    '4_off':   'SSSSVVSSSLSLSLSLSLSLSSSSSLSSSLSSSSSSSSSLSSSSSSSSSSSSSLSLSSSLSSSLSLSLSLSLSLSSSLSSSSSLSSS',
    '4_on':    'SSSSVVSSSLSLSLSLSLSLSSSSSLSSSLSSSSSSSSSLSSSSSSSSSSSSSLSLSSSLSSSLSLSLSLSSSSSLSSSLSLSSSLS',
    'all_off': 'SSSSVVSSSLSLSLSLSLSLSSSSSLSSSLSSSSSSSSSLSSSSSSSSSSSSSLSLSSSLSSSLSLSLSLSSSLSSSLSLSSSLSSS',
    'all_on':  'SSSSVVSSSLSLSLSLSLSLSSSSSLSSSLSSSSSSSSSLSSSSSSSSSSSSSLSLSSSLSSSLSLSLSLSLSSSLSSSSSLSSSLS'
}

def convert_times(code):
    global PULSE_S
    global PULSE_L
    global PULSE_V

    vals = []
    for c in code:
        if c=='S':
            vals.append(PULSE_S)
        elif c=='L':
            vals.append(PULSE_L)
        elif c=='V':
            vals.append(PULSE_V)
        else:
            sys.exit('Invalid code')

    return vals

def send_times(times):
    high = True
    for t in times:

        level = 0
        if high:
            level = 1
        #print("%d %04d" % (level, t))

        GPIO.output(gpiopin, level)
        time.sleep(t / 1000000)
        high = not high

if len(sys.argv) != 3:
    sys.stderr.write('usage: hamasender.py <buttonnr> <on|off>\n')
    sys.exit(1)

buttonnr_list = ['1', '2', '3', '4', 'all']
state_list = ['on', 'off']

buttonnr = sys.argv[1]
state = sys.argv[2]

if not buttonnr in buttonnr_list:
    sys.stderr.write('invalid button nr: "%s"\n' % buttonnr)
    sys.exit(1)

if not state in state_list:
    sys.stderr.write('on or off expected but "%s" found\n' % state)
    sys.exit(1)


key = '%s_%s' % (buttonnr, state)
code = codes[key]
print(code)

times = convert_times(code)

# add sync
times.append(20320)

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpiopin, GPIO.OUT)

for i in range(0, repeatcnt):
    send_times(times)

GPIO.output(gpiopin, 0)
GPIO.cleanup()

