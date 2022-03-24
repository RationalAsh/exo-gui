from curses import wrapper
import curses
import time
import serial
from serial.tools.list_ports import comports

def initialize_port():
    """
    Initialize the serial port.
    :return:
    """
    plist = comports()
    selected = []
    print("Checking for serial ports....")
    print("Found:")
    for i, p in enumerate(plist):
        print("{}. {}".format(i, p))
        if 'usbserial' in p.device:
            selected.append(p)
    print(selected)
    if len(selected) == 1:
        print("Selecting {}".format(selected[0]))
        return serial.Serial(selected[0].device, 500000)
    else:
        print("Could not find appropriate port.")
        return None

def main(stdscr):
    """
    The curses application
    :param stdscr:
    :return:
    """
    # Get serial port
    serial_port = initialize_port()

    # Clear screen
    stdscr.clear()
    ctr = 0
    while True:
        time.sleep(0.01)
        ctr += 1
        stdscr.addstr(0, 10, "Back Exo",
                      curses.A_REVERSE)
        sdata_bytes = serial_port.read(1024)
        sdata = sdata_bytes.decode('utf-8')
        datalines = sdata.strip().split("\n")
        datavals = datalines[-2].split(',')
        datavals_float = [float(i) for i in datavals]
        stdscr.addstr(1, 5, "  Force Command: {:.2f}".format(datavals_float[2]),
                      curses.A_REVERSE)
        stdscr.addstr(2, 5, " Left Hip Angle: {:.2f}".format(datavals_float[3]*0.1),
                      curses.A_REVERSE)
        stdscr.addstr(3, 5, "Right Hip Angle: {:.2f}".format(datavals_float[4]*0.1),
                      curses.A_REVERSE)
        stdscr.refresh()


    stdscr.refresh()
    stdscr.getkey()

if __name__ == '__main__':
    wrapper(main)