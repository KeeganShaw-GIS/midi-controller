import board
import digitalio
import analogio
import time
import usb_midi
import adafruit_midi

import busio
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from midi_note_map import note_mapping
from organ_display import clear_display
# Import the SSD1306 module.
import adafruit_ssd1306
from analog_pin import scale_analog_in


# ----- Initialize IO -------

# Initialize Midi Ports
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
midi_2 = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=1)

# Create the I2C interface.
i2c = busio.I2C(board.GP17, board.GP16)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# DI Pins - Organ
button_pins = [
    board.GP0,
    board.GP1,
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP7,
    board.GP8,
    board.GP9,
    board.GP10,
    board.GP11,
    board.GP12,
]

# Di Pins - Internal
option_pin = board.GP20

# Di Pins - Internal
control_pins = [
    board.GP13,
    board.GP14,
    board.GP15,
    board.GP19,
]

# Set up buttons
option_btn = digitalio.DigitalInOut(option_pin)
option_btn.direction = digitalio.Direction.INPUT
option_btn.pull = digitalio.Pull.UP
organ_btns = [digitalio.DigitalInOut(bp) for bp in button_pins]
for btn in organ_btns:
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
ctrl_btns = [digitalio.DigitalInOut(bp) for bp in control_pins]
for btn in ctrl_btns:
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP


# Key and trigger states - Organ Pedals
pressed_keys = [False for _ in button_pins]
triggered_keys = [False for _ in button_pins]
tr_key_cnt = [0 for _ in button_pins]

# Key and trigger states - Midi Buttons
pressed_keys_midi = [False for _ in control_pins]
triggered_keys_midi = [False for _ in control_pins]


# Ai Pins - Internal
orgin_vol_pin = analogio.AnalogIn(board.GP28)
orgin_filter_pin = analogio.AnalogIn(board.GP26)
pot_2 = analogio.AnalogIn(board.GP27)

transpose = 0
option_on = False
option_mode = False

# Clear the display.  Always call show after changing pixels to make the display
# update visible!
clear_display(display)
display.text('Play', 0, 20,1,size=1)
display.text('%s' % note_mapping[0], 62, 15,1,size=2)
display.show()

print("MacroPad MIDI Board")

vol =scale_analog_in(orgin_vol_pin)
filter = scale_analog_in(orgin_filter_pin)
showing_vol = False
showing_vol_cnt = 0
showing_filter = False
showing_filter_cnt = 0

last_filter_val = 0
# Run Main Routine
while True:
    new_filt = scale_analog_in(orgin_filter_pin)
    if abs(new_filt-filter) > 4 :
        filter  = new_filt
        print("Frequency %s " % new_filt)
    
    # If volume has
    if showing_vol:
        showing_vol_cnt += 1
    # Only show Volume for 80 cycles
    if showing_filter:
        showing_filter_cnt += 1
    # Only show Filter for 80 cycles
    if showing_vol_cnt > 80:
        showing_vol_cnt = 0
        if option_mode:
            clear_display(display)
            display.text('Options', 0, 20,1,size=1)
            display.text('%s' % note_mapping[0], 62, 15,1,size=2)
            display.show()
        else:
            clear_display(display)
            display.show()
            display.text('Play', 0, 20,1,size=1)
            display.text('%s' % note_mapping[transpose], 62, 15,1,size=2)
            display.show()
        showing_vol = False
    new_vol =scale_analog_in(orgin_vol_pin)
    if abs(vol-new_vol) > 4:
        vol = new_vol
        clear_display(display)
        display.text('Volume', 0, 20,1,size=1)
        display.text(str(vol), 62, 15,1,size=2)
        display.show()
        showing_vol = True
    if not option_btn.value and not option_on:
        option_on = True
        option_mode = not option_mode
        if option_mode:
            clear_display(display)
            display.text('Options', 0, 20,1,size=1)
            display.show()
        else:
            clear_display(display)
            display.text('Play', 0, 20,1,size=1)
            display.text('%s' % note_mapping[transpose], 62, 15,1,size=2)
            display.show()
        print("Option mode - %s" % option_mode)
    if option_btn.value and option_on:
        option_on = False
        print("Option Released")

    for ix, btn in enumerate(organ_btns):
        pressed_keys[ix] = btn.value

    for ix, btn in enumerate(ctrl_btns):
        pressed_keys_midi[ix] = btn.value

    # Organ Buttonns
    for ix, (pk, tk) in enumerate(zip(pressed_keys, triggered_keys)):
        # IF key is pressed (reversed pol) but not yet Triggered
        if not pk and not tk:
            volume = round(vol)
            triggered_keys[ix] = True
            if not option_mode:
                midi.send([NoteOn(48 + ix + transpose, volume )])

            else:
                clear_display(display)
                display.text('Options', 0, 20,1,size=1)
                display.text(note_mapping[ix], 62, 15,1,size=2)
                display.show()
                print("option-organ %s pressed" % ix)
                midi.send([NoteOff(48 + ix + transpose, 0)])
                transpose = ix

        elif pk and tk:
        # IF key is not being pressed (reversed pol)and was triggered
            triggered_keys[ix] = False
            if not option_mode:
                midi.send([NoteOff(48 + ix + transpose, 0)])

    # Midi Buttoons
    for ix, (pk, tk) in enumerate(zip(pressed_keys_midi, triggered_keys_midi)):
        if not pk and not tk:
            triggered_keys_midi[ix] = True
            if not option_mode:
                print("midi %s started" % note_mapping[ix])
                midi_2.send([NoteOn(36 + ix, 127)])
            else:
                print("option-midi %s pressed" % note_mapping[ix])

        elif pk and tk:
            triggered_keys_midi[ix] = False
            if not option_mode:
                print("midi %s stopped" % note_mapping[ix])
                midi_2.send([NoteOff(36 + ix, 0)])


    time.sleep(0.001)
