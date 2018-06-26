# webinject-server 0.1.0

WebInject Server is a project for running WebInject over http.

Run an existing script via a GET. Example: http://localhost/webinject/server/run/?path=examples*test.xml

Or submit a test script to run using POST.

The main WebInject project is here: http://qarj.github.io/WebInject

## Deploy on Windows

Check Python version - minimum version required is 3.6.
The 32 bit version is the default at python.org and is recommended.
```
python --version
```

Clone the project:
```
cd /d C:\
mkdir git
cd git
git clone https://github.com/Qarj/webinject-server.git
cd webinject-server
```

Install Django:
```
pip install Django
```

Initialise the project:
```
cd webinject
python manage.py migrate
```
### Install Apache

Apache and Python must be both 32 bit or 64 bit. 32 bit is recommended for Windows.

From Apache Lounge https://www.apachelounge.com/download/ download Win32 zip file - not 64 bit, then extract so C:\Apache24\bin folder is available.

From Admin terminal, `cd C:\Apache24\bin` then `httpd -k install` followed by `httpd -k start` (port 80 will need to be free for this to work)

### Install mod_wsgi-express

- Follow instructions exactly, and do not mix 32 and 64 bit!
- Microsoft Visual C++ 14.0 build toosl are required, you install them from the Visual Studio 2017 Build Tools
    - http://landinghub.visualstudio.com/visual-cpp-build-tools - choose install "Visual Studio Build Tools 2017"
    - Run the installer, click `Visual C++ build tools` (top left option) then the checkboxs for `C++/CLI support` and `VC++ 2015.3 v14.00 (v140) toolset for desktop` on the right hand side
    - You might need to reboot
- Ensure you have Python 3.6.5 32-bit version installed (default from Python.org)
- Press Windows Key, type `VS2015` right click `VS2015 x86 Native Tools Command` then select `Run as administrator`
    - Note: On my Windows 7 machine I had to select `Developer Command Prompt for VS 2017 (2)`

Now it will be possible to compile mod_wsgi on Windows:
```
pip install mod_wsgi
```

Check that it works!:
```
mod_wsgi-express module-config
```

The output will look something like this:
```
LoadFile "c:/python36/python36.dll"
LoadModule wsgi_module "c:/python36/lib/site-packages/mod_wsgi/server/mod_wsgi.cp36-win32.pyd"
WSGIPythonHome "c:/python36"
```

### Configure Apache to point to webinject-server

Activate `httpd-vhosts.conf`
```
notepad C:\Apache24\conf\httpd.conf
```
then uncomment `Include conf/extra/httpd-vhosts.conf`

Backup `httpd-vhosts.conf` then overwrite it with the mod_wsgi Apache settings
```
copy C:\Apache24\conf\extra\httpd-vhosts.conf C:\Apache24\conf\extra\httpd-vhosts_backup.conf
mod_wsgi-express module-config > C:\Apache24\conf\extra\httpd-vhosts.conf
```

Now append config required for WebInject Server
```
type C:\git\webinject-server\webinject\httpd-vhosts_windows.conf >> C:\Apache24\conf\extra\httpd-vhosts.conf
```

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

### Note 

These instructions assume that you are not already using Apache. If you are then you'll
need to manually merge in the previous config.

To merge the WSGIPythonPath you put a semicolon between the paths (or a colon for Linux).

```
WSGIPythonPath c:/git/test-results-dashboard/dash;c:/git/webinject-server/webinject
```

## Deploy on Linux

Deploy these projects to the recommended location:
* https://github.com/Qarj/WebInject
* https://github.com/Qarj/WebInject-Framework

Optionally deploy if you want to use Selenium too:
* https://github.com/Qarj/WebInject-Selenium

Check Python version - minimum version required is 3.6.
```
python --version
```
### Apache, Django and mod_wsgi installation

**_Skip this section if you have installed the test-results-dashboard project._**

Install required system packages as root:
```
sudo apt update
sudo apt-get install python3-pip
sudo apt-get install python3-venv
sudo apt install gnome-terminal
sudo apt install apache2
sudo apt install apache2-dev
```

Now create a Python 3 virtual environment and activate it:
```
cd /usr/local
sudo mkdir venvs
sudo chmod 777 venvs
cd venvs
python3 -m venv dash
cd dash
source bin/activate
```

Now that the virtual environment is active, any `python` and `pip` commands will
refer to Python 3, and not Python 2. Prove this:
```
python --version
```

Install the necessary packages for test-results-dashboard as a normal user, not as root:
```
pip install Django
pip install mod_wsgi
```
If you are plagued by SSL errors, then you need to build Python 3 manually to sort it out.
Check here for how to do this: https://github.com/Qarj/linux-survival/blob/master/BuildPython3.md
When you've got Python 3 working with shared libraries, `cd /usr/local/venvs` then `rm -r dash` go
back to the `python3 -m venv dash` step and continue from there.

### Clone Project

Create a folder for webinject-server and clone this project:
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

### Setup mod_wsgi

**_Skip this section if you have installed the test-results-dashboard project._**

```
mod_wsgi-express module-config | sudo tee /etc/apache2/conf-enabled/wsgi.conf
sudo cp tools/all-qarj-projects-linux.conf /etc/apache2/sites-enabled/all-qarj-projects.conf
sudo rm /etc/apache2/sites-enabled/000-default.conf
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

From folder `C:\git\webinject-server\webinject`:
```
python manage.py test server
```

## Run the development server

From folder `C:\git\webinject-server\webinject`:
```
python manage.py runserver
```

