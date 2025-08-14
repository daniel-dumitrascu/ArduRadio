#!/bin/bash

BLUETOOTH_USERNAME="daniel"
BLUETOOTH_CONFIG="/etc/bluetooth/main.conf"
BT_AGENT_FILENAME="bt-agent.service"
BT_AGENT_SERVICE_PATH="/etc/systemd/system/$BT_AGENT_FILENAME"
BT_AGENT_SERVICE_CONTENT="[Unit]
Description=Bluetooth Auth Agent
After=bluetooth.service
PartOf=bluetooth.service

[Service]
Type=simple
ExecStart=/usr/bin/bt-agent -c NoInputNoOutput

[Install]
WantedBy=bluetooth.target
"

echo " --> Add the user $BLUETOOTH_USERNAME to the bluetooth group, allowing it to access or control Bluetooth devices"
sudo usermod -a -G bluetooth "$BLUETOOTH_USERNAME"

echo " --> Append the line Class = 0x41C to the end of the file $BLUETOOTH_CONFIG"
sudo sed -i '$a Class = 0x41C' "$BLUETOOTH_CONFIG"

echo " --> Set the device to stays discoverable indefinitely, which is useful for persistent pairing availability."
sudo sed -i '$a DiscoverableTimeout = 0' "$BLUETOOTH_CONFIG"

echo " --> Restart bluetooth module"
sudo systemctl restart bluetooth

echo " --> Execute bluetooth commands"
{
  echo "power on"
  sleep 1
  echo "discoverable on"
  sleep 1
  echo "pairable on"
  sleep 1
  echo "agent on"
  sleep 1
  echo "default-agent"
  sleep 1
  echo "quit"
} | bluetoothctl &

sleep 10

echo " --> Start pulseaudio"
pulseaudio --start

sleep 5

echo " --> Check the status of the bluetooth module"
BLUETOOTH_STATUS=$(systemctl status bluetooth | grep 'Active:' | awk '{print $2, $3}' | tr -d '()')
if [[ "$BLUETOOTH_STATUS" == "active running" ]]; then
    echo "Bluetooth is active and running"
else
    echo "Bluetooth didn't start, script will not continue and it exit now!"
    exit 1
fi

echo " --> Setup pulseaudio so that it starts at boot"
sudo systemctl --user enable pulseaudio

echo " --> Create the service bt-agent.service"
touch "$BT_AGENT_FILENAME"  
  
echo " --> Adding the service content"
echo "$BT_AGENT_SERVICE_CONTENT"
echo "$BT_AGENT_SERVICE_CONTENT" > "$BT_AGENT_FILENAME"
    
echo " --> Move service file to the right location"
sudo mv "$BT_AGENT_FILENAME" "$BT_AGENT_SERVICE_PATH"

echo " --> Enable and start the bt-agent"
sudo systemctl enable bt-agent
sudo systemctl start bt-agent
