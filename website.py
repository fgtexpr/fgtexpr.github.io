from browser import window, html, document

elements = dict()

def create_canvas():
    canvas = html.CANVAS(id = "canv", width = 680, height = 480)
    if 'canvas' not in elements:
        elements['canvas'] = []
    elements['canvas'].append(canvas)
    return canvas


canv = create_canvas()

document <= canv
