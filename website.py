from browser import window, html, document, alert
from Vector import Vector
import math

elements = dict()

graphic_elements = dict()

canv = None

canv_options = {
    'width': 680,
    'height': 680,
    'origin': Vector(0, 0, 0),
    'lightSrc': Vector(300, 300, -10),
    'scale': 20
}

def graph_to_canv(g_coord):
    scale = canv_options['scale']
    offset = canv_options['height']
    return g_coord*scale + Vector(1, 1, 0)*(offset/2)

def canv_to_graph(c_coord):
    scale = canv_options['scale']
    offset = canv_options['height']
    return (c_coord - Vector(1,1,0)*(offset/2))*(1/scale)

def create_canvas(name = None):
    if 'canvas' not in elements:
        elements['canvas'] = []
    if name == None:
        name = 'canv_' + str(len(elements['canvas']))
    canvas = html.CANVAS(id = name, width = canv_options['width'], height = canv_options['height'])
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
    point = graph_to_canv(point)
    ul_corner = Vector(-0.5, 0.5, 0)*height
    ur_corner = Vector(0.5, 0.5, 0)*height
    lr_corner = Vector(0.5, -0.5, 0)*height
    ll_corner = Vector(-0.5, -0.5, 0)*height
    
    unit_normal = unit_normal.normalized()
    
    ul = ul_corner - unit_normal * (ul_corner * unit_normal)
    ur = ur_corner - unit_normal * (ur_corner * unit_normal)
    lr = lr_corner - unit_normal * (lr_corner * unit_normal)
    ll = ll_corner - unit_normal * (ll_corner * unit_normal)

    square = window.Shape3D.new(['M', ul[0], ul[1], ul[2], 'L', ur[0], ur[1], ur[2], lr[0], lr[1], lr[2], ll[0], ll[1], ll[2], 'Z'], 
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
    pt = Vector(point_in[0], point_in[1], point_in[2])
    
    draw_plane(pt, normal, color = 'red', height = canv_options['scale'])
    
    draw_elements(canv, graphic_elements)

def draw_elements(canvas, elements, bg_color = 'aliceblue'):
    canvas.setWorldCoords3D(0, 0, canv_options['width'])
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
    unit_normal = Vector(0.1, 0.2, 0).normalized()
    draw_plane(point, unit_normal)
    draw_elements(canv, graphic_elements)
    alert('testies')

setup()
