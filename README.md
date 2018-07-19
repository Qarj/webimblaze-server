# webinject-server 0.1.0

WebInject Server is a project for running WebInject over http.

Run an existing script via a GET. Example: http://localhost/webinject/server/run/?path=test.test

Or submit a test script to run using POST.

The main WebInject project is here: http://qarj.github.io/WebInject

## Deploy on Windows

To get WebInject Server working there are additional dependecies on Python 3, Apache and mod_wsgi. 
The setup is explained in the project test-results-dashboard. Rather than repeat the instructions
here, it is no harder to actually deploy the other project. So do that now and the dependencies will
be satisfied.

Deploy:
- https://github.com/Qarj/test-results-dashboard

Clone this project:
```
cd /d C:\
mkdir git
cd git
git clone https://github.com/Qarj/webinject-server.git
cd webinject-server
```

### Configure Apache to point to webinject-server

Restart Apache
```
\Apache24\bin\httpd -k restart
```

verify with url: http://localhost/webinject/server

Check the error logs
```
type C:\Apache24\logs\error.log
```

Note that in `C:\Apache24\conf\httpd.conf` you can change `LogLevel warn` to `LogLevel debug` for
additional log info.

## Deploy on Linux

Requires Python 3, tested with Python 3.5.2 and 3.6.5.

Deploy these projects to the recommended location:
- https://github.com/Qarj/WebInject
- https://github.com/Qarj/WebInject-Framework

Optionally deploy if you want to use Selenium too:
- https://github.com/Qarj/WebInject-Selenium

To get WebInject Server working there are additional dependecies on Python 3, Apache and mod_wsgi. 
The setup is explained in the project test-results-dashboard. Rather than repeat the instructions
here, it is no harder to actually deploy the other project. So do that now and the dependencies will
be satisfied.

Deploy:
- https://github.com/Qarj/test-results-dashboard

### Clone webinject-server

Create a folder for webinject-server and clone the project:
```
cd /var/www
sudo mkdir wis
sudo chmod 777 wis
cd wis
sudo git clone https://github.com/Qarj/webinject-server
```

Set permissions so the Apache user can access the file system:
```
cd /var/www
sudo find . -type d -exec chmod a+rwx {} \;
sudo find . -type f -exec chmod a+rw {} \;
sudo find . -type f -iname "*.py" -exec chmod +x {} \;
```

Restart Apache:
```
sudo systemctl restart apache2
```

Verify with url: http://localhost/webinject/server/canary/

### Debugging

```
sudo cat /etc/apache2/envvars
sudo cat /var/log/apache2/error.log
```

Optional - deactivate the virtual environment from your shell:
```
deactivate
```

## WebInject Server home page

http://localhost/webinject/server/

## Run the Unit Tests

From folder `webinject-server/webinject`:
```
python manage.py test server
```

## Run the development server

From folder `webinject-server/webinject`:
```
python manage.py runserver
```

