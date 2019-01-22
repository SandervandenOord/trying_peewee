# with peewee it is custom to import all methods with import *
from peewee import *

# peewee can create a sqlite database by itself.
# This only works for sqlite, not for Postgres or MySQL
db = SqliteDatabase('students.db')

students = {
    'sander': 20,
    'bob': 45,
    'claire': 23,
    'wizard': 60,
}


# models have singular names: Student, not Students
class Student(Model):
    username = CharField(max_length=255, unique=True)
    points = IntegerField(default=0)

    # in Meta you can define the database to connect to
    # but also the order of records etc. just like in Django
    class Meta:
        database = db


def add_students_to_table(students):
    """Add list of students to table"""
    for student_name, points in students.items():
        try:
            Student.create(username=student_name, points=points)
        except IntegrityError:  # IntError occurs when username already exists
            student_record = Student.get(username=student_name)
            if student_record.points != points:
                student_record.points = points
                student_record.save()


if __name__ == '__main__':
    db.connect()
    # safe=True is there to prevent app to break if db and
    # tables have already been created.
    db.create_tables([Student], safe=True)

    add_students_to_table(students)
