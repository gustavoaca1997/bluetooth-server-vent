#!/usr/bin/env python3
"""PyBluez simple example rfcomm-server.py

Simple demonstration of a server application that uses RFCOMM sockets.

Original author: Albert Huang <albert@csail.mit.edu>
Adaptations to MIT E-Vent: Gustavo Castellanos <gustavoaca1997@gmail.com> 
"""

import bluetooth
import select
import serial
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

###############################################################################################################

ser = serial.Serial('/dev/ttyACM0', 9600)

###############################################################################################################

# Parametros para el Ventilator
RR = "RR"
TV = "TV"
IE = "I/E"
vent_params = [RR, TV, IE]

vent_params_names = {
    RR: "Respiratory Rate (RR)",
    TV: "Tidal Volume (TV) (air volume pushed into lung)",
    IE: "I/E Ratio (inspiratory/expiration time ratio)"
}

# Funciones que procesan a los parametros. Estas serán las que se comuniquen con la salida de la Raspberry Pi

# Por ahora solo imprimen en stdout
encoding = 'utf-8'
byteError = 'Byte \'{}\' not written.'
bytesError = 'Error writing \'{}\' as bytes.'
endCharacter = ':'

def sendByte(c):
    strToWrite = c.decode(encoding) + endCharacter
    assert ser.write(bytes(strToWrite, encoding=encoding)) > 1, bytesError.format(strToWrite)

def tv_func(tv):
    if 200 <= tv and tv <= 800:
        strToWrite = 'V' + "{:.3}".format(tv) + endCharacter
        assert ser.write(bytes(strToWrite, encoding=encoding)) > 1, bytesError.format(strToWrite)
    else:
        raise ValueError("{} out of range.".format(vent_params_names[TV]))

def rr_func(rr):
    if 8 <= rr and rr <= 40:
        strToWrite = 'R'+ "{:.3}".format(rr) + endCharacter
        assert ser.write(bytes(strToWrite, encoding=encoding)) > 1, bytesError.format(strToWrite)

    else:
        raise ValueError("{} out of range.".format(vent_params_names[RR]))

def ie_func(ie):
    if 0 < ie[0] and 0 < ie[1] and ie[0] <= ie[1]:
        strPair = "{:.3}".format(float(ie[0])/float(ie[1]))
        strToWrite = 'I' + strPair + endCharacter
        assert ser.write(bytes(strToWrite, encoding=encoding)) > 1, bytesError.format(strToWrite)
    else:
        raise ValueError("{} has wrong value.".format(vent_params_names[IE]))

vent_funcs = {
    RR: rr_func,
    TV: tv_func,
    IE: ie_func,
}

###############################################################################################################

try:
    print("Waiting for connection on RFCOMM channel", port)
    client_sock, client_info = server_sock.accept()
    client_sock.setblocking(0)
    print("Accepted connection from", client_info)

    while True:
        while (ser.in_waiting):
                ou = ser.readline()
                print('Output:', ou.decode(encoding), end='')

        sock_ready = select.select([client_sock], [], [], 5)[0]
        if not sock_ready:
            continue
        data = client_sock.recv(1024)
        if not data:
            continue

        data = data.strip() # trim

        if data == b"exit": # shutdown server
            break

        if data == b"0":    # turn off bluetooth mode
            sendByte(data)
            continue

        try:
            in_values = json.loads(data) # parse dictionary

            for param in vent_params:
                if param in in_values:
                    new_value = in_values[param]
                    vent_funcs[param](new_value)

        except json.decoder.JSONDecodeError:
            print("Parsing error.")
        except ValueError as e:
            print('Data has errors:', e)
        except AssertionError as e:
            print('An assertion error occurred:', e)
        except bluetooth.btcommon.BluetoothError as e:
            print('A Bluetooth error occurred:', e)
        except Exception as e:
            print('An unexpected error occurred:', e)

except Exception as e:
    print('Something bad happened:', type(e))
finally:
    print("Disconnected.")

    try:
        client_sock.close()
    except:
        pass
    server_sock.close()
    ser.close()
    print("All done.")
