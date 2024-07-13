import bpy
from .generic_constrain import OP_generic_constrain_operator
from .utilities import Utilities
import json
from bpy.app.handlers import persistent


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
    bl_category = 'Animation'
    
    def draw(self, context):
        layout = self.layout
        for subclass in get_custom_operators():
            add_to_layout(layout, subclass, True, layout)
        refreshButton = add_to_layout(layout, OP_Refresh, True, layout)
        add_to_layout(layout, OP_SaveToCharacter, True, refreshButton)
        return
    
    @staticmethod
    def Delete_Custom_Operators():
        for subclass in get_custom_operators():
            try:
                bpy.utils.unregister_class(subclass)
                print(f"Unregistered class: {subclass.__name__}")
            except RuntimeError as e:
                print(f"Could not unregister class {subclass.__name__}: {e}")
    

class OP_Refresh(bpy.types.Operator):
    bl_idname = "object.refresh"
    bl_label = "Refresh"
    bl_description = "Refreshes the panel from the json file"
    
    def __init__(self):
        self.currentObject = None

    def execute(self, context):
        isValid = Utilities.Is_Valid_Armature_With_Json()
        if isinstance(isValid, ValueError):
            raise Exception(isValid)
        Refresh_Handler.Refresh_Panel(Utilities.Get_Selected_Object())
        return {'FINISHED'}
    
    
class Refresh_Handler:
    def __init__(self):
        self.currentObject = None
    
    @persistent
    def Refresh_On_Click(self,scene, depsgraph): #scene and depsgraph match Blender handler's calling signature
        if isinstance(Utilities.Is_Valid_Armature_With_Json(), ValueError):
            return {'FINISHED'}
        obj = Utilities.Get_Selected_Object()
        if self.currentObject and obj == self.currentObject:
            return {"FINISHED"}
        Refresh_Handler.Refresh_Panel(obj)
        return {"FINISHED"}
    
    @staticmethod
    def Refresh_Panel(obj):
        bpy.utils.unregister_class(OBJECT_PT_JsonConstrainPanel)
        OBJECT_PT_JsonConstrainPanel.Delete_Custom_Operators()
        bpy.utils.register_class(OBJECT_PT_JsonConstrainPanel)
        Create_Operators_From_Json(obj)
                

class OP_SaveToCharacter(bpy.types.Operator):
    bl_idname = "object.savetocharacter"
    bl_label = "Save to character"
    bl_description = "Saves the preset to a custom property"
    
    def execute(self, context):
        if not Utilities.Is_Selected_Object_Valid_Armature():
            raise Exception("No armature selected")
        obj = Utilities.Get_Selected_Object()
        if not Utilities.Get_Armature_Json_File(obj):
            raise Exception(f"{Utilities.Get_Selected_ArmatureData_Name()}.json does not exist or is invalid")
        obj["Json rig"] = json.dumps(Utilities.Get_Json_Data(obj), indent=2)
        obj.property_overridable_library_set(f'["Json rig"]', True)
        return {'FINISHED'}

#----------------------------- UI Panel

def Create_Operators_From_Json(obj):
    jsonContent = Utilities.Get_Json_Data(obj)
    for panelButton in jsonContent.keys():
        if not isinstance(jsonContent[panelButton], dict) or panelButton.lower()=="alias":
            continue
        Create_Custom_Operator(panelButton)
        
def Create_Custom_Operator(class_name):
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

