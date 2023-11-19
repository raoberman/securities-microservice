# E6156 - Merry Men Trading App Securities Microservice

__Author:__ Rachel Oberman

## A combination of the first microservice project and example Docker project from the professor for sprint 1

### Setup

- In the terminal, type ```pip install -r requirements.txt``` This will install the necessary
Python packages.


- You will see an initialization (logging) messages followed by the message
```
 Uvicorn running on http://0.0.0.0:8012 (Press CTRL+C to quit)
```


### Execution

- Click on ```http://0.0.0.0:8012``` link to open in the browser. You can also copy and past the link.
You will see something of the form

| <img src="./browser-screen-1.png"> |
| :---: |
| __Simple Execution__ |


- Accessing the URL ```http://0.0.0.0:8012/docs``` will navigate to the [OpenAPI](https://www.openapis.org/)
page/documentation for the application.


### Modification

1. Create a new GitHub project and clone the project.<br><br>
2. Change the name of the author in ```README.md```<br><br>
2. Copy the code from this example into the directory for the project.<br><br>
3. Follow the steps for:
   1. Creating a virtual environment for your version of the project.
   2. ```pip``` installing ```requirements.txt```
   3. Executing and accessing the application.
4. In ```main.py,``` modify the line ```return {"message": f"Hello {name}"}``` to return
a message of the form ```return {"message": f"Awesome cloud developer dff9 says Hello {name}"}```
Replace my uni with yours.
5. Rerun the application to test.


### Publish


<hr>

__Note:__
- The default behavior for virtual environment creation is to
create the venv in the current folder/project.
- You can create the venv anywhere on the file system.
- You do not want to venv pushed to GitHub. So, if the venv is inside the
project, remove the directory from the set of files that will be pushed.
The easiest way is to add to a [.gitignore file.](https://git-scm.com/docs/gitignore)

<hr>

<br>





