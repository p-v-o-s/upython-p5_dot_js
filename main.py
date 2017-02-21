import time
import machine
from micropython import mem_info

print("main.py running:")
mem_info()
print("Waiting for connection on UART 0...",end="")
time.sleep(1.0)

uart = machine.UART(0, 115200)# init with given baudrate

uart.init(115200, bits=8, parity=None, stop=1, timeout=1000) # init with given parameters
msg = uart.read(1)

if msg is None:
    print("timed out.")
    print("Loading p5js_app")
    import p5js_app
else:
    print(msg)
    print("Rerouting to REPL")
