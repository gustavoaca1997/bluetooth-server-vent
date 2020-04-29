#!/usr/bin/env python3
"""PyBluez simple example rfcomm-server.py

Simple demonstration of a server application that uses RFCOMM sockets.

Original author: Albert Huang <albert@csail.mit.edu>
Adaptations to MIT E-Vent: Gustavo Castellanos <gustavoaca1997@gmail.com> 
"""

import bluetooth
import json

###############################################################################################################

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

# Este es el UUID "cableado" en la app Serial Bluetooth Terminal (https://play.google.com/store/apps/details?id=de.kai_morich.serial_bluetooth_terminal)
uuid = "00001101-0000-1000-8000-00805F9B34FB"

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            )

print("Waiting for connection on RFCOMM channel", port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

###############################################################################################################

# Parametros para el Ventilator
RR = "RR"
TV = "TV"
IE = "I/E"
vent_params = [RR, TV, IE]

# Valores iniciales
vent_values = {
    RR: 8.0,            # Respiratory Rate (RR) (breaths per minute): between 8 – 40.
    TV: 200.0,          # Tidal Volume (TV) (air volume pushed into lung): between 200 – 800 mL based on patient weight.
    IE: [1.0, 2.0],     # I/E Ratio (inspiratory/expiration time ratio): recommended to start around 1:2; best if adjustable between range of 1:1 – 1:4.
}

vent_params_names = {
    RR: "Respiratory Rate (RR)",
    TV: "Tidal Volume (TV) (air volume pushed into lung)",
    IE: "I/E Ratio (inspiratory/expiration time ratio)"
}

# Funciones que procesan a los parametros. Estas serán las que se comuniquen con la salida de la Raspberry Pi

# Por ahora solo imprimen en stdout

def rr_func(rr):
    if 8 <= rr and rr <= 40:
        print("{} updated to {}.".format(vent_params_names[RR], rr))
        vent_values[RR] = rr
    else:
        print("{} out of range.".format(vent_params_names[RR]))

def tv_func(tv):
    if 200 <= tv and tv <= 800:
        print("{} updated to {}.".format(vent_params_names[TV], tv))
        vent_values[TV] = tv
    else:
        print("{} out of range.".format(vent_params_names[TV]))

def ie_func(ie):
    if 0 < ie[0] and 0 < ie[1] and ie[0] <= ie[1]:
        print("{} updated to {}:{}".format(vent_params_names[IE], ie[0], ie[1]))
        vent_values[IE] = ie
    else:
        print("{} has wrong value.".format(vent_params_names[IE]))

vent_funcs = {
    RR: rr_func,
    TV: tv_func,
    IE: ie_func,
}

###############################################################################################################

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            continue

        data = data.strip() # trim

        if data == b"exit":
            break

        try:
            in_values = json.loads(data) # parse dictionary

            for param in vent_params:
                if param in in_values:
                    new_value = in_values[param]
                    vent_funcs[param](new_value)

        except json.decoder.JSONDecodeError:
            print("Parsing error")

except OSError:
    pass

print("Disconnected.")

client_sock.close()
server_sock.close()
print("All done.")
