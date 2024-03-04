import minimalmodbus
import time
import serial.tools.list_ports

def select_com_port():
    # Get a list of available COM ports
    com_ports = serial.tools.list_ports.comports()

    # Print the list of available COM ports
    print("Available COM ports:")
    for port in com_ports:
        print(port.device)

    # Ask the user to select a COM port
    selected_port = input("Enter the COM port to use (e.g., COM1): ")

    return selected_port

selected_port = select_com_port()
print("Selected COM port:", selected_port)

# Configure Temperature device
instrument_port = (selected_port)  # Change this to match your device's port
instrument_address = 32  # Change this to match your device's address
instrument_baudrate = 4800
instrument_bytesize = 8
instrument_parity = 'N'
instrument_stopbits = 1
instrument_timeout = 2

# Configure Power Meter device
instrument1_port = (selected_port)  # Change this to match your device's port
instrument1_address = 9  # Change this to match your device's address
instrument1_baudrate = 4800
instrument1_bytesize = 8
instrument1_parity = 'N'
instrument1_stopbits = 1
instrument1_timeout = 2

# Define the Modbus register addresses for temperature and humidity
TEMPERATURE_REGISTER = 1
HUMIDITY_REGISTER = 0

# Define the Modbus register addresses for ABB voltage
REGISTER_A = 23296 #5B00 HEX
REGISTER_B = 23296 #5B00 HEX
REGISTER_C = 20480 #5000 HEX
REGISTER_D = 20480 #5000 HEX

def read_temperature_and_humidity():
    try:
        instrument = minimalmodbus.Instrument(instrument_port, instrument_address)
        instrument.serial.baudrate = instrument_baudrate
        instrument.serial.bytesize = instrument_bytesize
        instrument.serial.parity = instrument_parity
        instrument.serial.stopbits = instrument_stopbits
        instrument.serial.timeout = instrument_timeout

        temperature = instrument.read_register(TEMPERATURE_REGISTER, functioncode=3)
        humidity = instrument.read_register(HUMIDITY_REGISTER, functioncode=3)

        return temperature, humidity

    except Exception as e:
        print("Error:", e)
        return None, None
        
def read_meter():
    try:
        instrument1 = minimalmodbus.Instrument(instrument1_port, instrument1_address)
        instrument1.serial.baudrate = instrument1_baudrate
        instrument1.serial.bytesize = instrument1_bytesize
        instrument1.serial.parity = instrument1_parity
        instrument1.serial.stopbits = instrument1_stopbits
        instrument1.serial.timeout = instrument1_timeout

        var1 = instrument1.read_long(REGISTER_A, functioncode=3, signed=False, byteorder=0, number_of_registers: int = 2)
        var2 = instrument1.read_float(REGISTER_B, functioncode=3, number_of_registers=2, byteorder=0)
        var3 = instrument1.read_long(REGISTER_C, functioncode=3, signed=False, byteorder=0, number_of_registers: int = 4)
        var4 = instrument1.read_float(REGISTER_D, functioncode=3, number_of_registers=4, byteorder=0)
        
        return var1, var2, var3, var4

    except Exception as e:
        print("Error:", e)
        return None, None

try:
    while True:
        temperature, humidity = read_temperature_and_humidity()
        if temperature is not None and humidity is not None:
            print("Temperature:",(temperature/10),"°C", end=' / ')
            print("Humidity:",(humidity/10),"%")
            # Wait for a short duration before reading again
            time.sleep(5)  # Adjust as needed
        
        var1, var2, var3, var4 = read_meter()
        if var1 is not None and var2 is not None and var3 is not None and var4 is not None:
            print("Voltage L1:",var1, end=' / ')
            print("Voltage L1 float:",var2, end=' / ')
            print("Active Import:",var3, end=' / ')
            print("Active Import float:", var4)
            # Wait for a short duration before reading again
            time.sleep(5)  # Adjust as needed            
            
except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C) to gracefully exit the loop
    print("Exiting...")
