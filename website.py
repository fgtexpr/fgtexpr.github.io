from browser import document, html

elements = dict()

def create_canvas():
    canvas = html.CANVAS(width = 680, height = 480)
    ctx = canvas.getContext("webgl")
    if 'canvas' not in elements:
        elements['canvas'] = []
    elements['canvas'].append(canvas)
    ctx.clearColor(1.0, 0.0, 0.0, 0.0, 1.0)
    ctx.clear(ctx.COLOR_BUFFER_BIT)
    return canvas


canv = create_canvas()

document <= canv
