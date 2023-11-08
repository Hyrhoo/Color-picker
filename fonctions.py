
def rgb_to_hex(r: int, g: int, b: int):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hex_to_rgb(hex: str):
    hex.strip("#")
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)  
    return tuple(rgb)

def hsv_to_rgb(h: float, s: float, v: float):
    c = v * s
    x = c * (1 - abs((h/60) % 2 - 1))
    m = v - c
    if 0 <= h < 60 or h == 360:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    elif 300 <= h < 360:
        r, g, b = c, 0, x
    return (int((r+m)*255), int((g+m)*255), int((b+m)*255))

def rgb_to_hsv(r: int, g: int, b: int):
    r1, g1, b1 = map(lambda x: x/255, (r, g, b))
    cmax = max(r1, g1, b1)
    cmin = min (r1, g1, b1)
    delta = cmax - cmin

    hue = get_hue(r1, g1, b1, cmax, delta)
    saturation = get_saturation(cmax, delta)
    value = cmax
    
    return hue, saturation, value

def get_hue(r: float, g: float, b: float, cmax: float, delta: float):
    if delta == 0:
        return 0.0
    if cmax == r:
        return 60 * ((g - b)/delta % 6)
    if cmax == g:
        return 60 * ((b - r)/delta + 2)
    if cmax == b:
        return 60 * ((r - g)/delta + 4)


def get_saturation(cmax: float, delta: float):
    if cmax == 0:
        return 0.0
    return delta / cmax


def lighten_color(rgb_color, additive_value):
    return_color = []
    return_color.append(round(((255 - rgb_color[0])/255) * additive_value) + rgb_color[0])
    return_color.append(round(((255 - rgb_color[1])/255) * additive_value) + rgb_color[1])
    return_color.append(round(((255 - rgb_color[2])/255) * additive_value) + rgb_color[2])
    return tuple(return_color)

def darken_color(rgb_color, subtractive_value):
    return_color = []
    return_color.append(round((rgb_color[0]/255) * (255-subtractive_value)))
    return_color.append(round((rgb_color[1]/255) * (255-subtractive_value)))
    return_color.append(round((rgb_color[2]/255) * (255-subtractive_value)))
    return tuple(return_color)
