from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models import User

DATABASE_URL = "sqlite:///./Math_database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from Models import Base
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    while True:
        print("\nChoose an option:")
        print("1. Add User")
        print("2. Add Lesson")
        print("3. List Lessons")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            username = input("Enter username: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            print(f"Username: {username}")
            print(f"Email: {email}")
            print(f"Password: {password}")
            with SessionLocal() as session:
                user = User(username=username, email=email, password=password)
                session.add(user)
                session.commit()
                print("User added successfully!")
       elif choice == "2":
            title = input("Enter lesson title: ")
            description = input("Enter lesson description: ")
            content = input("Enter lesson content: ")
            with SessionLocal() as session:
                lesson = Lesson(title=title, description=description, content=content)
                session.add(lesson)
                session.commit()
                print("Lesson added successfully!")
        elif choice == "3":
            with SessionLocal() as session:
                lessons = session.query(Lesson).all()
            for lesson in lessons:
                print(f"Title: {lesson.title}")
                print(f"Description: {lesson.description}")
        elif choice == "4":
            break