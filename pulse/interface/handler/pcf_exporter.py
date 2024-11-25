from pathlib import Path

import numpy as np

from pulse.editor.structures import Bend, Elbow, Flange, Pipe, Point, Valve, Reducer


class PCFExporter:
    def __init__(self) -> None:
        pass

    def save(self, path, pipeline):
        path = Path(path).with_suffix(".pcf")
        var = self.encoder(pipeline)

        with open(path, "w", encoding="iso_8859_1") as file:
            file.write(var)

    def encoder(self, pipeline):
        string = self.encoder_header(pipeline)

        for structure in pipeline.structures:
            if isinstance(structure, Pipe):
                stringer = self.encoder_pipe(structure)
                string = string + "\n" + stringer

            elif isinstance(structure, Elbow):
                if structure.is_colapsed():
                    continue
                stringer = self.encoder_elbow(structure)
                string = string + "\n" + stringer

            elif isinstance(structure, Bend):
                if structure.is_colapsed():
                    continue
                stringer = self.encoder_bend(structure)
                string = string + "\n" + stringer

            elif isinstance(structure, Flange):
                stringer = self.encoder_flange(structure)
                string = string + "\n" + stringer

            elif isinstance(structure, Valve):
                stringer = self.encoder_valve(structure)
                string = string + "\n" + stringer

            elif isinstance(structure, Reducer):
                stringer = self.encoder_reducer(structure)
                string = string + "\n" + stringer


        return string

    def encoder_header(self, pipeline):
        string = (
            "ISOGEN-FILES            ISOGEN.FLS                  \n"
            "UNITS-BORE              MM                          \n"
            "UNITS-CO-ORDS           MM                          \n"
            "UNITS-BOLT-LENGTH       MM                          \n"
            "UNITS-BOLT-DIA          MM                          \n"
            "UNITS-WEIGHT            KGS                         \n"
            "PIPELINE-REFERENCE      CFG1                        \n"
            "PIPING-SPEC         CS150                           \n"
            "START-CO-ORDS       0.0000       0.0000      0.0000 \n"
        )

        return string

    def encoder_pipe(self, pipe):
        start_x = round(pipe.start.x * 1_000, 5)
        start_y = round(pipe.start.y * 1_000, 5)
        start_z = round(pipe.start.z * 1_000, 5)
        start_diameter = round(pipe.diameter * 1_000, 5)

        end_x = round(pipe.end.x * 1_000, 5)
        end_y = round(pipe.end.y * 1_000, 5)
        end_z = round(pipe.end.z * 1_000, 5)
        end_diameter = round(pipe.diameter * 1_000, 5)

        thk = round(pipe.thickness * 1_000, 5)

        string = (
            "PIPE \n"
            f"    END-POINT {start_x:>14}  {start_y:>14} {start_z:>14} {start_diameter:>14} \n"
            f"    END-POINT {end_x:>14}  {end_y:>14} {end_z:>14} {end_diameter:>14} \n"
            f"    R2_WALL_THK {thk:>14} \n"
            )
        return string
    
    def encoder_reducer(self, reducer):
        start_x = round(reducer.start.x * 1_000, 5)
        start_y = round(reducer.start.y * 1_000, 5)
        start_z = round(reducer.start.z * 1_000, 5)
        start_diameter = round(reducer.start_diameter * 1_000, 5)

        end_x = round(reducer.end.x * 1_000, 5)
        end_y = round(reducer.end.y * 1_000, 5)
        end_z = round(reducer.end.z * 1_000, 5)
        end_diameter = round(reducer.end_diameter * 1_000, 5)

        thk = round(reducer.thickness * 1_000, 5)

        if reducer.offset_y == 0 and reducer.offset_z ==0:
            string = (
                "REDUCER-CONCENTRIC \n"
                f"    END-POINT {start_x:>14}  {start_y:>14} {start_z:>14} {start_diameter:>14} \n"
                f"    END-POINT {end_x:>14}  {end_y:>14} {end_z:>14} {end_diameter:>14} \n"
                f"    R2_WALL_THK {thk:>14} \n"
                )
        else:
            string = (
                "REDUCER-ECCENTRIC \n"
                f"    END-POINT {start_x:>14}  {start_y:>14} {start_z:>14} {start_diameter:>14} \n"
                f"    END-POINT {end_x:>14}  {end_y:>14} {end_z:>14} {end_diameter:>14} \n"
                f"    R2_WALL_THK {thk:>14} \n"
                )
            
        return string

    def encoder_bend(self, bend):

        start_x = round(bend.start.x * 1_000, 5)
        start_y = round(bend.start.y * 1_000, 5)
        start_z = round(bend.start.z * 1_000, 5)
        start_diameter = round(bend.diameter * 1_000, 5)

        end_x = round(bend.end.x * 1_000, 5)
        end_y = round(bend.end.y * 1_000, 5)
        end_z = round(bend.end.z * 1_000, 5)
        end_diameter = round(bend.diameter * 1_000, 5)

        centre_x = round(bend.corner.x *1_000, 5)
        centre_y = round(bend.corner.y *1_000, 5)
        centre_z = round(bend.corner.z *1_000, 5)

        thk = round(bend.thickness *1_000, 5)

        string = (
            "BEND \n"
            f"    END-POINT {start_x:>14}  {start_y:>14} {start_z:>14} {start_diameter:>14} \n"
            f"    END-POINT {end_x:>14}  {end_y:>14} {end_z:>14} {end_diameter:>14} \n"
            f"    CENTRE-POINT {centre_x:>14}  {centre_y:>14} {centre_z:>14} \n"
            f"    R2_WALL_THK {thk:>14} \n"
             "    SKY BEBW"
        )
        return string

    def encoder_flange(self, flange):

        start_x = round(flange.start.x * 1_000, 5)
        start_y = round(flange.start.y * 1_000, 5)
        start_z = round(flange.start.z * 1_000, 5)
        start_diameter = round(flange.diameter * 1_000, 5)

        end_x = round(flange.end.x * 1_000, 5)
        end_y = round(flange.end.y * 1_000, 5)
        end_z = round(flange.end.z * 1_000, 5)
        end_diameter = round(flange.diameter * 1_000, 5)

        thk = round(flange.thickness *1_000, 5)

        string = (
            "FLANGE \n"
            f"    END-POINT {start_x:>14}  {start_y:>14} {start_z:>14} {start_diameter:>14} \n"
            f"    END-POINT {end_x:>14}  {end_y:>14} {end_z:>14} {end_diameter:>14} \n"
            f"    R2_WALL_THK {thk:>14} \n"
             "    SKEY FLBL"
        )
        return string
    
    def encoder_valve(self, valve):
        
        start_x = round(valve.start.x * 1_000, 5)
        start_y = round(valve.start.y * 1_000, 5)
        start_z = round(valve.start.z * 1_000, 5)
        start_diameter = round(valve.diameter * 1_000, 5)

        end_x = round(valve.end.x * 1_000, 5)
        end_y = round(valve.end.y * 1_000, 5)
        end_z = round(valve.end.z * 1_000, 5)
        end_diameter = round(valve.diameter * 1_000, 5)

        thk = round(valve.thickness *1_000, 5)

        string = (
            "VALVE \n"
            f"    END-POINT {start_x:>14}  {start_y:>14} {start_z:>14} {start_diameter:>14} \n"
            f"    END-POINT {end_x:>14}  {end_y:>14} {end_z:>14} {end_diameter:>14} \n"
            f"    R2_WALL_THK {thk:>14} \n"
             "    SKEY VVBW"
        )
        return string
  
    def encoder_elbow(self, bend):

        
        start_x = round(bend.start.x * 1_000, 5)
        start_y = round(bend.start.y * 1_000, 5)
        start_z = round(bend.start.z * 1_000, 5)
        start_diameter = round(bend.diameter * 1_000, 5)

        end_x = round(bend.end.x * 1_000, 5)
        end_y = round(bend.end.y * 1_000, 5)
        end_z = round(bend.end.z * 1_000, 5)
        end_diameter = round(bend.diameter * 1_000, 5)

        centre_x = round(bend.corner.x *1_000, 5)
        centre_y = round(bend.corner.y *1_000, 5)
        centre_z = round(bend.corner.z *1_000, 5)

        thk = round(bend.thickness *1_000, 5)

        string = (
            "ELBOW \n"
            f"    END-POINT {start_x:>14}  {start_y:>14} {start_z:>14} {start_diameter:>14} \n"
            f"    END-POINT {end_x:>14}  {end_y:>14} {end_z:>14} {end_diameter:>14} \n"
            f"    CENTRE-POINT {centre_x:>14}  {centre_y:>14} {centre_z:>14} \n"
            f"    R2_WALL_THK {thk:>14} \n"
             "    SKY EBSC"
        )
        return string

    