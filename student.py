
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Student(Base):
    __tablename__ = 'Students'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    first = Column(String(250), nullable=False)
    last = Column(String(250), nullable=False)
    gpa = Column(Integer, nullable=False)

    def __init__(self, first, last, gpa):
        self.first = first
        self.last = last
        self.gpa = gpa


class Classes(Base):
    __tablename__ = 'Classes'
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)



class Schedule(Base):
    __tablename__ = "Schedule"

    id = Column(Integer, primary_key=True)
    session = Column(Integer, ForeignKey('Classes.id'))
    student = Column(Integer, ForeignKey('Students.id'))

engine = create_engine('sqlite:///SchoolScheduler.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#scheduled_class = Schedule(session=1, student=1)
#session.add(scheduled_class)
#session.commit()

classes = session.query(Classes).all()
students = session.query(Student).all()
schedule = session.query(Schedule).all()

print(schedule[0].student)

for student in students:
    print(student.first)

for scheduled_class in classes:
    print(scheduled_class.name)