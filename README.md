# webinject-server 0.1.0

WebInject Server is a project for running WebInject over http.

Run an existing script via a GET. Example: http://localhost/webinject/server/run/?path=examples%2Ftest.xml

Or submit a test script to run using POST.

This project is not yet ready for use, check back later!

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

From Admin terminal, `cd C:\Apache\bin` then `httpd -k install` followed by `httpd -k start` (port 80 will need to be free for this to work)

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
notepad C:\Apache24\conf\httpd.conf`
```
then uncomment `Include conf/extra/httpd-vhosts.conf`

Backup `httpd-vhosts.conf` then overwrite it with the mod_wsgi Apache settings
```
C:\Apache24\conf\extra\httpd-vhosts.conf C:\Apache24\conf\extra\httpd-vhosts_backup.conf
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

