from db.models import Students, Teachers, Grades
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError


engine = create_engine('sqlite:///school.db')
Session = sessionmaker(bind=engine)

# ------------------ Admin Page --------------------- #


def admin_page():
    select = int(input(f'''
        Please select:

        1 - Add Teachers
        2 - View All Teachers

    ENTER: '''))

    # --------------- Add Teacher ------------------- #

    if select == 1:

        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        subject = input("Enter subject: ")
        add_teacher(first_name, last_name, subject)

    # ------------- View All Teachers --------------- #

    if select == 2:
        view_all_teachers()


# ----------------- Teacher Page --------------------- #


def teacher_page():
    select = int(input(f'''
        Please select:
        
        1 - Add Student
        2 - Add Grade
        3 - View Grades
        4 - Drop student

    ENTER: '''))

    # -------------- Add Student ------------- #

    if select == 1:

        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        add_student(first_name, last_name)

    # -------------- Add Grade --------------- #

    if select == 2:

        teacher_id = input("Enter teacher ID: ")
        student_id = input("Enter student ID: ")
        grade = input("Enter grade: ")
        add_grade(teacher_id, student_id, grade)

    # ----------- View Student Grades ----------#

    if select == 3:

        teacher_id = input("Enter teacher ID: ")
        view_all_grades(teacher_id)

    # ----------- Drop Student ----------------#

    if select == 4:

        student_id = input("Enter student ID: ")
        drop_student(student_id)

# ------------- Student Page ----------------- #


def student_page():
    select = int(input(f'''
        Please select:
        
        1 - View Classes
        2 - View Grades
        3 - Drop Class

    ENTER: '''))

    # --------- View Students Classes ---------- #

    if select == 1:
        pass


def add_teacher(first_name, last_name, subject):
    session = Session()
    new_teacher = Teachers(first_name=first_name,
                           last_name=last_name, subject=subject)
    session.add(new_teacher)
    session.commit()
    teacher_id = new_teacher.id
    teacher_name = f"{new_teacher.first_name} {new_teacher.last_name}"
    session.close()
    print(f"Added new teacher: {teacher_name} (ID: {teacher_id})")
    return teacher_id, teacher_name


def view_all_teachers():
    session = Session()
    try:
        # query for all teachers
        teachers = session.query(Teachers).all()
        if teachers:
            # print the teachers to the console
            for teacher in teachers:
                print(
                    f"{teacher.id}: {teacher.first_name} {teacher.last_name} - {teacher.subject}")
        else:
            print("No teachers found")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


def add_student(first_name, last_name):
    session = Session()
    new_student = Students(
        first_name=first_name, last_name=last_name)
    session.add(new_student)
    session.commit()
    student_id = new_student.id
    student_name = f"{new_student.first_name} {new_student.last_name}"
    session.close()
    print(f"Added new student: {student_name} (ID: {student_id})")
    return student_id, student_name


def add_grade(teacher_id, student_id, grade):
    session = Session()  # create a new session object
    new_grade = Grades(teachers_id=teacher_id,
                       students_id=student_id, grade=grade)
    session.add(new_grade)
    session.flush()  # flush to generate IDs before committing
    session.commit()
    grade_id = new_grade.id
    teacher_name = session.query(Teachers).filter_by(id=teacher_id).first()
    student_name = session.query(Students).filter_by(id=student_id).first()
    session.close()
    print(f"Added new grade: {grade} (ID: {grade_id}, {teacher_name.first_name} {teacher_name.last_name}, {student_name.first_name} {student_name.last_name})")
    return grade_id, teacher_id, student_id, grade


def view_all_grades(teacher_id):
    session = Session()
    try:
        # query for the teacher object
        teacher = session.query(Teachers).get(teacher_id)
        if teacher:
            # query for all grades associated with the teacher
            grades = session.query(Grades).filter_by(
                teachers_id=teacher_id).all()
            if grades:
                # group the grades by student
                grades_by_student = {}
                for grade in grades:
                    student_id = grade.students_id
                    student = session.query(Students).get(student_id)
                    if student:
                        if student not in grades_by_student:
                            grades_by_student[student] = []
                        grades_by_student[student].append(grade.grade)
                # print the grades to the console
                for student, grades in grades_by_student.items():
                    print(
                        f"{teacher.first_name} {teacher.last_name} - {student.first_name} {student.last_name}: {grades}")
            else:
                print(f"No grades found for teacher with id {teacher_id}")
        else:
            print(f"No teacher found with id {teacher_id}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


def drop_student(student_id):
    session = Session()
    try:
        # Delete all grades associated with the student
        session.query(Grades).filter_by(students_id=student_id).delete()
        session.commit()

        # Delete student from the students table
        student = session.query(Students).get(student_id)
        if student:
            session.delete(student)
            session.commit()
            return True
        else:
            return False
    except IntegrityError as e:
        session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        session.close()

# -------------------- Student's Functions -------------------- #
