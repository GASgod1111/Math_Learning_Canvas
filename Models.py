from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import bcrypt

DATABASE_URL = "sqlite:///./Math_database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserProgress(Base):
    __tablename__ = 'user_progress'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lessons.lid'), nullable=False)
    exercise_id = Column(Integer, ForeignKey('exercises.exercise_id'))
    quiz_id = Column(Integer, ForeignKey('quizzes.quiz_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
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
    achievements = relationship("UserAchievements", back_populates="user")
    rewards = relationship("UserRewards", back_populates="user")
    progress = relationship("UserProgress", back_populates="user")

    def __init__(self, username, email, password, progress=None):
        self.username = username
        self.email = email
        self.set_password(password)
        self.progress = progress or []  # Set default empty list if progress is None


    def set_password(self, password):
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.password_hash = password_hash

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class Lesson(Base):
    __tablename__ = 'lessons'
    lid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(String, index=True)
    description = Column(String)
    content = Column(String)
    module_id = Column(Integer, ForeignKey('modules.module_id'))
    exercises = relationship("Exercise", back_populates="lesson")
    quizzes = relationship("Quiz", back_populates="lesson")
    progress = relationship("UserProgress", back_populates="lesson")

    def __init__(self, title, description, content):
        self.title = title
        self.description = description
        self.content = content

class UserAchievements(Base):
    __tablename__ = 'user_achievements'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    achievement_id = Column(Integer, ForeignKey('achievements.achievement_id'), nullable=False)
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="users")

class UserRewards(Base):
    __tablename__ = 'user_rewards'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    reward_id = Column(Integer, ForeignKey('rewards.reward_id'), nullable=False)
    user = relationship("User", back_populates="rewards")
    reward = relationship("Reward", back_populates="users")

class Achievement(Base):
    __tablename__ = 'achievements'
    achievement_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    users = relationship("UserAchievements", back_populates="achievement")

class Reward(Base):
    __tablename__ = 'rewards'
    reward_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    users = relationship("UserRewards", back_populates="reward")

class Exercise(Base):
    __tablename__ = 'exercises'
    exercise_id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String)
    answer_options = Column(JSON)
    correct_answers = Column(JSON)
    lesson_id = Column(Integer, ForeignKey('lessons.lid'))
    lesson = relationship("Lesson", back_populates="exercises")
    progress = relationship("UserProgress", back_populates="exercise")

class Quiz(Base):
    __tablename__ = 'quizzes'
    quiz_id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lessons.lid'))
    questions = Column(JSON)
    score_to_pass = Column(Integer)
    progress = relationship("UserProgress", back_populates="quiz")
    lesson = relationship("Lesson", back_populates="quizzes")

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