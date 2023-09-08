from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import bcrypt

Base = declarative_base()

from Database import Base 

Base = declarative_base()

class UserProgress(Base):
    __tablename__ = 'user_progress'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id'), nullable=False)
    exercise_id = Column(Integer, ForeignKey('exercises.exercise_id'))
    quiz_id = Column(Integer, ForeignKey('quizzes.quiz_id'))
    completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress")
    exercise = relationship("Exercise", back_populates="progress")
    quiz = relationship("Quiz", back_populates="progress")

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String) 

    DATABASE_URL = "sqlite:///./Math_database.db"
    engine = create_engine(DATABASE_URL)

    # the relationship to UserProgress, UserAchievements, and UserRewards
    progress = relationship("UserProgress", back_populates="user")
    achievements = relationship("UserAchievements", back_populates="user")
    rewards = relationship("UserRewards", back_populates="user")

    def __init__(self, username, email, password, progress=None):
        self.username = username
        self.email = email
        self.set_password(password)  # Hash and set the password
        self.progress = progress

    def set_password(self, password):
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.password_hash = password_hash

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class Lesson(Base):
    __tablename__ = 'lessons'

    lesson_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    content = Column(String) 
    module_id = Column(Integer, ForeignKey('modules.module_id'))

    exercises = relationship("Exercise", back_populates="lesson")
    quizzes = relationship("Quiz", back_populates="lesson")

class UserAchievements(Base):
    __tablename__ = 'user_achievements'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    achievement_id = Column(Integer, ForeignKey('achievements.achievement_id'), nullable=False)

    #relationships to User and Achievement
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="users")

class UserRewards(Base):
    __tablename__ = 'user_rewards'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    reward_id = Column(Integer, ForeignKey('rewards.reward_id'), nullable=False)

    # relationships to User and Reward
    user = relationship("User", back_populates="rewards")
    reward = relationship("Reward", back_populates="users")

class Exercise(Base):
    __tablename__ = 'exercises'

    exercise_id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String)
    answer_options = Column(JSON)
    correct_answers = Column(JSON)
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id'))

    lesson = relationship("Lesson", back_populates="exercises")  #

class Quiz(Base):
    __tablename__ = 'quizzes'

    quiz_id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id'))
    questions = Column(JSON)

    score_to_pass = Column(Integer)

class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)

class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

class Module(Base):
    __tablename__ = 'modules'

    module_id = Column(Integer, primary_key=True, index=True)

if __name__ == "__main__":
    DATABASE_URL = "sqlite:///./Math_database.db"
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)

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

            # Debugging statements
            print(f"Username: {username}")
            print(f"Email: {email}")
            print(f"Password: {password}")

            with Session(engine) as session:
                user = User(username=username, email=email, password=password, progress=None)
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
                        print(f"Title: {lesson.title}")
                        print(f"Description: {lesson.description}")
                        print(f"Content: {lesson.content}")
                        print("----------")

        elif choice == "4":
            break
