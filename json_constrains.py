bl_info = {
    "name": "Json rigging panel",
    "author": "Distar",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "description": "Creates animation constrain panels based on Json presets",
    "warning": "",
    "doc_url": "",
    "category": "Animation",
}

import bpy
import math
import os
from pathlib import Path
import json

get_selected_object = lambda : bpy.context.object
get_filepath = lambda : bpy.data.filepath
get_directory = lambda : bpy.path.abspath("//")

get_custom_operators = lambda : list(OP_generic_constrain_operator.__subclasses__())

def match_aliases(dict, aliasDict):
    match_alias = lambda x,aliasDict : aliasDict[x] if x in aliasDict.keys() else x
    if isinstance(dict, list):
        mapped_items=[]
        for item in dict:
            mapped_items.append(match_alias(item, aliasDict))
        return mapped_items
    for entry,value in dict.items():
        dict[entry]=match_alias(dict[entry], aliasDict)
    return dict

def Get_Json_Data():
    filePath = Path(bpy.path.abspath("//")+Get_Armature_Name()+'.json')
    if not filePath.exists():
        raise Exception(f"Le fichier {Get_Armature_Name()}.json n'existe pas")
    with open(filePath) as jsonDataFile:
        return json.load(jsonDataFile)

def add_attribute(constrain, attribute, value):
    if value == "self":
        value = get_selected_object()
    get_subtype = lambda : type(constrain).bl_rna.properties[attribute].subtype
    if isinstance(value, float) and get_subtype() == "ANGLE":
        value = math.radians(value)
    if hasattr(constrain, attribute):
        print("a l'attribut" + attribute)
        setattr(constrain, attribute, value)

def Get_Armature_Name():
    selectedObject = get_selected_object()
    if selectedObject.type != "ARMATURE":
        raise Exception("Please select an armature")
    return bpy.data.armatures[selectedObject.data.name].name


def Add_Constrain(constrain_attributes):
    constrainedBone = constrain_attributes["bone"]
    constrainType = constrain_attributes["constrain"]
    newConstrain = get_selected_object().pose.bones[constrainedBone].constraints.new(type=constrainType)
    constrainTarget = get_selected_object()
    if "target" in constrain_attributes.keys() and constrain_attributes["target"] != get_selected_object().name:
        constrainTarget = [ob for ob in bpy.context.view_layer.objects if constrain_attributes["target"] in ob.name][0]
    add_attribute(newConstrain, "target", constrainTarget)
    for attribute,value in constrain_attributes.items():
        if attribute in ["constrain", "bone", "target"]:
            continue
        add_attribute(newConstrain, attribute, value)
        

def Remove_Bone_Constrains(boneName):
    characterRig = get_selected_object().pose
    for constrain in characterRig.bones[boneName].constraints:
        characterRig.bones[boneName].constraints.remove(constrain)

def Remove_Constrains(bonesConstrainsToClear):
    for boneName in bonesConstrainsToClear:
        Remove_Bone_Constrains(boneName)


#-----------------------------------Jambes


class OP_generic_constrain_operator(bpy.types.Operator):
    bl_idname = "object.constrain_operator"
    bl_label = "Generic constrain"
    bl_description = "generic constrain operator"

    def execute(self, context):
        jsonContent = Get_Json_Data()
        if self.bl_label not in jsonContent.keys():
            raise Exception(f"The preset {self.bl_label} does not exist")
        buttonValues = jsonContent[self.bl_label]
        aliasDict = jsonContent["Alias"] if "Alias" in jsonContent.keys() else []
        if not isinstance(buttonValues, dict):
            return {'FINISHED'}
        if "Remove Constrains" in buttonValues.keys():
            aliased_constrains = match_aliases(buttonValues["Remove Constrains"], aliasDict)
            Remove_Constrains(aliased_constrains)        
        if "Add_Constrain" not in buttonValues.keys():
            return {'FINISHED'}        
        for constrain in buttonValues["Add_Constrain"]:
            aliased_constrains = match_aliases(constrain, aliasDict)
            Add_Constrain(aliased_constrains)
        return {'FINISHED'}
        
    
class OP_Refresh(bpy.types.Operator):
    bl_idname = "object.refresh"
    bl_label = "Refresh panel"
    bl_description = "Refresh panel"

    def execute(self, context):
        bpy.utils.unregister_class(OBJECT_PT_SwitchIKFKPanel)
        unregister_operators()
        bpy.utils.register_class(OBJECT_PT_SwitchIKFKPanel)
        initialize_classes()
        return {'FINISHED'}


#----------------------------- UI Panel

def layout_op(target,new_operator, column = False, layout=None):
    new_element = target.row() if column == False else layout.column().row()
    new_element.operator(new_operator.bl_idname)
    return new_element
    

class OBJECT_PT_SwitchIKFKPanel(bpy.types.Panel):
    bl_label = "IK/FK Switcher"
    bl_idname = "OBJECT_PT_switch_ik_fk"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Animation'
    
    def draw(self, context):
        layout = self.layout
        for subclass in get_custom_operators():
            layout_op(layout, subclass, True, layout)
        layout_op(layout, OP_Refresh, True, layout)
        return
        

def initialize_classes():
    jsonContent = Get_Json_Data()
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

def register():
    bpy.utils.register_class(OP_Refresh)
    bpy.utils.register_class(OBJECT_PT_SwitchIKFKPanel)
    
def unregister_operators():
    for subclass in get_custom_operators():
        try:
            bpy.utils.unregister_class(subclass)
            print(f"Unregistered class: {subclass.__name__}")
        except RuntimeError as e:
            print(f"Could not unregister class {subclass.__name__}: {e}")

def unregister():
    unregister_operators()
    bpy.utils.unregister_class(OP_Refresh)
    bpy.utils.unregister_class(OBJECT_PT_SwitchIKFKPanel)


if __name__ == "__main__":
    register()