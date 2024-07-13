bl_info = {
    "name": "Json quick constrains",
    "author": "Distar",
    "version": (1, 2,1),
    "blender": (2, 80, 0),
    "description": "Creates animation constrain panels based on Json presets",
    "warning": "",
    "doc_url": "",
    "category": "Animation",
}

import bpy
from .UI_panel import OP_Refresh
from .UI_panel import OBJECT_PT_JsonConstrainPanel
from .UI_panel import OP_Refresh
from .UI_panel import OP_SaveToCharacter
from .generic_constrain import OP_generic_constrain_operator
    

def register():
    bpy.utils.register_class(OBJECT_PT_JsonConstrainPanel)
    bpy.utils.register_class(OP_Refresh)
    bpy.utils.register_class(OP_generic_constrain_operator)
    bpy.utils.register_class(OP_SaveToCharacter)

def unregister():
    OP_Refresh.unregister_operators()
    bpy.utils.unregister_class(OP_Refresh)
    bpy.utils.unregister_class(OBJECT_PT_JsonConstrainPanel)
    bpy.utils.unregister_class(OP_generic_constrain_operator)
    bpy.utils.unregister_class(OP_SaveToCharacter)


if __name__ == "__main__":
    register()