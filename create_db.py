from app import db, create_app
app = create_app()

with app.app_context():
    db.create_all()
    
if __name__ == "__main__":
    print("Database created successfully.")