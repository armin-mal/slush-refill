import serial
import serial.tools.list_ports
import re
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as ticker

BAUDRATE = 115200
MAX_DATENPUNKTE = 50


def find_stm32_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        desc = port.description.lower()
        if "stmicroelectronics" in desc or "nucleo" in desc or "mbed" in desc:
            print(f"STM32 automatisch gefunden: {port.device} ({port.description})")
            return port.device
    for port in ports:
        desc = port.description.lower()
        if "usb" in desc or "serial" in desc or "ch340" in desc or "cp210" in desc or "ftdi" in desc:
            print(f"Möglicher USB-Serial-Adapter gefunden: {port.device} ({port.description})")
            return port.device
    if len(ports) == 1:
        print(f"Nur ein COM-Port aktiv. Verwende: {ports[0].device} ({ports[0].description})")
        return ports[0].device
    return None

PORT = find_stm32_port()

if PORT is None:
    print("Fehler: Kein STM32 oder USB-Serial-Port gefunden!")
    print("Verfügbare Ports waren:")
    for p in serial.tools.list_ports.comports():
        print(f" - {p.device}: {p.description}")
    exit()

x_data = collections.deque(maxlen=MAX_DATENPUNKTE)
y_data = collections.deque(maxlen=MAX_DATENPUNKTE)
pattern = re.compile(r"Distance\s*=\s*(\d+)\s*mm")

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print(f"Erfolgreich mit {PORT} verbunden. Warte auf Daten...")
except Exception as e:
    print(f"Fehler beim Öffnen des Ports {PORT}: {e}")
    exit()

fig, ax1 = plt.subplots()
line, = ax1.plot([], [], 'r-', lw=2, marker='o', markersize=4)
ax1.set_title("Live-Distanzmessung (SEN0592)")
ax1.set_xlabel("Messung (Index)")
ax1.set_ylabel("Distanz (mm)", color='r')
ax1.tick_params(axis='y', labelcolor='r')
ax1.set_ylim(200, 0)
ax1.yaxis.set_major_locator(ticker.MultipleLocator(10))
ax1.grid(True)

ax2 = ax1.twinx()
ax2.set_ylabel("Distanz (cm)", color='b')
ax2.tick_params(axis='y', labelcolor='b')
ax2.set_ylim(20, 0)
ax2.yaxis.set_major_locator(ticker.MultipleLocator(1))

def init():
    line.set_data([], [])
    return line,

counter = 0

def update(frame):
    global counter
    if ser.in_waiting > 0:
        try:
            line_bytes = ser.readline()
            line_str = line_bytes.decode('utf-8', errors='ignore').strip()
            match = pattern.search(line_str)
            if match:
                distance_mm = int(match.group(1))
                counter += 1
                x_data.append(counter)
                y_data.append(distance_mm)
                print(f"Empfangen: {distance_mm} mm ({distance_mm / 10.0} cm)")
                line.set_data(x_data, y_data)
                ax1.set_xlim(min(x_data), max(x_data))
        except Exception as e:
            print(f"Fehler bei der Datenverarbeitung: {e}")
    return line,

ani = animation.FuncAnimation(fig, update, init_func=init, interval=100, blit=False, cache_frame_data=False)

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    ser.close()
    print("Verbindung geschlossen.")