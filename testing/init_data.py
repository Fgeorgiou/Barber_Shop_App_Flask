from app.models import User
from app import db
admin = User(first_name="admin",last_name="test",email="admin@lakosta.com",password="Admin123",role_id=2,is_admin=True)
db.session.add(admin)
db.session.commit()
