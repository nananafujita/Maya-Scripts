import maya.cmds as cmds

def create_window():
    if cmds.window("Shader Preview", exists=True):
        cmds.deleteUI("Shader Preview")
    window = cmds.window(title="Shader Preview")
    cmds.showWindow(window")
    
"""

def create_preview(shader_name, color(1,0, 0)):
    sphere = cmds.sphere(r=10)
    
    shading_node = cmds.shadingNode(shader_name, asShader=True)
    shading_group = cmds.setAttr(shading_node + ".color", *color, type="double3")
    
    cmds.select(sphere)
    cmds.hyperShade(assign=shading_node)
    
    return sphere, shading_node
    
def add_lighting():
    light = cmds.directionalLight(rgb=(1, 1, 1))
    cmds.setAttr(light + ".rotateX", -45)
    cmds.setAttr(light + ".rotateY", 45)
    return light

"""
    
create_window()