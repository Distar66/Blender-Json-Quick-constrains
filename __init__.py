bl_info = {
    "name": "Json quick constraints",
    "author": "Distar",
    "version": (1, 3, 4),
    "blender": (2, 80, 0),
    "description": "Creates constraint buttons based on Json presets",
    "warning": "",
    "doc_url": "",
    "category": "Animation",
}

import bpy
from .UI_panel import OP_Refresh
from .UI_panel import OBJECT_PT_JsonConstrainPanel
from .UI_panel import OP_Refresh
from .UI_panel import Refresh_Handler
from .UI_panel import OP_SaveToCharacter
from .generic_constrain import OP_generic_constraint_operator

refresh_handler_instance = Refresh_Handler()

def register():
    bpy.app.handlers.depsgraph_update_post.append(refresh_handler_instance.Refresh_On_Click)
    bpy.utils.register_class(OP_Refresh)
    bpy.utils.register_class(OBJECT_PT_JsonConstrainPanel)
    bpy.utils.register_class(OP_generic_constraint_operator)
    bpy.utils.register_class(OP_SaveToCharacter)
    

def unregister():
    OBJECT_PT_JsonConstrainPanel.Delete_Custom_Operators()
    bpy.utils.unregister_class(OP_Refresh)
    bpy.utils.unregister_class(OBJECT_PT_JsonConstrainPanel)
    bpy.utils.unregister_class(OP_generic_constraint_operator)
    bpy.utils.unregister_class(OP_SaveToCharacter)
    if refresh_handler_instance.Refresh_On_Click in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(refresh_handler_instance.Refresh_On_Click)

if __name__ == "__main__":
    register()
    OP_Refresh()