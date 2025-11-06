from getpass import getpass
import sys
from app.db.database import SessionLocal
from app.models.user import User, UserRole
from passlib.context import CryptContext

# Initialize password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def createsuperuser():
    db = next(get_db())
    
    print("Create a superuser (admin)")
    print("-" * 30)
    
    # Get user input
    try:
        first_name = input("First name: ").strip().title()
        last_name = input("Last name: ").strip().title()
        email = input("Email: ").strip().lower()
        username = input("Username: ").strip()
                
        # Hidden password input
        while True:
            password = getpass("Password: ")
            password2 = getpass("Confirm password: ")
            
            if password == password2:
                break
            print("Passwords don't match. Please try again.")
    
        # Check if username or email already exists
        if db.query(User).filter(User.username == username).first():
            print("Error: Username already exists")
            sys.exit(1)
            
        if db.query(User).filter(User.email == email).first():
            print("Error: Email already exists")
            sys.exit(1)
    
        # Create the superuser
        superuser = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            hashed_password=pwd_context.hash(password),
            role=UserRole.admin,
            is_active=True
        )
        
        db.add(superuser)
        db.commit()
        db.refresh(superuser)
        
        print("\nSuperuser created successfully!")
        print(f"Username: {username}")
        print(f"Role: {superuser.role}")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError creating superuser: {str(e)}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    createsuperuser()