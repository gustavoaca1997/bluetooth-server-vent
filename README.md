# Bluetooth Server for an Emergency Ventilator (E-Vent)

## Instalation
_Warning: The order of the steps is not guaranteed to be succesful, neither every step is guaranteed to be necessary. TODO: Improve these steps._
### OS Dependencies
```bash
sudo apt-get install bluez bluez-utils
sudo apt-get install python-dev
sudo apt-get install libbluetooth-dev
```

#### Solve bug starting a SDP server
Follow [these steps](https://raspberrypi.stackexchange.com/a/42262/119007) for successfully starting the bluetooth server.

### Python dependencies
See [requirements.txt](./requirements.txt)

## Usage
Start Bluetooth server with
```bash
python server_uuid.py
```

Then from your Android App scan to find the server and then connect to it. You can now send bytes as messages. The servers was implemented to parse JSON messages that are similar to this one:

```json
{
    "RR": 8,
    "TV": 200,
    "I/E": [1, 2]
}
```

You can send an `"exit"` message to kill the server. Any other kind of message would be ignored or raise `"Parsing error"`.

## Tested app
The server was tested with the app [Serial Bluetooth Terminal](https://play.google.com/store/apps/details?id=de.kai_morich.serial_bluetooth_terminal), whose UUID is `"00001101-0000-1000-8000-00805F9B34FB"`, that is why that UUID is written in the script code.