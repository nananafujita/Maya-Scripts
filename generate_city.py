import maya.cmds as cmds
import random

class Building:
    def __init__(self, x, y, z, w, d, h, n):
        self.x_pos = x
        self.y_pos = y
        self.z_pos = z
        self.width = w
        self.depth = d
        self.height = h
        self.name = n
        
    def create_polycube(self):
        cube = cmds.polyCube(width=self.width, height=self.height, depth=self.depth, name=self.name)
        cmds.move(self.x_pos + self.width / 2, self.y_pos, self.z_pos + self.depth / 2, worldSpace=True)
        return cube
       
class City:
    def __init__(self, grid_width, grid_depth, bldg_width, bldg_depth, bldg_height):
        self.grid_width = grid_width  
        self.grid_depth = grid_depth
        self.bldg_width = bldg_width        #(min, max)
        self.bldg_depth = bldg_depth        #(min, max)
        self.bldg_height = bldg_height      #(min, max)
        self.buildings = []

    def add_building(self, b):
        self.buildings.append(b[0])
    
    def generate_city(self):
        z = 0
        bldg_count = 0
        while z < self.grid_depth:
            # adjust last one to fit to the edge of the grid
            if z + self.bldg_depth[0] > self.grid_depth:
                break
            x = 0
            remaining_depth = self.grid_depth - z
            if remaining_depth < self.bldg_depth[1]:
                depth = remaining_depth
            else:
                depth = random.uniform(self.bldg_depth[0], self.bldg_depth[1])
                
            while x < self.grid_width:
                # break if no more buildings with minimum width fit
                if x + self.bldg_width[0] > self.grid_width:
                    break

                # random value between minimum bldg dimensions, and the either the maximum dimensions or available space
                remaining_width = self.grid_width - x
                if remaining_width < self.bldg_width[1]:
                    width = remaining_width
                else: 
                    width = random.uniform(self.bldg_width[0], min(self.bldg_width[1], remaining_width))
                height = random.uniform(self.bldg_height[0], self.bldg_height[1])
                                
                bldg_count += 1
                name = "pCube" + str(bldg_count)
                building = Building(x, height/2, z, width, depth, height, name)
                bldg_cube = building.create_polycube()
                self.add_building(bldg_cube)
                x += width
            z += depth
        cmds.group(self.buildings, name="cityGroup") 
        

class CityGenerator:
    def __init__(self):
        self.city_specs = {
            "gridWidth": 50.0,
            "gridDepth": 50.0,
            "bldgWidth": (1.0, 5.0),
            "bldgDepth": (1.0, 5.0),
            "bldgHeight": (1.0, 10.0),
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
        
        cmds.button(label="Generate City", command=lambda *_: self.on_generate_clicked())
        
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
                    
        if self.city_specs["bldgWidth"][0] > self.city_specs["gridWidth"] or self.city_specs["bldgWidth"][1] > self.city_specs["gridWidth"]:
            message += "Min and Max Building Width must be less than Grid Width\n"
            success = False
            
        if self.city_specs["bldgDepth"][0] > self.city_specs["gridDepth"] or self.city_specs["bldgDepth"][1] > self.city_specs["gridDepth"]:
            message += "Min and Max Building Depth must be less than Grid Depth\n"
            success = False
        
        if success:
            message += "Inputs Valid. City Generating..."
        else:
            message = "Inputs invalid.\n" + message

        cmds.text(self.ui_elements["message"], edit=True, label=message)
        return success
    
    #def generate_building(self, w, d, h):
        
        
    def on_generate_clicked(self):
        self.update_city_specs()
        success = self.validate_inputs()
        
        if success:
            city = City(self.city_specs["gridWidth"], 
                        self.city_specs["gridDepth"],
                        (self.city_specs["bldgWidth"][0],self.city_specs["bldgWidth"][1]),
                        (self.city_specs["bldgDepth"][0], self.city_specs["bldgDepth"][1]),
                        (self.city_specs["bldgHeight"][0], self.city_specs["bldgHeight"][1]))
            city.generate_city()
            cmds.text(self.ui_elements["message"], edit=True, label="done generating")


window1 = CityGenerator()
window1.create_ui()