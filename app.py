from flask import Flask
from dotenv import load_dotenv
import os
from extensions import db
from flask_login import LoginManager
from models import User

# Load environment variables from .env file
load_dotenv()

# Initialize the app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///blog.db')

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    from routes import main
    app.register_blueprint(main)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

