# Bluetooth Server for an Emergency Ventilator (E-Vent)

## Instalation

### OS Dependencies
_Warning: The order of the following steps is not guaranteed to be succesful, neither every step is guaranteed to be necessary. TODO: Improve these steps._

```bash
sudo apt-get install bluez bluez-utils
sudo apt-get install python-dev
sudo apt-get install libbluetooth-dev
```

### Solve bug starting a SDP server
Follow [these steps](https://raspberrypi.stackexchange.com/a/42262/119007) for successfully starting the bluetooth server.

### Python dependencies
See [requirements.txt](./requirements.txt)

## Usage
Start Bluetooth server with
```bash
python server_uuid.py
```

If you get `bluetooth.btcommon.BluetoothError: no advertisable device` error, please run the following command to make the device discoverable:
```bash
sudo hciconfig hci0 piscan
```

Then from your Android App scan to find the server and then connect to it. You can now send bytes as messages. The server was implemented to parse JSON messages that are similar to this one:

```json
{
    "RR": 8,
    "TV": 200,
    "I/E": [1, 2]
}
```

Each field corresponds to one of these parameters:
- Respiratory Rate (RR) (breaths per minute): between 8 – 40.
- Tidal Volume (TV) (air volume pushed into lung): between 200 – 800 mL based on patient weight.
- I/E Ratio (inspiratory/expiration time ratio): recommended to start around 1:2; best if adjustable between range of 1:1 – 1:4*.

You can send an `"exit"` message to kill the server. Any other kind of message will be ignored or raise `"Parsing error"`.

## Tested app
The server was tested with the app [Serial Bluetooth Terminal](https://play.google.com/store/apps/details?id=de.kai_morich.serial_bluetooth_terminal), whose UUID is `"00001101-0000-1000-8000-00805F9B34FB"`, that is why that UUID is written in the script code.

## Inspiration
This script is supposed to evolve into a Raspberry Pi program that will be used to implement a ventilator inspired on the [MIT E-Vent](https://e-vent.mit.edu/).

The script was inspired on [this example](https://github.com/pybluez/pybluez/blob/master/examples/simple/rfcomm-server.py), using the [PyBluez library](https://pybluez.readthedocs.io/en/latest/index.html).

The communication between the controller Android app and the server could be based on [this open source Android app](https://github.com/kai-morich/SimpleBluetoothTerminal).
