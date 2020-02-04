
class OpenPulseError():
    
    #Sucess
    PULSE_SUCESS = 0

    #3DLinesErrors
    PULSE_3DLINE_INVALID_VERTICE = 1

    ERRON = {
        PULSE_SUCESS: "Sucess",
        PULSE_3DLINE_INVALID_VERTICE: "Vertex Coordinate Error"
    }

    @staticmethod
    def erron(erron):
        print(OpenPulseError.ERRON[erron])

a = OpenPulseError()
print(OpenPulseError.ERRON[OpenPulseError.PULSE_SUCESS])