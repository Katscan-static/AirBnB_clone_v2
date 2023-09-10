#!/usr/bin/env bash
# install nginx and configure it

if ! dpkg -l | grep -q nginx; then
	sudo apt-get update
	sudo apt-get install nginx
fi

sudo mkdir -p /data/web_static/{releases/test,shared}
echo "<html>
	<head>
	</head>
	<body>
		Hello, this is a test page.
	</body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
addition_hbnb="\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n"
sudo sed -i "\$i\\$addition_hbnb" /etc/nginx/sites-available/default

sudo service nginx restart
exit 0
