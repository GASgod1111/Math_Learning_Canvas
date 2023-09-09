# import sys
# import os

# # Add the project directory to sys.path
# project_dir = os.path.abspath(os.path.dirname(__file__))
# sys.path.append(project_dir)

# # Now you can import your modules
# from lib.Models import User, Lesson, Base
# from Database import SessionLocal, init_db

# if __name__ == "__main__":
#     # Initialize the database
#     init_db()

#     while True:
#         print("\nChoose an option:")
#         print("1. Add User")
#         print("2. Add Lesson")
#         print("3. List Lessons")
#         print("4. Exit")
#         choice = input("Enter your choice: ")

#         if choice == "1":
#             username = input("Enter username: ")
#             email = input("Enter email: ")
#             password = input("Enter password: ")

#             with SessionLocal() as session:
#                 user = User(username=username, email=email, password=password)
#                 session.add(user)
#                 session.commit()
#                 print("User added successfully!")

#         elif choice == "2":
#             title = input("Enter lesson title: ")
#             description = input("Enter lesson description: ")
#             content = input("Enter lesson content: ")

#             with SessionLocal() as session:
#                 lesson = Lesson(title=title, description=description, content=content)
#                 session.add(lesson)
#                 session.commit()
#                 print("Lesson added successfully!")

#         elif choice == "3":
#             with SessionLocal() as session:
#                 lessons = session.query(Lesson).all()
#                 if not lessons:
#                     print("No lessons found.")
#                 else:
#                     print("List of Lessons:")
#                     for lesson in lessons:
#                         print(f"Title: {lesson.title}")
#                         print(f"Description: {lesson.description}")
#                         print(f"Content: {lesson.content}")
#                         print("----------")

#         elif choice == "4":
#             break
