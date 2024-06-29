from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a database engine
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')

# Create a session factory
Session = sessionmaker(bind=engine)

# Define a database model
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    private_key = Column(String)

# Create the database table
Base.metadata.create_all(engine)

# Insert a new user
session = Session()
new_user = User(name='John Doe', private_key='john@example.com')
session.add(new_user)
session.commit()

# Query the database
users = session.query(User).all()
for user in users:
    print(f'{user.name} - {user.private_key}')
