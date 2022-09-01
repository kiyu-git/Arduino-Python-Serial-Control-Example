import datetime
import glob
import sys
import time

import schedule
import serial


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


def job_on():
    print(datetime.datetime.now(), "ON")
    arduinoData.write(bytes("1", encoding="ascii"))


def job_off():
    print(datetime.datetime.now(), "OFF")
    arduinoData.write(bytes("0", encoding="ascii"))


if __name__ == "__main__":
    arduinoData = serial.Serial(get_serial_port(), 9600)
    schedule.every().hour.at(":10").do(job_on)
    schedule.every().hour.at(":20").do(job_off)
    schedule.every().hour.at(":30").do(job_on)
    schedule.every().hour.at(":40").do(job_off)
    schedule.every().hour.at(":50").do(job_on)
    schedule.every().hour.at(":00").do(job_off)

    while True:
        schedule.run_pending()
        time.sleep(1)
