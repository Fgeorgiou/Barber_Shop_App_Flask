from app.models import *
from app import db
admin = User(first_name="admin",last_name="test",email="admin@lakosta.com",password="Admin123",role_id=3,is_admin=True)
db.session.add(admin)
db.session.commit()