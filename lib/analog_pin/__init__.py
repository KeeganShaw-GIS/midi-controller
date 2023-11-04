def scale_analog_in(vol_pin, min=0, max=127):
    return round((vol_pin.value*(max-min))/65600 + min)