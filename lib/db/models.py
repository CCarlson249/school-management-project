from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///pet_stores.db')

Base = declarative_base()

class Teachers(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    subject = Column(String())

    grades = relationship('Grades', backref=backref('teachers'))
    def __repr__(self):
        return f"Teacher(id={self.id}, name='{self.first_name} {self.last_name}', subject='{self.subject}')"


class Students(Base):
    __tablename__ = 'students'

    id = Column(Integer(), primary_key = True)
    first_name = Column(String()),
    last_name = Column(String()),

    grades = relationship('Grades', backref=backref('students'))    
    def __repr__(self):
        return f"Student(id={self.id}, name='{self.first_name} {self.last_name}')"


class Grades(Base):
    __tablename__ = "grades"

    id = Column(Integer(), primary_key = True)
    teacher_id = Column(Integer(), ForeignKey('teachers.id'))
    students_id = Column(Integer(), ForeignKey('students.id'))
    grade = Column(String())

    def __repr__(self):
        return f"Grade(id={self.id}, teacher_id={self.teacher_id}, student_id={self.student_id}, grade='{self.grade}')"

    




