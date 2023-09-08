from sqlalchemy.orm import sessionmaker
from Database import Base, engine

# Create the database tables
Base.metadata.create_all(bind=engine)

# Close the database engine
engine.dispose()
