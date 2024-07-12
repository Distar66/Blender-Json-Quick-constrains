import bpy
from pathlib import Path
import json


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
    def Get_Json_Data():
        filePath = Path(bpy.path.abspath("//")+Utilities.Get_Armature_Name()+'.json')
        if not filePath.exists():
            raise Exception(f"Le fichier {Utilities.Get_Armature_Name()}.json n'existe pas")
        with open(filePath) as jsonDataFile:
            return json.load(jsonDataFile)

    @staticmethod
    def Get_Armature_Name():
        selectedObject = Utilities.Get_Selected_Object()
        if not selectedObject or selectedObject.type != "ARMATURE":
            raise Exception("Please select an armature")
        return bpy.data.armatures[selectedObject.data.name].name
