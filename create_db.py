from app import db, create_app
import os

app = create_app()

db_location = 'dev.db'
add_db = not os.path.exists(db_location)

if add_db:
    with app.app_context():
        db.create_all()
        print("Database created successfully.")
else:
    print("Database already exists.")