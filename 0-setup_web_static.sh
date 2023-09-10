#!/usr/bin/env bash
# install nginx and configure it

if ! dpkg -l | grep -q nginx; then
	sudo apt-get update
	sudo apt-get install nginx
fi

sudo mkdir -p /data/web_static/{releases/test,shared}
echo "<html><head></head><body>Hello, this is a test page.</body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
nginx_config="/etc/nginx/sites-available/default"
echo "server {
    location /hbnb_static/ {
        alias /data/web_static/current/;
    }

    # Additional server configuration...
}" | sudo tee "$nginx_config" > /dev/null
sudo service nginx restart
exit 0
