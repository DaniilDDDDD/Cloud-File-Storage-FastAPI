# Cloud file storage

A file storage that allows you to share a file via a link with other people, customize file permissions, 
and display a list of the most downloaded files.

## Getting started
Fork project's [repository](https://github.com/DaniilDDDDD/Cloud-File-Storage-FastAPI.git).
Load it to your machine.
You must have python3 installed and create [virtual environment](https://docs.python.org/3/library/venv.html).
To install all required packages open command prompt, activate virtual environment, go to project's directory and write
```pip instal requirements.txt```. When all packages would be installed use command ```uvicorn main:app --reload```
 to run FastAPI server on 8000 port of your machine (for example ```localhost:8000```)

## Endpoints
All urls starts with domain name of your machine and port number on which you run the application.
For example ```http://localhost:8000``` or ```http://blablabla.bla:1234```.

## Documentation
You can see the documentation by deploying project and following the link ```/docs```