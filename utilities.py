import bpy
from pathlib import Path
import json


def Is_Valid_Json(jsonString):
    try:
        json.loads(jsonString)
        return True
    except ValueError:
        return False

class Utilities:
    
    @staticmethod
    def Get_Selected_Object():
        return bpy.context.object
    
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
    def Is_Armature(obj):
        return False if not obj or obj.type != "ARMATURE" else True

    @staticmethod
    def Is_Selected_Object_Valid_Armature():
        if not Utilities.Get_Selected_Object():
            return False
        obj = Utilities.Get_Selected_Object()
        if not Utilities.Is_Armature(obj):
            return False
        return True

    @staticmethod
    def Get_Json_Data(obj):
        jsonFileData = Utilities.Get_Armature_Json_File(obj)
        if jsonFileData:
            return jsonFileData
        customPropertyJsonData = Utilities.Get_Armature_Json_Custom_Property(obj)
        if customPropertyJsonData:
            return customPropertyJsonData
        return None
    
    @staticmethod
    def Is_Valid_Armature_With_Json():
        if not Utilities.Is_Selected_Object_Valid_Armature():
                return ValueError("The selected object is not a valid armature")
        obj = Utilities.Get_Selected_Object()
        if not Utilities.Get_Json_Data(obj):
            return ValueError("The object has no valid Json file or valid Json custom property")
        return True
        
    @staticmethod
    def Get_Armature_Json_Custom_Property(obj):
        if not obj["Json rig"]:
            return False
        if not Is_Valid_Json(obj["Json rig"]):
            return False
        return obj["Json rig"]

    @staticmethod
    def Get_Armature_Json_File(obj):
        jsonFilename = Utilities.Get_Selected_ArmatureData_Name()+'.json'
        filePath = Path(bpy.path.abspath("//")+jsonFilename)
        if not filePath.exists():
            return False
        with open(filePath) as jsonDataFile:
            jsonContent = jsonDataFile.read()
            if not Is_Valid_Json(jsonContent):
                return False
            return json.loads(jsonContent)
        
    @staticmethod
    def Get_Json_Filepath(obj):
        jsonFilename = Utilities.Get_Selected_ArmatureData_Name()+'.json'
        filePath = Path(bpy.path.abspath("//")+jsonFilename)
        if not filePath.exists():
            return False
        
    @staticmethod
    def Get_Selected_ArmatureData_Name():
        if not Utilities.Is_Selected_Object_Valid_Armature():
            raise Exception("No armature selected")
        return bpy.data.armatures[Utilities.Get_Selected_Object().data.name].name
