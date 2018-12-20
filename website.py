from browser import window, html, document
from Vector import Vector
import math

elements = dict()

graphic_elements = dict()

def create_canvas():
    if 'canvas' not in elements:
        elements['canvas'] = []
    n_canvs = len(elements['canvas'])
    canvas = html.CANVAS(id = "canv_" + str(n_canvs), width = 680, height = 480)
    document <= canvas
    canvas = window.Cango3D.new("canv_" + str(n_canvs))
    elements['canvas'].append(canvas)
    return canvas

def draw_plane(point, unit_normal, height = 30, color = "blue"):
    square = window.Shape3D.new(window.shapeDefs3D.square(height), 
            {'fillColor': color, 'backColor': color}
            )

    square.transform.translate(point[0], point[1], point[2])
    
    axis = unit_normal % Vector(0, 0, 1)
    angle = unit_normal * Vector(0, 0, 1)

    square.rotate(axis[0], axis[1], axis[2], math.degrees(math.acos(angle)) )
    #square.rotate(1.0, 0.0, 0.0, math.radians(math.acos(angle)))

    if 'square' not in graphic_elements:
        graphic_elements['square'] = []

    graphic_elements['square'].append(square)
    return square

def draw_elements(canvas, elements, bg_color = 'aliceblue'):
    canvas.setWorldCoords3D(0, 0, 500)
    canvas.setPropertyDefault("backgroundColor", bg_color)
    canvas.setLightSource(0, -100, 50)
    for element_type in elements:
        for e in elements[element_type]:
            canvas.render(e)


def setup():
    canv = create_canvas()
    point = Vector(100, 200, 1)
    unit_normal = Vector(0.3, 0.3, 0.2).normalized()
    draw_plane(point, unit_normal)
    draw_elements(canv, graphic_elements)

setup()
