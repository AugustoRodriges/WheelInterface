import serial

# Configurações da porta serial
PORTA_SERIAL = 'COM4'  # Altere para a porta correta
BAUD_RATE = 115200  # Taxa de baud

def configurar_serial():
    """Configura a comunicação serial com o Arduino."""
    try:
        ser = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
        print(f"Conectado na porta {PORTA_SERIAL} com {BAUD_RATE} bps")
        return ser
    except serial.SerialException as e:
        print(f"Erro ao abrir a porta serial: {e}")
        return None

def ler_e_imprimir_dados(ser):
    """Lê e imprime os 10 bytes recebidos da comunicação serial."""
    while True:
        # Ler 10 bytes de dados
        data = ser.read(6)
        
        if len(data) == 6:
            print((data[2] | (data[3] << 8)) & 0x03FF)
        else:
            print(f"Erro: esperava 8 bytes, mas recebi {len(data)} bytes.")

def main():
    ser = configurar_serial()
    if ser is None:
        return

    ler_e_imprimir_dados(ser)

if __name__ == "__main__":
    main()
