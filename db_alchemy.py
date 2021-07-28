from sqlalchemy import Column, ForeignKey, Integer, String, MetaData, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random

Base = declarative_base()
engine = create_engine('sqlite:///SchoolScheduler.db')

# drop and recreate all tables
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class Student(Base):
    __tablename__ = 'Student'
    id = Column(Integer, primary_key=True)
    first = Column(String(250), nullable=False)
    last = Column(String(250), nullable=False)
    gpa = Column(Integer, nullable=False)

    @staticmethod
    def get_all():
        query = session.query(Student)
        return session.execute(query).scalars().all()

    @staticmethod
    def by_id(id):
        query = session.query(Student).where(Student.id == id)
        return session.execute(query).scalar()

    @staticmethod
    def insert(id, first, last, gpa):
        session.add(Student(id=id, first=first, last=last, gpa=gpa))

    @staticmethod
    def delete(id):
        session.delete(Student).where(Student.id == id)
        session.commit()

    @staticmethod
    def available(student_id, period):
        num_in_period = \
            session.execute(session.query(func.count(Schedule.id)).where(Schedule.student_id == student_id).where(
                Schedule.period == period)).scalar()
        if num_in_period == 0:
            return True
        return False


class Class(Base):
    __tablename__ = 'Class'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('Course.id'))
    period = Column(Integer, nullable=False)

    @staticmethod
    def get_all():
        query = session.query(Class)
        return session.execute(query).all()

    @staticmethod
    def by_id(id):
        query = session.query(Class).where(Class.id == id)
        return session.execute(query).scalar()

    @staticmethod
    def get_name(id):
        query = session.query(Course).where(Class.id == Class.by_id(id).course_id)
        return session.execute(query).scalar().name

    @staticmethod
    def insert(id, course_id, period):
        session.add(Class(id=id, course_id=course_id, period=period))
        session.commit()


class Course(Base):
    __tablename__ = 'Course'
    id = id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    type = Column(String(250), nullable=False)
    capacity = Column(Integer, nullable=False)

    @staticmethod
    def get_all():
        query = session.query(Course)
        return session.execute(query).all()

    @staticmethod
    def by_id(id):
        query = session.query(Course).where(Course.id == id)
        return session.execute(query).scalar()

    @staticmethod
    def insert(id, name, type, capacity):
        session.add(Course(id=id, name=name, type=type, capacity=capacity))
        session.commit()

    @staticmethod
    def available(id, period, student_id):
        classes = session.execute(
            session.query(Class).where(Class.id == id).where(Class.period == period)).scalars().all()
        for c in classes:
            count = session.execute(session.query(func.count(Schedule.id)).where(Schedule.class_id == c.id).where(
                Schedule.period == period)).scalar()
            if count < 15:
                return c.id
        return -1


class Schedule(Base):
    __tablename__ = "Schedule"

    id = id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('Student.id'))
    class_id = Column(Integer, ForeignKey('Class.id'))
    period = Column(Integer, nullable=False)

    @staticmethod
    def get_all():
        query = session.query(Schedule)
        return session.execute(query).all()

    @staticmethod
    def insert(student_id, class_id, period):
        session.add(Schedule(student_id=student_id, class_id=class_id, period=period))
        session.commit()

    @staticmethod
    def by_student_id(student):
        query = session.query(Schedule).where(Schedule.student_id == student_id)
        return session.execute(query).scalar()


class Preference(Base):
    __tablename__ = "Preference"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('Course.id'))
    student_id = Column(Integer, ForeignKey('Student.id'))
    period = Column(Integer, nullable=False)

    @staticmethod
    def get_all():
        query = session.query(Preference)
        return session.execute(query).scalars().all()

    @staticmethod
    def insert(course_id, student_id, period):
        session.add(Preference(course_id=course_id, student_id=student_id, period=period))

    @staticmethod
    def by_student_id(student_id):
        query = session.query(Preference).where(Preference.student_id == student_id)
        return session.execute(query).scalars().all()

    @staticmethod
    def by_period(period):
        query = session.query(Preference).where(Preference.period == period)
        return session.execute(query).all()


class Class_History(Base):
    __tablename__ = "Class_History"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('Student.id'))
    class_name = Column(String(250), nullable=False)
    credit = Column(Integer, nullable=False)
    grade = Column(String(250), nullable=False)

    @staticmethod
    def insert(student_id, class_name, credit, grade):
        session.add(Class_History(student_id=student_id, class_name=class_name, credit=credit, grade=grade))

    @staticmethod
    def by_student_id(student_id):
        query = session.query(Class_History).where(Class_History.student_id == student_id)
        return session.execute(query).scalars().all()


def db_init():
    Base.metadata.create_all(engine)


def db_purge():
    Base.metadata.drop_all(engine)


# db_purge()
# db_init()
#
# scheduled_class = Schedule(student_id=1, class_id=1, period=1)
# session.add(scheduled_class)
# session.add(Student(id=2, first="Test",last="Name",gpa=3.0))
# session.commit()

# Class.insert(1, 1, 2)
# Course.insert(1,"test", "test", 20)
# print(Class.by_id(1).period)
# Course.available(1,2,3)
#
# classes = session.query(Class).all()
# students = session.query(Student).all()
# schedules = session.query(Schedule).all()
#
# print(schedules[0].student_id)
#
# s = Student.by_id(2)
# print(s.first)
# s.first = "aaaa"
# print(Student.by_id(2).first)
#
# for student in students:
#     print(str(student.id) + " " + student.first)
#
# for scheduled_class in classes:
#     print(scheduled_class.id)
#     print(Class.get_name(scheduled_class.id))

def insert_test_students():
    # (id, first, last, GPA)
    words = open('words.txt', 'r')
    lines = words.read().splitlines()

    for x in range(1000):
        Student.insert(x, lines[random.randint(0, 10000)], lines[random.randint(0, 10000)], 4)
    session.commit()


def insert_test_courses():
    # (name, type)

    # Class ID are generated in order check the UI for easy sorting and dispaly
    courses = [['Algebra 1', 'MATH'],
               ['Algebra 2', 'MATH'],
               ['Geometry', 'MATH'],
               ['ADV MATH 1', 'MATH'],
               ['ADV MATH 2', 'MATH'],
               ['ELA 1', 'ELA'],
               ['ELA 2', 'ELA'],
               ['ELA 3', 'ELA'],
               ['ELA 4', 'ELA'],
               ['Biology 1', 'SCIENCE'],
               ['Science Class 1', 'SCIENCE'],
               ['Science Class 2', 'SCIENCE'],
               ['World History', 'SOCIAL'],
               ['U.S. History', 'SOCIAL'],
               ['U.S. Government', 'SOCIAL'],
               ['Economics', 'SOCIAL'],
               ['Physical Education', 'HEALTH'],
               ['Elective 1', 'ELECTIVE'],
               ['Elective 2', 'ELECTIVE'],
               ['Elective 3', 'ELECTIVE'],
               ['Elective 4', 'ELECTIVE'],
               ['Elective 5', 'ELECTIVE'],
               ['Elective 6', 'ELECTIVE'],
               ['Elective 7', 'ELECTIVE'],
               ['Elective 8', 'ELECTIVE'],
               ['ART 1', 'FINEART'],
               ['ART 2', 'FINEART'],
               ['ART 3', 'FINEART'],
               ['Study Hall', 'FREE']
               ]
    x = 0
    for c in courses:
        Course.insert(x, c[0], c[1], 15)
        x += 1


def insert_test_preferences():
    # Assume 1000 students with decreasing number count thru 9 to 12th greade
    # Note that Preference period is almost meaningless and is simply here for indexing in UI
    # insert(course_id, student_id, period):
    for x in range(0, 349):
        # ELA 9th grade everyone takes
        Preference.insert(5, x, 1)

        # Math
        r = random.random()
        if (r < 0.9):
            Preference.insert(0, x, 2)
        else:
            Preference.insert(2, x, 2)

        # Science all 9th graders take bio
        Preference.insert(9, x, 3)

        # Social
        r = random.random()
        if (r < 0.95):
            Preference.insert(12, x, 4)
        else:
            Preference.insert(13, x, 4)

        # Elective
        r = random.randint(17, 24)
        Preference.insert(r, x, 5)

        # P.E
        Preference.insert(16, x, 6)

        # Study Hall
        Preference.insert(28, x, 7)

    for x in range(350, 649):
        # ELA 10th grade everyone takes around 2% fail and must retake
        r = random.random()
        if (r < 0.98):
            Preference.insert(6, x, 1)
        else:
            Preference.insert(5, x, 1)

        # Math
        r = random.random()
        if (r < 0.9):
            Preference.insert(2, x, 2)
        elif (r < 0.98):
            Preference.insert(1, x, 2)
        else:
            Preference.insert(0, x, 2)

        # Science
        r = random.randint(10, 11)
        Preference.insert(r, x, 3)

        # Social
        r = random.random()
        if r < 0.95:
            Preference.insert(13, x, 4)
        else:
            Preference.insert(14, x, 4)

        # Elective
        r = random.randint(17, 20)
        Preference.insert(r, x, 5)

        r = random.randint(21, 27)
        Preference.insert(r, x, 6)

        # Study Hall
        Preference.insert(28, x, 7)

    for x in range(650, 900):
        # ELA 11th grade everyone takes around 2% fail and must retake
        r = random.random()
        if r < 0.98:
            Preference.insert(7, x, 1)
        else:
            Preference.insert(6, x, 1)

        # Math
        r = random.random()
        if r < 0.95:
            Preference.insert(1, x, 2)
        else:
            r = random.randint(3, 4)
            Preference.insert(r, x, 2)

        # Science
        r = random.randint(10, 11)
        Preference.insert(r, x, 3)

        # Social
        r = random.random()
        if r < 0.95:
            Preference.insert(14, x, 4)
        else:
            Preference.insert(15, x, 4)

        # Elective
        r = random.randint(17, 20)
        Preference.insert(r, x, 5)

        r = random.randint(21, 27)
        Preference.insert(r, x, 6)

        # Study Hall
        Preference.insert(28, x, 7)

    for x in range(900, 1000):
        # ELA 12th grade everyone takes around 2% fail and must retake
        r = random.random()
        if r < 0.98:
            Preference.insert(8, x, 1)
        else:
            Preference.insert(7, x, 1)

        # Math
        r = random.randint(3, 4)
        Preference.insert(r, x, 2)

        # Social
        r = random.random()
        if r < 0.98:
            Preference.insert(15, x, 3)
        else:
            Preference.insert(28, x, 3)

        # Study Hall
        Preference.insert(28, x, 4)

        # Elective
        r = random.randint(17, 20)
        Preference.insert(r, x, 5)

        r = random.randint(21, 27)
        Preference.insert(r, x, 6)

        # Study Hall
        Preference.insert(28, x, 7)
    session.commit()


def insert_test_coursework():
    # student_id, name, credit, grade
    courses = [['Algebra 1', 'MATH'],
               ['Algebra 2', 'MATH'],
               ['Geometry', 'MATH'],
               ['ADV MATH 1', 'MATH'],
               ['ADV MATH 2', 'MATH'],
               ['ELA 1', 'ELA'],
               ['ELA 2', 'ELA'],
               ['ELA 3', 'ELA'],
               ['ELA 4', 'ELA'],
               ['Biology 1', 'SCIENCE'],
               ['Science Class 1', 'SCIENCE'],
               ['Science Class 2', 'SCIENCE'],
               ['World History', 'SOCIAL'],
               ['U.S. History', 'SOCIAL'],
               ['U.S. Government', 'SOCIAL'],
               ['Economics', 'SOCIAL'],
               ['Physical Education', 'HEALTH'],
               ['Elective 1', 'ELECTIVE'],
               ['Elective 2', 'ELECTIVE'],
               ['Elective 3', 'ELECTIVE'],
               ['Elective 4', 'ELECTIVE'],
               ['Elective 5', 'ELECTIVE'],
               ['Elective 6', 'ELECTIVE'],
               ['Elective 7', 'ELECTIVE'],
               ['Elective 8', 'ELECTIVE'],
               ['ART 1', 'FINEART'],
               ['ART 2', 'FINEART'],
               ['ART 3', 'FINEART'],
               ['Study Hall', 'FREE']
               ]

    for x in range(350, 1000):
        Class_History.insert(x, courses[5][0], 3, get_grade())
        r = random.random()
        if (r < 0.9):
            Class_History.insert(x, courses[0][0], 3, get_grade())
        else:
            Class_History.insert(x, courses[2][0], 3, get_grade())

        Class_History.insert(x, courses[9][0], 3, get_grade())

        r = random.random()
        if (r < 0.95):
            Class_History.insert(x, courses[12][0], 3, get_grade())
        else:
            Class_History.insert(x, courses[13][0], 3, get_grade())

        r = random.randint(17, 24)
        Class_History.insert(x, courses[r][0], 1, get_grade())

        Class_History.insert(x, courses[16][0], 3, get_grade())

        Class_History.insert(x, courses[28][0], 1, get_grade())

        if x in range(650, 900):
            failed = classes_failed(x)
            classes = Class_History.by_student_id(x)

            if "ELA 1" in failed:
                Class_History.insert(x, courses[5][0], 3, get_grade())
            else:
                Class_History.insert(x, courses[6][0], 3, get_grade())

            # Math
            r = random.random()
            if "Algebra 1" in failed:
                Class_History.insert(x, courses[0][0], 3, get_grade())
            elif "Geometry" in failed:
                Class_History.insert(x, courses[2][0], 3, get_grade())
            else:
                if [y for y in classes if y.class_name == "Algebra 1"]:
                    if r < 0.9:
                        Class_History.insert(x, courses[2][0], 3, get_grade())
                    else:
                        Class_History.insert(x, courses[1][0], 3, get_grade())
                elif [y for y in classes if y.class_name == "Geometry"]:
                    Class_History.insert(x, courses[0][0], 3, get_grade())

            # Science
            if "Biology 1" in failed:
                Class_History.insert(x, courses[9][0], 3, get_grade())
            else:
                r = random.randint(10, 11)
                Class_History.insert(x, courses[r][0], 3, get_grade())

            # Social
            if "World History" in failed:
                Class_History.insert(x, courses[12][0], 3, get_grade())
            elif "U.S. History" in failed:
                Class_History.insert(x, courses[13][0], 3, get_grade())
            else:
                if [y for y in classes if y.class_name == "World History"]:
                    r = random.random()
                    if r < 0.95:
                        Class_History.insert(x, courses[13][0], 3, get_grade())
                    else:
                        Class_History.insert(x, courses[14][0], 3, get_grade())
                else:
                    Class_History.insert(x, courses[14][0], 3, get_grade())

            # Elective
            r = random.randint(17, 20)
            Class_History.insert(x, courses[r][0], 3, get_grade())

            r = random.randint(21, 27)
            Class_History.insert(x, courses[r][0], 3, get_grade())

            # Study Hall
            Class_History.insert(x, courses[28][0], 3, get_grade())

        elif x in range(900, 1000):
            failed = classes_failed(x)
            classes = Class_History.by_student_id(x)

            if "ELA 2" in failed:
                Class_History.insert(x, courses[6][0], 3, get_grade())
            else:
                Class_History.insert(x, courses[7][0], 3, get_grade())

            # Math
            if "Algebra 2" in failed or [y for y in classes if y.class_name != "Algebra 2"]:
                Class_History.insert(x, courses[1][0], 3, get_grade())
            else:
                r = random.randint(3, 4)
                Class_History.insert(x, courses[r][0], 3, get_grade())

            # Science
            if "Biology 1" in failed:
                Class_History.insert(x, courses[9][0], 3, get_grade())
            elif "Science Class 1" in failed:
                Class_History.insert(x, courses[10][0], 3, get_grade())
            elif "Science Class 2" in failed:
                Class_History.insert(x, courses[11][0], 3, get_grade())
            else:
                if [y for y in classes if y.class_name == "Science Class 1"]:
                    Class_History.insert(x, courses[11][0], 3, get_grade())
                else:
                    Class_History.insert(x, courses[10][0], 3, get_grade())

            # Social
            if "U.S. History" in failed:
                Class_History.insert(x, courses[13][0], 3, get_grade())
            elif "U.S. Government" in failed:
                Class_History.insert(x, courses[14][0], 3, get_grade())
            else:
                if [y for y in classes if y.class_name == "U.S. Government"]:
                    Class_History.insert(x, courses[15][0], 3, get_grade())
                else:
                    Class_History.insert(x, courses[14][0], 3, get_grade())

            # Elective
            r = random.randint(17, 20)
            Class_History.insert(x, courses[r][0], 3, get_grade())

            r = random.randint(21, 27)
            Class_History.insert(x, courses[r][0], 3, get_grade())

            # Study Hall
            Class_History.insert(x, courses[28][0], 3, get_grade())
    session.commit()


def get_grade():
    r = random.random()
    if r <= 0.6:
        return "A"
    elif r <= 0.8:
        return "B"
    elif r <= 0.925:
        return "C"
    elif r <= .98:
        return "D"
    else:
        return "F"


def classes_failed(student_id):
    failed = []
    for c in Class_History.by_student_id(student_id)[:-7]:
        if c.grade == "F":
            failed.append(c.class_name)
    return failed
