import bpy
from .generic_constrain import OP_generic_constrain_operator
from .utilities import Utilities
import json


Get_Custom_Operators = lambda : list(OP_generic_constrain_operator.__subclasses__())


#----------------------------- UI Panel

def Add_To_Layout(target,newOperator, column = False, layout=None):
    new_element = target.row() if column == False else layout.column().row()
    new_element.operator(newOperator.bl_idname)
    return new_element
    

class OBJECT_PT_JsonConstrainPanel(bpy.types.Panel):
    bl_label = "Json quick constrains"
    bl_idname = "OBJECT_PT_switch_ik_fk"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rigging'
    
    def draw(self, context):
        layout = self.layout
        for subclass in Get_Custom_Operators():
            Add_To_Layout(layout, subclass, True, layout)
        refreshButton = Add_To_Layout(layout, OP_Refresh, True, layout)
        Add_To_Layout(layout, OP_SaveToCharacter, True, refreshButton)
        return
    

class OP_Refresh(bpy.types.Operator):
    bl_idname = "object.refresh"
    bl_label = "Refresh"
    bl_description = "Refresh panel"

    def execute(self, context):
        bpy.utils.unregister_class(OBJECT_PT_JsonConstrainPanel)
        OP_Refresh.Unregister_Operators()
        bpy.utils.register_class(OBJECT_PT_JsonConstrainPanel)
        Initialize_Classes()
        return {'FINISHED'}
    
    @staticmethod
    def Unregister_Operators():
        for subclass in Get_Custom_Operators():
            try:
                bpy.utils.unregister_class(subclass)
                print(f"Unregistered class: {subclass.__name__}")
            except RuntimeError as e:
                print(f"Could not unregister class {subclass.__name__}: {e}")
               
                
class OP_SaveToCharacter(bpy.types.Operator):
    bl_idname = "object.savetocharacter"
    bl_label = "Save to character"
    bl_description = "Saves the current json to a custom property on the armature"
    
    def execute(self, context):
        selectedObject = Utilities.Get_Selected_Object()
        selectedObject["Json rigging"] = json.dumps(Utilities.Get_Json_Data(), indent=2)
        selectedObject.property_overridable_library_set(f'["Json rigging"]', True)
        return{'FINISHED'}


#----------------------------- UI Panel

def Initialize_Classes():
    jsonContent = Utilities.Get_Json_Data()
    for panelButton in jsonContent.keys():
        if not isinstance(jsonContent[panelButton], dict) or panelButton.lower()=="alias":
            continue
        Create_Custom_Operator(panelButton)
        
def Create_Custom_Operator(className):
    alreadyExists = False
    for subclass in Get_Custom_Operators():
        if subclass.bl_label != className:
            continue
        newClass = subclass
        alreadyExists = True
    newClass = newClass if alreadyExists else type(className, (OP_generic_constrain_operator,), {})
    newClass.bl_label = className
    newClass.bl_idname = f'object.{className.replace(" ","")}'.lower()
    bpy.utils.register_class(newClass)
    return newClass