import random as rd

def random_dark_color():
    r = rd.random()
    g = rd.random()
    b = rd.random()
    if r+g+b<2 and r+g+b>0.5:
        return (r, g, b)
    else:
        return random_dark_color()

def differentiable(color_a, color_b, difference):
    for i in range(3):
        if abs(color_a[i]-color_b[i])>difference:
            return True
    return False

def random_dark_colors(size):
    colors = []
    for i in range(size):
        color = random_dark_color()
        while False in [differentiable(color, _, 1/size**(1/2)) for _ in colors]:
            color = random_dark_color()
        colors.append(color)
    return colors
