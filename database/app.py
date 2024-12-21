from flask import Flask
from flask_session import Session
from utils import db, migrate


def create_app(config_class="config.Development"):
    """Create and configure app instance"""
    app = Flask(__name__)
    # Set configuration app
    app.config.from_object(config_class)
    # Initialize Database
    db.init_app(app)
    
    # Test connection only for MSSQL
    # Refactoring as command cli
    #with app.app_context():
    #   import sqlalchemy
    #   con = db.session.execute( sqlalchemy.text("SELECT SYSTEM_USER;"))
    #   for c in con:
    #       print(c)

    # Initialize Server-Side-Session
    Session(app)
    # Initialize Migrate
    migrate.init_app(app, db)
    from models import (Student, Teacher, Course, Inscription, Mark,
        Attendance, Charge, TeacherPayment, CourseExpense)
    
    # Execute seeders
    @app.cli.command("run_seeder")
    def run_seeder():
        from seeders import seed_tables
        seed_tables()
        return True

    return app

if __name__ == "__main__":
    app = create_app()
