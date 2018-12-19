from browser import document, html

global elements

elements = {}

def create_canvas():
    canvas = document["canv"]
    ctx = canvas.getContext("webgl")
    'canvas' not in elements:
        elements['canvas'] = []
    elements['canvas'].append(canvas)
    ctx.clearColor(0, 0, 0, 0, 1)
    ctx.clear(ctx.COLOR_BUFFER_BIT)
    return canvas


canv = create_canvas()
