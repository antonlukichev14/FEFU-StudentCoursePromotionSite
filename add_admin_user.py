from run import create_app
from app.models import db, User

def add():
    app = create_app()

    with app.app_context():
        
        User.query.delete()

        admin_user = User(
            username = 'Alex',
            email = 'None',
            password = '123',
            role = 'admin'
        )

        db.session.add(admin_user)
        db.session.commit() 

        print(f"User {admin_user.username} with password hash {admin_user.password_hash} register!")

if __name__ == '__main__':
    add()