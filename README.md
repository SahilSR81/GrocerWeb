#To run this project on your local machine or github codespace
First download the zip and extract on local machine
If on github codespace then just clone this repo and then do this 

Go to the terminal then in the project directory first grocs file directory once inside then :
First type : pip install django

then type : pip install xhtml2pdf

then type : python manage.py migrate 
output : Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, superadmin, web
Running migrations:
  No migrations to apply.

Then type : python manage.py runserver
