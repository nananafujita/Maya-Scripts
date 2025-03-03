import maya.cmds as cmds
import random

class CityGenerator:
    def __init__(self):
        self.city_specs = {
            "gridWidth": 50.0,
            "gridDepth": 50.0,
            "bldgWidth": (1.0, 5.0),
            "bldgDepth": (1.0, 5.0),
            "bldgHeight": (1.0, 10.0),
            "minSpacing": 1.0
        }
        self.window = "CityGenerator"
        self.ui_elements = {}
    
    def create_ui(self):
        if cmds.window("cityGenerator", title="City Generator", exists=True):
            cmds.deleteUI("cityGenerator")
            
        self.window = cmds.window("cityGenerator")
        cmds.columnLayout(adjustableColumn=True)
            
        cmds.text(label="Grid", align="left", font="boldLabelFont")
        self.ui_elements["gridWidth"] = cmds.floatFieldGrp("gridWidth", label="Width", value1=self.city_specs["gridWidth"])
        self.ui_elements["gridDepth"] = cmds.floatFieldGrp("gridDepth", label="Depth", value1=self.city_specs["gridDepth"])
            
        cmds.text(label="Buildings", align="left", font="boldLabelFont")
        self.ui_elements["bldgWidth"] = cmds.floatFieldGrp("bldgWidth", label="Width Min/Max", numberOfFields=2, value1=self.city_specs["bldgWidth"][0], value2=self.city_specs["bldgWidth"][1])
        self.ui_elements["bldgDepth"] = cmds.floatFieldGrp("bldgDepth", label="Depth Min/Max",  numberOfFields=2, value1=self.city_specs["bldgDepth"][0], value2=self.city_specs["bldgDepth"][1])
        self.ui_elements["bldgHeight"] = cmds.floatFieldGrp("bldgHeight", label="Height Min/Max",  numberOfFields=2, value1=self.city_specs["bldgHeight"][0], value2=self.city_specs["bldgHeight"][1])
        self.ui_elements["minSpacing"] = cmds.floatFieldGrp("minSpacing", label="Min Spacing", value1=self.city_specs["minSpacing"])
        
        cmds.button(label="Generate City", command=lambda *_: self.generate_city())
        
        self.ui_elements["message"] = cmds.text(label="", align="right") 
        cmds.showWindow(self.window)
    
    def get_input(self, field_name):
        ui_element = self.ui_elements[field_name]
        if not ui_element:
            raise ValueError("Error: The UI element is None. Something went wrong with storing of querying the UI element.")
        
        try:
            value1=cmds.floatFieldGrp(ui_element, query=True, value1=True)
            value2=cmds.floatFieldGrp(ui_element, query=True, value2=True)
            if value2 is not None:
                return (value1, value2)
            else:
                return value1
        except RuntimeError:
            return value1
    
    def update_city_specs(self):
        for key in self.city_specs:
            self.city_specs[key] = self.get_input(key)
    
    def validate_inputs(self):
        success = True
        message = ""
        for field_name, val in self.city_specs.items():
            if isinstance(val, tuple):
                if val[0] < 1.0 or val[1] < 1.0:
                    message += f"{field_name} values must be at least 1.0\n"
                    success = False
                if val[0] > val[1]:
                    message += f"{field_name} min must be less than or equal to max\n"
                    success = False
            '''elif field_name == "minSpacing":
                if val < 0.0:
                    message += f"{field_name} must be at least 0.0\n"
                    success = False'''
                    
        if self.city_specs["bldgWidth"][1] > self.city_specs["gridWidth"]:
            message += "Max Building Width must be less than Grid Width\n"
            success = False
            
        if self.city_specs["minSpacing"] + self.city_specs["bldgWidth"][0] > self.city_specs["gridWidth"]:
            message += "Spacing + Min Building Width must be less than Grid Width\n"
            success = False
                    
        if self.city_specs["bldgDepth"][1] > self.city_specs["gridDepth"]:
            message += "Max Building Depth must be less than Grid Depth\n"
            success = False
            
        if self.city_specs["spacing"] + self.city_specs["bldgDepth"][0] > self.city_specs["gridDepth"]:
            message += "Spacing + Min Building Depth must be less than Grid Depth\n"
            success = False
        
        if success:
            message += "Inputs Valid. City Generating..."
        else:
            message = "Inputs invalid.\n" + message

        cmds.text(self.ui_elements["message"], edit=True, label=message)
        return success
    
    def generate_building(self, w, d, h):
        
        
    def generate_city(self):
        self.update_city_specs()
        success = self.validate_inputs()
        
        if success:
            gridW = self.city_specs["gridWidth"]
            gridD = self.city_specs["gridDepth"]
            minBldgW = self.city_specs["bldgWidth"][0]
            maxBldgW = self.city_specs["bldgWidth"][1]
            minBldgD = self.city_specs["bldgDepth"][0]
            maxBldgD = self.city_specs["bldgDepth"][1]
            minBldgH = self.city_specs["bldgHeight"][0]
            maxBldgH = self.city_specs["bldgHeight"][1]
            minSpace = self.city_specs["minSpacing"]
            x = 0
            while x < gridW:
                if x + minBldgW > gridW:
                    break
                maxBldgW = min(maxBldgW, gridW - x) #clamp maxBldgWidth to not exceed grid limits
                z = 0
                while z < gridD:
                    if z + minBldgD > gridD:
                        break
                    maxBldgD = min(maxBldgD, gridD - z)

                    bldgW = random.uniform(minBldgW, maxBldgW)
                    bldgD = random.uniform(minBldgD, maxBldgD)
                    bldgH = random.uniform(minBldgH, maxBldgH)
                    space = random.uniform(minSpace, minSpace * 1.5) # add some random offset to spacing
                    self.generate_building(bldgW, bldgD, bldgH)
       
            
            
window1 = CityGenerator()
window1.create_ui()