import datetime
import glob
import sys

import serial

# set OSC
from pythonosc import osc_server, udp_client
from pythonosc.dispatcher import Dispatcher

recieve_port = 4000

# set osc
def light_ctl(unused_addr, *args):
    print(unused_addr, args[0])
    new_state = args[0]
    arduinoData.write(bytes(str(new_state), encoding="ascii"))


def start_osc_server(IP, PORT):
    dispatcher = Dispatcher()
    dispatcher.map("/light", light_ctl)

    server = osc_server.ThreadingOSCUDPServer((IP, PORT), dispatcher)
    print(f"Serving on {server.server_address}")
    server.serve_forever()


# serial communication
def get_serial_port():
    # Reads the available serial ports
    if sys.platform.startswith("win"):
        ports = ["COM%s" % (i + 1) for i in range(256)]
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        ports = glob.glob("/dev/tty[A-Za-z]*")
    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")
    else:
        raise EnvironmentError("Unsupported platform")

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    for index, item in enumerate(result):
        print("[" + str(index) + "]", item)

    usb = input("Enter port number : ")
    return result[int(usb)]


if __name__ == "__main__":
    arduinoData = serial.Serial(get_serial_port(), 9600)
    start_osc_server("127.0.0.1", recieve_port)
