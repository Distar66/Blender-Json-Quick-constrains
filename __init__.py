bl_info = {
    "name": "Json quick constrains",
    "author": "Distar",
    "version": (1, 1,0),
    "blender": (2, 80, 0),
    "description": "Creates animation constrain panels based on Json presets",
    "warning": "",
    "doc_url": "",
    "category": "Animation",
}

import bpy
from .UI_panel import OP_Refresh
from .UI_panel import OBJECT_PT_JsonConstrainPanel
from .generic_constrain import OP_generic_constrain_operator
    

def register():
    bpy.utils.register_class(OBJECT_PT_JsonConstrainPanel)
    bpy.utils.register_class(OP_Refresh)
    bpy.utils.register_class(OP_generic_constrain_operator)

def unregister():
    OP_Refresh.unregister_operators()
    bpy.utils.unregister_class(OP_Refresh)
    bpy.utils.unregister_class(OBJECT_PT_JsonConstrainPanel)
    bpy.utils.unregister_class(OP_generic_constrain_operator)


if __name__ == "__main__":
    register()