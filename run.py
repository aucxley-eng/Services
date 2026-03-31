from app import create_app, db
from app.models import User, Product # Import models to ensure they are registered

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Creates tables based on models
    app.run(debug=True, port=5000)