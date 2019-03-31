# Task Manager
'Task Manager' is a web application made using Django.<br />
### **Features**
* An authenticated user can create a team with registered users.
* A user in a team can create and define task with titile,description and status.
    * Task creator can assign the task to multiple users. 
    * Task creator can assign the task to himself.
* Only the task creator can edit or delete the task
* Any user in a team can view and comment on the tasks created in that team.
* Authenticated userrs can search for their tasks and teams using a search box
* New users can signup and registered users can login and logout of the webapp.

### **Run**
intitialize the database with:-<br />
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```
Create an admin:-<br />
```
$ python3 manage.py createsuperuser
```
Run the webapp in development mode:-<br />
```
$ python3 manage.py runserver
```
Access the webapp by typing the url http://127.0.0.1:8000/ in a browser.
