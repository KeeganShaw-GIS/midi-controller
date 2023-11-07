import board
import digitalio
import analogio
import time
import usb_midi
import adafruit_midi

import busio
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.control_change import ControlChange
from midi_note_map import note_mapping, pot_mapping_normal, pot_mapping_opt, drum_idx_map, drum_tracks, pot_mapping_drum
from organ_display import ODisplay
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
    board.GP15,
    board.GP14,
    board.GP13,
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
tr_key_dtime = [0 for _ in button_pins]

# Key and trigger states - Midi Buttons
pressed_ctl_btns = [False for _ in control_pins]
trig_ctl_btns = [False for _ in control_pins]

# Ai Pins - Internal
pots = [analogio.AnalogIn(board.GP28), analogio.AnalogIn(board.GP27), analogio.AnalogIn(board.GP26)]
pot_vals = [scale_analog_in(pot) for pot in pots]
showing_pots_cnt = 0



# init internal vars
transpose = 0
oct_drop = False
drum_track = 0
mode = "Pl"

option_on_flag = False # Flag for denoting option button has been engaged
debounce_time = 0.001 

# ------- Initialize Display --------
o_display = ODisplay(display, "Pl", '%s' % note_mapping[12], "0")


def getNoteNumber(key_idx, transpose, octave_drop, root=48):
    return root + key_idx + transpose - octave_drop*12

print("MacroPad MIDI Board")
# Run Main Routine
while True:
    # Initialize Key Vals
    current_time = time.monotonic()
    for ix, btn in enumerate(organ_btns):
        button_act = not btn.value
        # Button is activated not conditioned
        if button_act and not pressed_keys[ix]:
            # If hasnt started
            if tr_key_dtime[ix] == 0:
                tr_key_dtime[ix] = current_time
            # Mark and clear timer if condition met 
            elif current_time - tr_key_dtime[ix] >= debounce_time:
                pressed_keys[ix] = True
                tr_key_dtime[ix] = 0 
        elif not button_act:
            # Could add a debouce timer on fall too
            pressed_keys[ix] = False

    for ix, btn in enumerate(organ_btns):
        if tr_key_dtime[ix] > 0 and current_time - tr_key_dtime[ix] >= debounce_time:
                pressed_keys[ix] = not btn.value
                tr_key_dtime[ix] = 0


    for ix, btn in enumerate(ctrl_btns):
        pressed_ctl_btns[ix] = not btn.value

    # ---- Handle Opts ----
    # On Click - option_btn.value is fail safe
    if not option_btn.value and not option_on_flag:
        # After Value has been on for more then a scan, d
        if mode == "Pl":
            mode = "Op"
        elif mode == "Op":
            mode = "Dm"
        else:
            mode = "Pl"
        o_display.set_text_1(mode)
        option_on_flag = True
        if mode == "Op" or mode == "Dm" :
            # clear all keys
            for idx, _ in enumerate(button_pins):
                if pressed_keys[idx]:
                    pressed_keys[idx] = False
                if triggered_keys[idx]:
                    triggered_keys[idx] = False
                if pressed_keys[idx] or triggered_keys[idx]:
                    midi.send([NoteOff(getNoteNumber(idx, transpose, oct_drop), 0)])
            if mode == "Op":
                o_display.set_text_2('%s' % note_mapping[transpose+(1-oct_drop)*12])
                o_display.set_text_3('D' if oct_drop else 'N')
            if mode == "Dm":
                o_display.set_text_2(str(drum_track))
                o_display.set_text_3("")
        
        elif mode == "Pl":
            # clear all keys
            for idx, _ in enumerate(control_pins):
                if pressed_ctl_btns[idx]:
                    pressed_ctl_btns[idx] = False
                if trig_ctl_btns[idx]:
                    trig_ctl_btns[idx] = False
                if pressed_ctl_btns[idx] or trig_ctl_btns[idx]:
                    midi_2.send([NoteOff(36 + ix, 0)])
            o_display.set_text_3(str(drum_track))
            o_display.set_text_2('%s' % note_mapping[transpose+(1-oct_drop)*12])
    # On Release - option_btn.value is fail safe
    if option_btn.value and option_on_flag:
        option_on_flag = False


    # Potentiometer Controls
    new_pot_vals = [scale_analog_in(pot) for pot in pots]
    for ix, (nv, v) in enumerate(zip(new_pot_vals, pot_vals)):
        if abs(nv-v) > 4:
            if mode == "Op":
                o_display.set_text_1(pot_mapping_opt[ix][0])
                midi_2.send([ControlChange(pot_mapping_opt[ix][1], nv)])
            elif mode == "Pl":
                o_display.set_text_1(pot_mapping_normal[ix][0])
                midi_2.send([ControlChange(pot_mapping_normal[ix][1], nv)])
            elif mode == "Dm":
                # Fix here
                o_display.set_text_1(pot_mapping_drum[ix][0])
                midi_2.send([ControlChange(pot_mapping_drum[ix][1], nv)])
            o_display.set_text_2(str(nv))
            showing_pots_cnt=1
            pot_vals[ix] = nv
    # Clear Pot controls if they are idle for more than 500 cycles
    if showing_pots_cnt > 0:
        if showing_pots_cnt < 500:
            showing_pots_cnt = showing_pots_cnt + 1
        else:
            o_display.set_text_1(mode)
            if mode == "Op":
                o_display.set_text_2('%s' % note_mapping[transpose+(1-oct_drop)*12])
            elif mode == "Pl":
                o_display.set_text_3(str(drum_track))
                o_display.set_text_2('%s' % note_mapping[transpose+(1-oct_drop)*12])
            elif mode == "Dm":
                o_display.set_text_2(str(drum_track))
            showing_pots_cnt = 0

    # Organ Buttonns
    for ix, (pk, tk) in enumerate(zip(pressed_keys, triggered_keys)):
        # IF key is pressed but not yet Triggered
        if pk and not tk:
            triggered_keys[ix] = True
            if mode == "Pl":
                # print("midi %s started" % getNoteNumber(ix, transpose, oct_drop))
                midi.send([NoteOn(getNoteNumber(ix, transpose, oct_drop), 127 )])
            elif mode == "Op":
                o_display.set_text_2('%s' % note_mapping[ix+(1-oct_drop)*12])
                transpose = ix
            elif mode == "Dm":
                drum_idx = drum_idx_map[ix]
                if (drum_idx > 0):
                    o_display.set_text_2(str(drum_idx))
                    drum_track = ix
                
        elif not pk and tk:
        # IF key is not being pressed and was triggered
            triggered_keys[ix] = False
            if mode == "Pl":
                midi.send([NoteOff(getNoteNumber(ix, transpose, oct_drop), 0)])

    # Control Buttons
    for ix, (pk, tk) in enumerate(zip(pressed_ctl_btns, trig_ctl_btns)):
        if pk and not tk:
            trig_ctl_btns[ix] = True
            if mode == "Pl":
                # Start Drums
                if ix == 2:
                    # print("drum %s started" % drum_tracks[drum_track][0])
                    midi_2.send([NoteOn(drum_tracks[drum_track][0], 127)])
                # Stop Drums
                elif ix == 3:
                    # print("drum %s stopped" % drum_tracks[drum_track][1])
                    midi_2.send([NoteOn(drum_tracks[drum_track][1], 127)])
                else:
                    # print("midi %s started" % note_mapping[ix])
                    midi_2.send([NoteOn(36 + ix, 127)])
            elif mode == "Op":
                if ix == 0:
                    oct_drop = not oct_drop
                    o_display.set_text_3('D' if oct_drop else 'N')
            # else:
                # print("option-midi %s pressed" % note_mapping[ix])

        elif not pk and tk:
            trig_ctl_btns[ix] = False
            if mode == "Pl":
                # Start Drums
                if ix == 2:
                    midi_2.send([NoteOff(drum_tracks[drum_track][0], 0)])
                # Stop Drums
                elif ix == 3:
                    midi_2.send([NoteOff(drum_tracks[drum_track][1], 0)])
                else:
                    midi_2.send([NoteOff(36 + ix, 0)])

