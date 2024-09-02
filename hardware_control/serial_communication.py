import serial

class ArduinoWheel:
    def __init__(self, arduino_port, bps):
        self.arduino = serial.Serial(arduino_port, bps, timeout=1)

        self.pedals_data = [None, None, None]
        self.wheel_data = None
    
    def get_data(self):
        # Ler 10 bytes de dados
        data = self.arduino.read(10)

        if len(data) != 10:
            return None

        # Separar os bytes para valores analógicos (cada valor é 10 bits)
        self.pedals_data[0] = (data[0] | (data[1] << 8)) & 0x03FF  # Ajusta para 10 bits
        self.pedals_data[1] = (data[2] | (data[3] << 8)) & 0x03FF  # Ajusta para 10 bits
        self.pedals_data[2] = (data[4] | (data[5] << 8)) & 0x03FF  # Ajusta para 10 bits

        # Reconstrução do valor do encoder (int32_t)
        self.wheel_data = (data[6] | (data[7] << 8) | (data[8] << 16) | (data[9] << 24))

        # Ajuste para valores negativos
        # Para garantir a interpretação correta de int32_t com sinal, você pode usar `& 0xFFFFFFFF` para tratar o valor como unsigned antes do ajuste
        if self.wheel_data & 0x80000000:  # Checa o bit de sinal (bit mais significativo)
            self.wheel_data -= 0x100000000  # Ajusta o valor para o intervalo negativo

        return self.wheel_data
    
