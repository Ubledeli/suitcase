from matplotlib.colors import to_hex, to_rgb, hsv_to_rgb, rgb_to_hsv

grays_url = 'https://miro.medium.com/max/1400/1*JV9YdsFrBWYdFVnVPmMpGQ.png'
rainbow_url = 'https://ih1.redbubble.net/image.246747041.4466/st,small,845x845-pad,1000x1000,f8f8f8.u5.jpg'

hues = {
    'purple': '#9b76b2',
    'magenta': '#e186b8',
    'pink': '#f897ab',
    'orange': '#fcb58e',
    'ochre': '#ffce81',
    'yellow': '#fff797',
    'green': '#b4d98a',
    'turquoise': '#7cccb5',
    'cyan': '#62cadc',
    'blue': '#6caada',
}

cold_grays = {
    'cold_black': '#1e2932',
    'cold_gray_dark_3': '#313f4a',
    'cold_gray_dark_2': '#3d4c58',
    'cold_gray_dark_1': '#51606c',
    'cold_gray_dark': '#606e7b',
    'cold_gray_light': '#7a8793',
    'cold_gray_light_1': '#99a5b0',
    'cold_gray_light_2': '#cbd2d9',
    'cold_gray_light_3': '#e4e7eb',
    'cold_white': '#f5f7fa',
}

neutral_grays = {
    'neutral_black': '#222222',
    'neutral_gray_dark_3': '#3b3b3b',
    'neutral_gray_dark_2': '#515151',
    'neutral_gray_dark_1': '#626262',
    'neutral_gray_dark': '#7e7e7e',
    'neutral_gray_light': '#9e9e9e',
    'neutral_gray_light_1': '#b1b1b1',
    'neutral_gray_light_2': '#cfcfcf',
    'neutral_gray_light_3': '#e1e1e1',
    'neutral_white': '#f7f7f7',
}


warm_grays = {
    'warm_black': '#27241d',
    'warm_gray_dark_3': '#423d34',
    'warm_gray_dark_2': '#504a41',
    'warm_gray_dark_1': '#625d53',
    'warm_gray_dark': '#857f73',
    'warm_gray_light': '#a39e94',
    'warm_gray_light_1': '#b8b2a8',
    'warm_gray_light_2': '#d3cec5',
    'warm_gray_light_3': '#e8e6e1',
    'warm_white': '#faf9f7',
}


def merge_dicts(dicts):
    z = dicts[0].copy()  # start with keys and values of x
    for d in dicts[1:]:
        z.update(d)  # modifies z with keys and values of y
    return z


rainbow = {}
for k, v in hues.items():
    h, s, va = rgb_to_hsv(to_rgb(v))
    s += 0.38
    rainbow.update({k: to_hex(hsv_to_rgb((h, s, va)))})
hues = rainbow

colors = merge_dicts([hues, cold_grays, neutral_grays, warm_grays])

if __name__ == '__main__':
    # save(colors)
    # plot_colors()
    print('done')
