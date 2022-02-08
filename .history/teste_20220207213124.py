import sys

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            if port.manufacturer:
                print(port.device + ': ' + port.manufacturer)
            else:
                print(port.device + ': No Manufacturer Listed')
        except AttributeError:
            print("\nThis utility requires that pyserial version 3.4 or greater is installed.")
            sys.exit(0)