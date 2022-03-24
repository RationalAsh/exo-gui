import asyncio
import serial
from serial.tools.list_ports import comports
from serial.serialutil import SerialException
from signal import SIGINT, SIGTERM

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

async def serial_task():
    """
    Async task for serial port monitoring.
    :return: 
    """
    port = initialize_port()
    max_reconnects = 10
    reconnect_count = 0

    if port:
        while True:
            try:
                sdata = port.read(1024)
                print("Got {} chars of data".format(len(sdata)))
                await asyncio.sleep(0.01)
            except asyncio.CancelledError:
                port.close()
                break
            except:
                print("Serial port disconnected.")
                print("Trying to reconnect...")
                port = initialize_port()

                if port is None:
                    print("Failed to read.")
    else:
        pass

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    stask = loop.create_task(serial_task())
    try:
        loop.run_until_complete(stask)
    except KeyboardInterrupt as e:
        print("Caught keyboard interrupt. Canceling tasks...")
        stask.cancel()
    finally:
        loop.close()