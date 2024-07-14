import bpy
from pathlib import Path
import json


def Is_Valid_Json(str):
    try:
        json.loads(str)
        return True
    except Exception as e:
        return False


class Bpy_Utilities:
    @staticmethod
    def Get_Selected_Object():
        return bpy.context.object
    
    @staticmethod
    def Get_Object_From_Name(searchedName):
        return [obj for obj in bpy.context.view_layer.objects if searchedName.lower in obj.name.lower()][0]
    
    @staticmethod
    def Is_Armature(obj):
        return False if not obj or obj.type != "ARMATURE" else True
    
    @staticmethod
    def Is_Selected_Valid_Armature():
        if not Bpy_Utilities.Get_Selected_Object():
            return False
        obj = Bpy_Utilities.Get_Selected_Object()
        if not Bpy_Utilities.Is_Armature(obj):
            return False
        return True
    
    @staticmethod
    def Get_Json_Data(obj):
        jsonFileData = Bpy_Utilities.Get_Armature_Json_File(obj)
        if jsonFileData:
            return jsonFileData
        customPropertyJson = Bpy_Utilities.Get_Armature_Json_Prop(obj)
        if customPropertyJson:
            return customPropertyJson
        return None
    
    @staticmethod
    def Selected_Armature_Has_Json():
        if not Bpy_Utilities.Is_Selected_Valid_Armature():
            return ValueError("The selected object is not a valid armature")
        obj = Bpy_Utilities.Get_Selected_Object()
        if not Bpy_Utilities.Get_Json_Data(obj):
            return ValueError("The object has no valid Json file or valid Json custom property")
        return True
        
    @staticmethod
    def Get_Armature_Json_Prop(obj):
        if not obj["Json rig"]:
            return False
        if not Is_Valid_Json(obj["Json rig"]):
            return False
        return json.loads(obj["Json rig"])

    @staticmethod
    def Get_Armature_Json_File(obj):
        jsonFilename = Bpy_Utilities.Get_Selected_ArmatureData_Name()+'.json'
        filePath = Path(bpy.path.abspath("//")+jsonFilename)
        if not filePath.exists():
            return False
        with open(filePath) as jsonDataFile:
            jsonString = jsonDataFile.read()
            if not Is_Valid_Json(jsonString):
                return False
            return json.loads(jsonString)
        
    @staticmethod
    def Get_Json_Filepath(obj):
        jsonFilename = Bpy_Utilities.Get_Selected_ArmatureData_Name()+'.json'
        filePath = Path(bpy.path.abspath("//")+jsonFilename)
        if not filePath.exists():
            return False
        
    @staticmethod
    def Get_Selected_ArmatureData_Name():
        if not Bpy_Utilities.Is_Selected_Valid_Armature():
            return Exception("No armature selected")
        return bpy.data.armatures[Bpy_Utilities.Get_Selected_Object().data.name].name

class Utilities:
    
    @staticmethod
    def Match_Aliases(dict, aliasDict):
        match_alias = lambda x,aliasDict : aliasDict[x] if x in aliasDict.keys() else x
        if isinstance(dict, list):
            mapped_items=[]
            for item in dict:
                mapped_items.append(match_alias(item, aliasDict))
            return mapped_items
        for entry,value in dict.items():
            dict[entry]=match_alias(dict[entry], aliasDict)
        return dict
    
    @staticmethod
    def Match_Case_Insensitive(string, list):
        for element in list:
            if element.lower() != string.lower():
                continue
            return element
        return None
