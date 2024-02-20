import configparser
from pathlib import Path
from pulse import OPEN_PULSE_DIR


class StandardCrossSections:
    def __init__(self):
        self._reset_variables()
        self._load_standard_cross_sections_for_carbon_steel()
        self._load_standard_cross_sections_for_stainless_steel()

    def _reset_variables(self):
        self.carbon_steel_cross_sections = dict()
        self.stainless_steel_cross_sections = dict()
        self.default_path_for_carbon_steel = OPEN_PULSE_DIR / 'pulse/lib/standard_cross_sections_carbon_steel.dat'
        self.default_path_for_stainless_steel = OPEN_PULSE_DIR / 'pulse/lib/standard_cross_sections_stainless_steel.dat'

    def _load_standard_cross_sections_for_carbon_steel(self):
        """ This method loads the standard cross-sections from ASME B36.10m (2018)
            Welded and Seamless Wrought Steel Pipe.
        """

        file = open(self.default_path_for_carbon_steel, mode="r", encoding="utf-8")
        lines = file.readlines()

        for index, line in enumerate(lines):
            
            if "#" in line:
                continue

            line = line.split(";")
            NPS_str = line[0].split("/")

            if len(NPS_str) == 1:
                _NPS = float(NPS_str[0])
            elif len(NPS_str) == 2:
                if len(NPS_str[0]) == 1:
                    _NPS = float(NPS_str[0])/float(NPS_str[1])
                elif len(NPS_str[0]) == 2:
                    _NPS = float(NPS_str[0][0]) + float(NPS_str[0][1])/float(NPS_str[1])
                else:
                    print(f"Invalid cross-section NPS: {NPS_str}")
                    return
            else:
                print(f"Invalid cross-section NPS: {NPS_str}")
                return

            DN_str = line[1][1:-1]
            _DN = int(DN_str)

            id_str = line[2]
            if "..." in id_str:
                identification = ""
            else:
                identification = id_str
            
            schedule_str = line[3]
            if "..." in schedule_str:
                schedule = ""
            else:
                schedule = int(schedule_str)
        
            outside_diameter_in = float(line[4])
            outside_diameter_mm = 25.4*float(line[4])

            thickness_in = float(line[6])
            thickness_mm = 25.4*float(line[6])

            linear_mass_lb_ft = float(line[8])
            linear_mass_kg_m = (0.45359237/0.3048)*float(line[8])
            
            self.carbon_steel_cross_sections[index] = { "NPS" : _NPS,
                                                        "DN" : _DN,
                                                        "Identification" : identification,
                                                        "Schedule" : schedule,
                                                        "Outside diameter (in)" : outside_diameter_in,
                                                        "Outside diameter (mm)" : outside_diameter_mm,
                                                        "Wall thickness (in)" : thickness_in,
                                                        "Wall thickness (mm)" : thickness_mm,
                                                        "Plain end mass (lb/ft)" : linear_mass_lb_ft,
                                                        "Plain end mass (kg/m)" : linear_mass_kg_m }

        file.close()


    def _load_standard_cross_sections_for_stainless_steel(self):
        """ This method loads the standard cross-sections from ASME B36.19m (2018)
            Stainless Steel Pipe.
        """

        file = open(self.default_path_for_stainless_steel, mode="r", encoding="utf-8")
        lines = file.readlines()
        shift = 0

        for index, line in enumerate(lines):
            
            if "#" in line:
                continue

            line = line.split(";")
            NPS_str = line[0].split("/")

            if len(NPS_str) == 1:
                NPS = float(NPS_str[0])
            elif len(NPS_str) == 2:
                if len(NPS_str[0]) == 1:
                    NPS = float(NPS_str[0])/float(NPS_str[1])
                elif len(NPS_str[0]) == 2:
                    NPS = float(NPS_str[0][0]) + float(NPS_str[0][1])/float(NPS_str[1])
                else:
                    print(f"Invalid cross-section NPS: {NPS_str}")
                    return
            else:
                print(f"Invalid cross-section NPS: {NPS_str}")
                return

            DN_str = line[1][1:-1]
            DN = int(DN_str)
            
            schedule_str = line[2]
            if "..." in schedule_str:
                schedule = ""
            else:
                schedule = schedule_str
        
            outside_diameter_in = float(line[3])
            outside_diameter_mm = 25.4*float(line[3])

            if line[5] == "...":
                shift += 1
                continue

            else:

                thickness_in = float(line[5])
                thickness_mm = float(line[6][1:-1])
                linear_mass_lb_ft = float(line[7])
                linear_mass_kg_m = (0.45359237/0.3048)*float(line[7])

            self.stainless_steel_cross_sections[index-shift] = {"NPS" : NPS,
                                                                "DN" : DN,
                                                                "Schedule" : schedule,
                                                                "Identification" : "",
                                                                "Outside diameter (in)" : outside_diameter_in,
                                                                "Outside diameter (mm)" : outside_diameter_mm,
                                                                "Wall thickness (in)" : thickness_in,
                                                                "Wall thickness (mm)" : thickness_mm,
                                                                "Plain end mass (lb/ft)" : linear_mass_lb_ft,
                                                                "Plain end mass (kg/m)" : linear_mass_kg_m}

        file.close()


if __name__ == "__main__":
    cross = StandardCrossSections()