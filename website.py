from browser import window, html, document, alert
from Vector import Vector
from sphere import Sphere
import math
from math import *
elements = dict()

graphic_elements = dict()

canv = None

canv_options = {
    'width': 680,
    'height': 680,
    'origin': Vector(0, 0, 0),
    'lightSrc': Vector(300, 300, -10),
    'scale': 100
}

def create_canvas(name = None):
    if 'canvas' not in elements:
        elements['canvas'] = []
    if name == None:
        name = 'canv_' + str(len(elements['canvas']))
    canvas = html.CANVAS(id = name, width = canv_options['width'], height = canv_options['height'])
    document <= canvas
    #TODO

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

    #TODO

def create_function_from_input(inp):
    func_text = document[inp].value
    def call(u, v):
        return exec(func_text)
    return call

def create_patch(ev):
    fx = create_function_from_input('fx')
    fy = create_function_from_input('fy')
    fz = create_function_from_input('fz')
    pth = Patch.create(fx, fy, fz)
    alert(pth(Vector(0,0)))
    alert(pth(Vector(0,1)))
    alert(pth(Vector(1,0)))

def setup():
    ##Create inputs for fx, fy, fz
    create_input('text', 'fx')
    create_input('text', 'fy')
    create_input('text', 'fz')
    create_button('go').bind('click', create_patch)
    
setup()
