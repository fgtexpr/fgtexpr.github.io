from browser import window, html, document, alert
from Vector import Vector
from patch import Patch
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

def plane_vertices(point, unit_normal, height = 30, color = "blue"):
    ul_corner = Vector(-0.5, 0.5, 0)*height
    ur_corner = Vector(0.5, 0.5, 0)*height
    lr_corner = Vector(0.5, -0.5, 0)*height
    ll_corner = Vector(-0.5, -0.5, 0)*height
    
    unit_normal = unit_normal.normalized()
    ul = point + ul_corner - unit_normal * (ul_corner * unit_normal)
    ur = point + ur_corner - unit_normal * (ur_corner * unit_normal)
    lr = point + lr_corner - unit_normal * (lr_corner * unit_normal)
    ll = point + ll_corner - unit_normal * (ll_corner * unit_normal)
    
    return [ul, ur, lr, lr, ll, ul]

def render_as_planes(points, normals):
    # two triangles per point, 3 vertices per triangle
    verts = [None for _ in range(6*len(points))]

    for i in range(len(points)):
        point_verts = plane_vertices(points[i], normals[i])
        for j in range(6):
            verts[6*i + j] = point_verts[j]
    alert(verts)
    alert(verts[0])
    verts = window.Float32Array.new(verts)
    
    geometry = window.THREE.BufferGeometry.new()
    geometry.addAttribute('position', window.THREE.BufferAttribute.new(verts, 3))
    mat = window.THREE.MeshBasicMaterial.new( {'color': 0xff0000 } )
    mesh = window.THREE.Mesh.new(geometry, mat)

    renderer = window.THREE.WebGLRenderer.new()
    renderer.setSize(800, 600)
    document <= renderer.domElement
    alert('verts placed')
    
    scene = window.THREE.Scene.new()
    camera = window.THREE.PerspectiveCamera.new(45, 800/600, 1, 1000)
    alert('cam created')


    scene.add(mesh)

    alert('mesh added')
    renderer.render(scene, camera)

def create_function_from_input(inp):
    func_text = document[inp].value
    def call(u, v):
        return exec(func_text)
    return call

def draw_patch(ev):
    fx = create_function_from_input('fx')
    fy = create_function_from_input('fy')
    fz = create_function_from_input('fz')
    pth = Patch.create(fx, fy, fz)
    
    u_min = float(document['umin'].value)
    u_max = float(document['umax'].value)
    v_min = float(document['vmin'].value)
    v_max = float(document['vmax'].value)

    u_step = float(document['ustep'].value)
    v_step = float(document['vstep'].value)
    
    u_width = int((u_max - u_min)/u_step)
    v_width = int((v_max - v_min)/v_step)

    uv_points = [Vector(u_min + u_step*u, v_min + v_step*v) for u in range(u_width) for v in range(v_width)]
    
    xyz_points = [pth(pt) for pt in uv_points]
    normals = [pth(pt) for pt in uv_points]
    
    render_as_planes(xyz_points, normals)

def setup():
    ##Create inputs for fx, fy, fz
    alert('ahh')
    create_input('text', 'fx')
    create_input('text', 'fy')
    create_input('text', 'fz')
    create_input('text', 'umin')
    create_input('text', 'umax')
    create_input('text', 'vmin')
    create_input('text', 'vmax')
    create_input('text', 'ustep')
    create_input('text', 'vstep')

    create_button('go').bind('click', draw_patch)
    
setup()
