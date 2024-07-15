import bpy
import math
from .utilities import Utilities
from .utilities import Bpy_Utilities

class OP_generic_constraint_operator(bpy.types.Operator):
    bl_idname = "object.constraint_operator"
    bl_label = "Generic constraint"
    bl_description = "generic constraint operator"

    def execute(self, context):
        obj = Bpy_Utilities.Get_Selected_Object()
        jsonContent = Bpy_Utilities.Get_Json_Data(obj)
        presetName = self.bl_label
        preset = Get_Preset_From_Json(presetName, jsonContent)
        presetKeys = jsonContent.keys()
        aliasKey = Utilities.Match_Case_Insensitive("alias", jsonContent.keys())
        aliasDict = jsonContent[aliasKey] if aliasKey else {}
        Remove_Constraints_From_Preset(preset, aliasDict)
        Add_Constraints_From_Preset(obj,preset, aliasDict)
        return {'FINISHED'}
    
    
def Get_Preset_From_Json(presetName,jsonContent):
    if presetName not in jsonContent.keys():
        raise Exception(f"The preset {presetName} does not exist")
    preset = jsonContent[presetName]
    if not isinstance(preset, dict):
        raise Exception(f"The preset {presetName} is not valid")
    return preset

def Add_Constraints_From_Preset(obj,preset, aliasDict):
    constraintKey = Utilities.Match_Case_Insensitive("constraints", preset.keys())
    if not constraintKey:
        return
    for constraint in preset[constraintKey]:
        aliasedConstraints = Utilities.Match_Aliases(constraint, aliasDict)
        Add_Constraint(obj,aliasedConstraints)


def Add_Constraint(obj,constraintAttr):
    constrainedBone = constraintAttr["bone"]
    constrainType = constraintAttr["constraint"]
    newConstraint = obj.pose.bones[constrainedBone].constraints.new(type=constrainType)
    for attribute,value in constraintAttr.items():
        if attribute in ["constraint", "bone"]:
            continue
        Add_Attribute(obj,newConstraint, attribute, value)
    if "target" in type(newConstraint).bl_rna.properties.keys() and newConstraint.target == None:
        Add_Attribute(obj,newConstraint, "target", "self")
    
        
def Add_Attribute(obj,constraint, attribute, value):
    is_pointer = lambda : True if type(constraint).bl_rna.properties[attribute].type == "POINTER" else False
    get_subtype = lambda : type(constraint).bl_rna.properties[attribute].subtype
    if is_pointer():
        if value.lower() == "self":
            value = obj
        else :
            value = Bpy_Utilities.Get_Object_From_Name(value)
    if isinstance(value, float) and get_subtype() == "ANGLE":
        value = math.radians(value)
    if hasattr(constraint, attribute):
        setattr(constraint, attribute, value)
        

def Remove_Constraints_From_Preset(preset, aliasDict):
    removeKey = Utilities.Match_Case_Insensitive("remove", [key for key in preset.keys()])
    if not removeKey:
        return 
    bonesToClear = Utilities.Match_Aliases(preset[removeKey], aliasDict)
    Remove_All_Constraints(bonesToClear)

def Remove_All_Constraints(bonesToClear):
    for boneName in bonesToClear:
        Clear_Bone_Constraints(boneName)

def Clear_Bone_Constraints(boneName):
    characterRig = Bpy_Utilities.Get_Selected_Object().pose
    for constraint in characterRig.bones[boneName].constraints:
        characterRig.bones[boneName].constraints.remove(constraint)
        
        