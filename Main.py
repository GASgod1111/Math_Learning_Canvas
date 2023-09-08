from sqlalchemy import create_engine
from sqlalchemy.orm import Session 
from lib.Models import User, Lesson 
from Database import init_db

if __name__ == "__main__":
    DATABASE_URL = "sqlite:///./Math_database.db"
    engine = create_engine(DATABASE_URL)
    init_db(engine)

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

            with Session(engine) as session:
                user = User(username=username, email=email, password=password)
                session.add(user)
                session.commit()
                print("User added successfully!")

        elif choice == "2":
            title = input("Enter lesson title: ")
            description = input("Enter lesson description: ")
            content = input("Enter lesson content: ")

            with Session(engine) as session:
                lesson = Lesson(title=title, description=description, content=content)
                session.add(lesson)
                session.commit()
                print("Lesson added successfully!")

        elif choice == "3":
            with Session(engine) as session:
                lessons = session.query(Lesson).all()
                if not lessons:
                    print("No lessons found.")
                else:
                    print("List of Lessons:")
                    for lesson in lessons:
                        print(f"Lesson ID: {lesson.lesson_id}")
                        print(f"Title: {lesson.title}")
                        print(f"Description: {lesson.description}")
                        print(f"Content: {lesson.content}")
                        print("----------")

        elif choice == "4":
            break
