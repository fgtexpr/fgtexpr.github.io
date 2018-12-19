from browser import window, html, document
from vector import Vector

elements = dict()

graphic_elements = dict()

def create_canvas():
    if 'canvas' not in elements:
        elements['canvas'] = []
    n_canvs = len(elements['canvas'])
    canvas = html.CANVAS(id = "canv_" + n_canvs, width = 680, height = 480)
    document <= canvas
    canvas = window.Cango3D.new("canv_" + n_canvs)
    elements['canvas'].append(canvas)
    return canvas

def draw_plane(point, unit_normal, height = 1, color = "red"):
    square = window.Shape3D.new(window.shapeDefs3D.square(height), 
            {'fillColor': color, 'backColor': color}
            )

    square.transform.translate(point[0], point[1], point[2])
    
    b1 = unit_normal.cross((unit_normal + Vector(0.1, 0, 0)).normalized() )
    b2 = unit_normal.cross(b1)

    square.transform.rotate(b1[0], b1[1], b1[2], b2 * Vector(0, 0, 1))
    square.transform.rotate(b2[0], b2[1], b2[2], b1 * Vector(1, 0, 0))
    
    if 'square' not in graphic_elements:
        graphic_elements['square'] = []

    graphic_elements['square'].append(square)
    return square

def draw_elements(canvas, elements, bg_color = 'aliceblue'):
    canvas.setWorldCoords3D(0, 0, 0, 0)
    canvas.setLightSource(0, 0, -100)
    for element_type in elements:
        for e in elements[element_type]:
            canvas.render(e)


def setup():
    canv = create_canvas()
    point = Vector3(5, 0, 1)
    unit_normal = Vector3(-1, 1, 0)
    draw_plane(point, unit_normal)
    draw_elements(canv, graphic_elements)

setup()
