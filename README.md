# Teacher Direcory
This directory app containing teachers details. The data can be fetched with both django-rest API and Template View. 

# Dependencies 
The project requirements can be installed 

    pip install requirements.txt
    
# Quick Start

 - Run Migrations
 
        python manage.py migrate
        
 - Run project

        python manage.py runserver
        
 - Create superuser
 
        pyhon manage.py createsuperuser
        
 # App Details
 
 - After creating a superuser login to the admi page to view the models and data, "http://localhost:8000/admin/".
 
    # Django template view
    
    - Open http://localhost:8000/teachers/ to see the list of teachers
    - Options for Teacher profile and bulk import are include the same template page
    - Users can be login using username and password (create via admin page) and logout already login users.
    
    # Django Rest API
    
    - http://localhost:8000/teachers-rest/ URL can be used for list and GET teacher data. 
    
          http://localhost:8000/teachers-rest/<id> for all details of particular teacher
          
    - "last_name" (starting letter) or "subject" can be passed as query parameter for filtering values
    
          eg: http://localhost:8000/teachers-rest/?last_name=A&subject=Chemistry
    - For the import file to create new teachers http://localhost:8000/teachers-rest/bulk_import_teachers/ 
    
         - Pass Token in headers as Authorization = Token xxxxxxx. (Only Authenticated users can upload file and do bulk import)
     
    - To create new token make a POST request to  http://localhost:8000/api-token-auth/ with username and password.
