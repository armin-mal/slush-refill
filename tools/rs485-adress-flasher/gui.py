import tkinter as tk
from tkinter import messagebox, ttk
import threading
import minimalmodbus
import serial.tools.list_ports

def get_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def refresh_ports():
    ports = get_ports()
    port_picker["values"] = ports
    if port_var.get() not in ports:
        port_var.set(ports[0] if ports else "")

def check_addresses():
    port = port_var.get()
    if not port:
        messagebox.showerror("Fehler", "Bitte zuerst einen COM-Port auswählen.")
        return

    check_button.config(state="disabled")
    port_picker.config(state="disabled")
    refresh_button.config(state="disabled")
    status_var.set("Suche Modbus-Geräte am ausgewählten Port ...")

    def scan():
        found = []
        for address in range(1, 248):
            instrument = None
            try:
                instrument = minimalmodbus.Instrument(port, address)
                instrument.serial.baudrate = 9600
                instrument.serial.timeout = 0.15
                register_value = instrument.read_register(512, functioncode=3)
                found.append((address, register_value))
            except Exception:
                pass
            finally:
                if instrument is not None:
                    try:
                        instrument.serial.close()
                    except Exception:
                        pass
        root.after(0, finish_scan, found)

    threading.Thread(target=scan, daemon=True).start()

def finish_scan(found):
    check_button.config(state="normal")
    port_picker.config(state="readonly")
    refresh_button.config(state="normal")
    if not found:
        status_var.set("Kein Gerät mit lesbarem Register 512 gefunden.")
        return

    old_addr_entry.delete(0, tk.END)
    old_addr_entry.insert(0, str(found[0][0]))
    results = ", ".join(
        f"Adresse {address} (Registerwert {value})" for address, value in found
    )
    status_var.set(f"Gefunden: {results}")

def change_address():
    port = port_var.get()
    try:
        old_addr = int(old_addr_entry.get())
        new_addr = int(new_addr_entry.get())
        if not port:
            raise ValueError("Bitte zuerst einen COM-Port auswählen.")
        if not 1 <= old_addr <= 247 or not 1 <= new_addr <= 247:
            raise ValueError("Modbus-Adressen müssen zwischen 1 und 247 liegen.")
        
        # Verbindung zum Sensor herstellen (Standard: 9600 Baud, Modbus RTU)
        instrument = minimalmodbus.Instrument(port, old_addr)
        instrument.serial.baudrate = 9600
        instrument.serial.timeout = 1.0
        
        # Register 0x0200 (dezimal 512) mit neuer Adresse überschreiben (Function Code 0x06)
        instrument.write_register(512, new_addr, functioncode=6)
        
        messagebox.showinfo("Erfolg", f"Die Adresse wurde erfolgreich von {old_addr} auf {new_addr} geändert.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Kommunikationsfehler:\n{e}")

# GUI erstellen
root = tk.Tk()
root.title("RS-485 Adress-Flasher")
root.geometry("440x330")
root.resizable(False, False)

tk.Label(root, text="COM-Port:").pack(pady=(14, 4))
port_var = tk.StringVar(root)
port_picker = ttk.Combobox(root, textvariable=port_var, state="readonly", width=24)
port_picker.pack()
refresh_button = ttk.Button(root, text="Ports aktualisieren", command=refresh_ports)
refresh_button.pack(pady=5)
refresh_ports()

tk.Label(root, text="Aktuelle Geräteadresse:").pack(pady=(12, 4))
old_addr_entry = tk.Entry(root)
old_addr_entry.pack()
check_button = ttk.Button(root, text="Adresse checken", command=check_addresses)
check_button.pack(pady=7)
status_var = tk.StringVar(root, value="Noch keine Adresse geprüft.")
tk.Label(root, textvariable=status_var, wraplength=410, justify="center").pack(pady=3)

tk.Label(root, text="Neue Adresse (1 bis 247):").pack(pady=(12, 4))
new_addr_entry = tk.Spinbox(root, from_=1, to=247, width=8)
new_addr_entry.delete(0, tk.END)
new_addr_entry.insert(0, "2")
new_addr_entry.pack()

ttk.Button(root, text="Adresse schreiben", command=change_address).pack(pady=16)

root.mainloop()