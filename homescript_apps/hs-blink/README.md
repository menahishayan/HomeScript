# hs-blink

Automation script to Blink an accessory for example a light or smart plug.

The script is executed on an infinite loop to exit, CTRL + C.

### Setup a python script as a service through systemctl/systemd

**sudo nano /etc/systemd/system/blink.service**

```
[Unit]
Description=Blink Accessory Aervice
After=multi-user.target
[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /home/pi/HomeScript/blink.py
[Install]
WantedBy=multi-user.target
```

Reload the daemon.

```
sudo systemctl daemon-reload
```

Enable the service so that it doesn’t get disabled if the server restarts.

```
sudo systemctl enable blink.service
```

Start service.

```
sudo systemctl start blink.service
```

Now the service is up and running.

There are several commands to start, stop, restart, and check status.

To stop the service.

```
sudo systemctl stop blink
```

To restart.

```
sudo systemctl restart blink
```

To check status.

```
sudo systemctl status blink
```

