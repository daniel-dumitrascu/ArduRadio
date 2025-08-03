#!/bin/bash

BLUETOOTH_USERNAME="daniel"
BLUETOOTH_CONFIG="/etc/bluetooth/main.conf"
BLUETOOTH_COMMANDS="power on,discoverable on,pairable on,agent on,default-agent,quit"
BT_AGENT_SERVICE="/etc/systemd/system/bt-agent.service"
BT_AGENT_SERVICE_CONTENT="[Unit]\nDescription=Bluetooth Auth Agent\nAfter=bluetooth.service\nPartOf=bluetooth.service\n\n[Service]\nType=simple\nExecStart=/usr/bin/bt-agent -c NoInputNoOutput\n\n[Install]\nWantedBy=bluetooth.target\n"

echo " --> Add the user $BLUETOOTH_USERNAME to the bluetooth group, allowing it to access or control Bluetooth devices"
usermod -a -G bluetooth "$BLUETOOTH_USERNAME"

echo " --> Append the line Class = 0x41C to the end of the file $BLUETOOTH_CONFIG"
sed -i '$a Class = 0x41C' "$BLUETOOTH_CONFIG"

echo " --> Set the device to stays discoverable indefinitely, which is useful for persistent pairing availability."
sed -i '$a DiscoverableTimeout = 0' "$BLUETOOTH_CONFIG"

echo " --> Restart bluetooth module"
systemctl restart bluetooth

echo " --> Execute bluetooth commands"
bluetoothctl <<EOF
$(echo "$BLUETOOTH_COMMANDS" | tr ',' '\n')
EOF

echo " --> Start pulseaudio"
pulseaudio --start

echo " --> Check the status of the bluetooth module"
BLUETOOTH_STATUS=$(systemctl status bluetooth | grep 'Active:' | awk '{print $2, $3}' | tr -d '()')
if [[ "$BLUETOOTH_STATUS" == "active running" ]]; then
    echo "Bluetooth is active and running"
else
    echo "Bluetooth didn't start, script will not continue and it exit now!"
    exit 1
fi

echo " --> Setup pulseaudio so that it starts at boot"
systemctl --user enable pulseaudio

echo " --> Check if the service bt-agent.service exists. If not, then create it"
if [ ! -f "$BT_AGENT_SERVICE" ]; then
    echo "Create the service"
    touch "$BT_AGENT_SERVICE"
    echo "Adding the service content"
    echo "$BT_AGENT_SERVICE_CONTENT" > "$BT_AGENT_SERVICE"
fi

echo "Enable and start the bt-agent"
systemctl enable bt-agent
systemctl start bt-agent