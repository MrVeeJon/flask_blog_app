# Run this script once seperately before running the app
from extensions import db
from app import create_app

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("All tables have been created.")
