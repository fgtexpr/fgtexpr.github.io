from browser import window, html, document
from Vector import Vector
import math

elements = dict()

graphic_elements = dict()

canv = None
def create_canvas(name = None):
    if 'canvas' not in elements:
        elements['canvas'] = []
    if name == None:
        name = 'canv_' + str(len(elements['canvas']))
    canvas = html.CANVAS(id = name, width = 680, height = 480)
    document <= canvas
    canvas = window.Cango3D.new(name)
    elements['canvas'].append(canvas)
    return canvas

def create_input(tpe, name = None):
    if 'input' not in elements:
        elements['input'] = []
    if name == None:
        name = 'input_' + str(len(elements['input']))

    inp = html.INPUT(type = tpe, id = name)

    document <= inp
    elements['input'].append(inp)
    
    return inp

def create_button(name = None):
    if 'button' not in elements:
        elements['button'] = []
    if name == None:
        name = 'button_' + str(len(elements['button']))
    
    btn = html.BUTTON(id = name)

    document <= btn
    elements['button'].append(btn)
    return btn

def draw_plane(point, unit_normal, height = 30, color = "blue"):
    ul_corner = Vector(-0.5,0.5,0)
    ur_corner = Vector(0.5, 0.5, 0)
    lr_corner = Vector(0.5, -0.5, 0)
    ll_corner = Vector(-0.5, -0.5, 0)
        
    p_ul = ul_corner - ( (ul_corner * unit_normal) * unit_normal)
    p_ur = ur_corner - ( (ur_corner * unit_normal) * unit_normal)
    p_lr = lr_corner - ( (lr_corner * unit_normal) * unit_normal)
    p_ll = ll_corner - ( (ll_corner * unit_normal) * unit_normal)

    



    square = window.Shape3D.new(['M'] + list(p_ul) + ['l'] + list(p_ur) + list(p_lr) + list(p_ll) + ['z'], 
            {'fillColor': color, 'backColor': color}
            )

    square.transform.translate(point[0], point[1], point[2])

    if 'square' not in graphic_elements:
        graphic_elements['square'] = []

    graphic_elements['square'].append(square)
    return square

def action_draw_plane(ev):
    n_in = list( map( float, document['normal_input'].value.split(',') ) )
    point_in = list( map( float, document['point_input'].value.split(',')))

    normal = Vector(n_in[0], n_in[1], n_in[2]).normalized()
    pt = Vector(point_in[0], point_in[1], point_in[2]).normalized()
    
    draw_plane(pt, normal, color = 'red')
    
    draw_elements(canv, graphic_elements)

def draw_elements(canvas, elements, bg_color = 'aliceblue'):
    canvas.setWorldCoords3D(0, 0, 500)
    canvas.setPropertyDefault("backgroundColor", bg_color)
    canvas.setLightSource(0, -100, 50)
    for element_type in elements:
        for e in elements[element_type]:
            canvas.render(e)


def setup():
    global canv
    canv = create_canvas()
    create_input('text', name = 'normal_input')
    create_input('text', name = 'point_input')
    create_button().bind('click', action_draw_plane)
    point = Vector(100, 200, 1)
    unit_normal = Vector(0.1, 0.2, 0.4).normalized()
    draw_plane(point, unit_normal)
    draw_elements(canv, graphic_elements)
    


setup()
