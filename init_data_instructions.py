'''
This file contains instructions on how to initialize this website.
1. In the command prompt window, the set FLASK_APP variable must be set to the entry point file -> command = set FLASK_APP=run_app.py
2. Pip install the requirements.txt -> pip install -r /path/to/requirements.txt
3. Now that the libraries are loaded, in order to create a database, with migration files, the following commands myst be issued -> commands = 

-> flask db init
-> flask db migrate
-> flask db upgrade

This set of commands aim to initialize a db file, pass the data from the models file and then upgrade to the latest version.

4. Now to pass the init data. In the cmd window, use the command access the flask shell -> command = flask shell
5. In the flask shell, the following commands need to be typed to initialize an admin account. Of course the information
is the user's choice. Here, the defaults for the barber shop are being used. -> commands =

-> from app.models import *
-> from app import db
-> admin = User(first_name="Admin",last_name="Admin",email="admin@labarberia.com",password="Admin123",role_id=3,is_admin=True)
-> db.session.add(admin)
-> db.session.commit()

6. This step can be followed to insert as many users as needed. Also the query can be adapted to insert any piece of data the models provide.
Now, the admin must add the roles
-> from app.models import *
-> from app import db
-> role_1 = Role(role_title="Customer")
-> role_2 = Role(role_title="Barber")
-> role_3 = Role(role_title="S Admin")
-> db.session.add(role_1)
-> db.session.add(role_2)
-> db.session.add(role_3)
-> db.session.commit()
7. These are the commands for the default services follows -> commands =

-> from app.models import *
-> from app import db
-> service_1 = Service(name="Manly haircut",cost=8)
-> service_2 = Service(name="Kids haircut",cost=7)
-> service_3 = Service(name="Clean cut",cost=5)
-> service_4 = Service(name="Trimming(hair)",cost=6)
-> service_5 = Service(name="Trimming(beard)",cost=4)
-> service_6 = Service(name="Cleaning (neck, ears, nose)",cost=4)
-> service_7 = Service(name="Hair dye",cost=12)
-> service_8 = Service(name="Traditional shave",cost=8)
-> service_9 = Service(name="Trimming (hair) + shave",cost= 12)
-> service_10 = Service(name="Trimming (beard) + cleaning (neck, ears, nose)",cost=6)
-> db.session.add(service_1)
-> db.session.add(service_2)
-> db.session.add(service_3)
-> db.session.add(service_4)
-> db.session.add(service_5)
-> db.session.add(service_6)
-> db.session.add(service_7)
-> db.session.add(service_8)
-> db.session.add(service_9)
-> db.session.add(service_10)
-> db.session.commit()

'''

