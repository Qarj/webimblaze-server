# webinject-server 0.1.0

WebInject Server is a project for running WebInject over http.

The main WebInject project is here: http://qarj.github.io/WebInject

## Install on Windows

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

