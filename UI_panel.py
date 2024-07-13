import bpy
from .generic_constrain import OP_generic_constrain_operator
from .utilities import Utilities
import json


get_custom_operators = lambda : list(OP_generic_constrain_operator.__subclasses__())


#----------------------------- UI Panel

def add_to_layout(target,new_operator, column = False, layout=None):
    new_element = target.row() if column == False else layout.column().row()
    new_element.operator(new_operator.bl_idname)
    return new_element
    

class OBJECT_PT_JsonConstrainPanel(bpy.types.Panel):
    bl_label = "Json quick constrains"
    bl_idname = "OBJECT_PT_switch_ik_fk"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rigging'
    
    def draw(self, context):
        layout = self.layout
        for subclass in get_custom_operators():
            add_to_layout(layout, subclass, True, layout)
        refreshButton = add_to_layout(layout, OP_Refresh, True, layout)
        add_to_layout(layout, OP_SaveToCharacter, True, refreshButton)
        return
    

class OP_Refresh(bpy.types.Operator):
    bl_idname = "object.refresh"
    bl_label = "Refresh"
    bl_description = "Refreshes the panel from the json file"

    def execute(self, context):
        bpy.utils.unregister_class(OBJECT_PT_JsonConstrainPanel)
        OP_Refresh.unregister_operators()
        bpy.utils.register_class(OBJECT_PT_JsonConstrainPanel)
        initialize_classes()
        return {'FINISHED'}
    
    @staticmethod
    def unregister_operators():
        for subclass in get_custom_operators():
            try:
                bpy.utils.unregister_class(subclass)
                print(f"Unregistered class: {subclass.__name__}")
            except RuntimeError as e:
                print(f"Could not unregister class {subclass.__name__}: {e}")

class OP_SaveToCharacter(bpy.types.Operator):
    bl_idname = "object.savetocharacter"
    bl_label = "Save to character"
    bl_description = "Saves the preset to a custom property"
    
    def execute(self, context):
        obj = Utilities.Get_Selected_Object()
        obj["Json rigging"] = json.dumps(Utilities.Get_Json_Data(), indent=2)
        obj.property_overridable_library_set(f'["Json rigging"]', True)
        return {'FINISHED'}

#----------------------------- UI Panel

def initialize_classes():
    jsonContent = Utilities.Get_Json_Data()
    for panelButton in jsonContent.keys():
        if not isinstance(jsonContent[panelButton], dict) or panelButton.lower()=="alias":
            continue
        create_operator(panelButton)
        
def create_operator(class_name):
    alreadyExists = False
    for subclass in get_custom_operators():
        if subclass.bl_label != class_name:
            continue
        newClass = subclass
        alreadyExists = True
    newClass = newClass if alreadyExists else type(class_name, (OP_generic_constrain_operator,), {})
    newClass.bl_label = class_name
    newClass.bl_idname = f'object.{class_name.replace(" ","")}'.lower()
    bpy.utils.register_class(newClass)
    return newClass