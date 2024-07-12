import bpy
import math
from .utilities import Utilities

class OP_generic_constrain_operator(bpy.types.Operator):
    bl_idname = "object.constrain_operator"
    bl_label = "Generic constrain"
    bl_description = "generic constrain operator"

    def execute(self, context):
        jsonContent = Utilities.Get_Json_Data()
        presetName = self.bl_label
        presetContent = Get_Preset_From_Json(presetName, jsonContent)
        aliasDict = jsonContent["Alias"] if "Alias" in jsonContent.keys() else []
        Remove_Constrains_From_Preset(presetContent, aliasDict)
        Add_Constrains_From_Preset(presetContent, aliasDict)
        return {'FINISHED'}
    

def Get_Preset_From_Json(presetName,jsonContent):
    if presetName not in jsonContent.keys():
        raise Exception(f"The preset {presetName} does not exist")
    presetContent = jsonContent[presetName]
    if not isinstance(presetContent, dict):
        raise Exception(f"The preset {presetName} is not valid")
    return presetContent

def Add_Constrains_From_Preset(presetContent, aliasDict):
    if "Add_Constrain" not in presetContent.keys():
        return
    for constrain in presetContent["Add_Constrain"]:
        aliasedConstrains = Utilities.Match_Aliases(constrain, aliasDict)
        Add_Constrain(aliasedConstrains)


def Add_Constrain(constrainAttributes):
    constrainedBone = constrainAttributes["bone"]
    constrainType = constrainAttributes["constrain"]
    newConstrain = Utilities.Get_Selected_Object().pose.bones[constrainedBone].constraints.new(type=constrainType)
    constrainTarget = Utilities.Get_Selected_Object()
    if "target" in constrainAttributes.keys() and constrainAttributes["target"] != Utilities.Get_Selected_Object().name:
        constrainTarget = [ob for ob in bpy.context.view_layer.objects if constrainAttributes["target"] in ob.name][0]
    add_attribute(newConstrain, "target", constrainTarget)
    for attribute,value in constrainAttributes.items():
        if attribute in ["constrain", "bone", "target"]:
            continue
        add_attribute(newConstrain, attribute, value)
        
def add_attribute(constrain, attribute, value):
    if value == "self":
        value = Utilities.Get_Selected_Object()
    get_subtype = lambda : type(constrain).bl_rna.properties[attribute].subtype
    if isinstance(value, float) and get_subtype() == "ANGLE":
        value = math.radians(value)
    if hasattr(constrain, attribute):
        setattr(constrain, attribute, value)
        

def Remove_Constrains_From_Preset(presetContent, aliasDict):
    if "Remove Constrains" in presetContent.keys():
        bonesToClear = Utilities.Match_Aliases(presetContent["Remove Constrains"], aliasDict)
        Remove_All_Constrains(bonesToClear)

def Remove_All_Constrains(bonesToClear):
    for boneName in bonesToClear:
        Clear_Bone_Constrains(boneName)

def Clear_Bone_Constrains(boneName):
    characterRig = Utilities.Get_Selected_Object().pose
    for constrain in characterRig.bones[boneName].constraints:
        characterRig.bones[boneName].constraints.remove(constrain)
            