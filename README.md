# midi-controller

Inspired by Benj of the [mayhemingways](https://youtu.be/ROnXihaXhZg?feature=shared&t=181). A toy that lets you play base while you do other things with your hands! Like write code. 

A midi controller built from an 12 key old organ foot pedal and Some momentary pushbuttons, a SSD1306 Display, and a few 10K pots. Designed to send notes to a synth (Fluid synth on a raspberry PI). That control Bass, and Drums. 

Features:
- 3 Pots, send reserved CC for volume (7, 9) , reverb (??), drum temp
- Option Button - Play, Options, Drum Select Modes
- Drop full Octave Button - Drops a full octave!
- Increment / Decrement Patch Buttons - Programmable on Fluid Synth (36-37)
- Drum Track Play and Stop - (CC 100 to 108 to play , and CC 109-117 to stop) Value is determined by selected drum track
- Transpose Key with option selector (Option Button -> Note you want to transpose to ----> Puts that not in the Low C position)
- Select Drum Track with option selector (Option Button x2 -> Select Track 1-8 (White Keys) ----> Drum Play and )

How To Use:
1. Get a raspberry Pi Pico (with headers if you don't solder).
2. Find an old organ with a foot pedal board. Or build your own with a twister mat. I dont care. 
4. Install Circuit Py.
5. Copy Code and Libs folder.
6. Get wiring!
7. Coming Soon.... A circuit diagram. 
