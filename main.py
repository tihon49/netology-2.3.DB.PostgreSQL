from pprint import pprint
import psycopg2 as pg
import datetime as dt


#create connection
con = pg.connect(database = 'netology',
                 user = 'admin',
                 password = 1234)

print('connected to the DB secesfuly')
cur = con.cursor()
print('cursor created secesfully')

student_1 = {'name':'Alex', 'gpa':5, 'birth':dt.datetime(1985, 12, 11)}
student_2 = {'name':'Den', 'gpa':3, 'birth':dt.datetime(1986, 5, 30)}

students_list = [
    {'name':'Alex', 'gpa':4, 'birth':dt.datetime(1995, 5, 10)},
    {'name':'Nik', 'gpa':4, 'birth':dt.datetime(1986, 10, 27)},
    {'name':'Bob', 'gpa':3, 'birth':dt.datetime(1989, 7, 25)}
]


# создает таблицы
def create_db(): 
    cur.execute("""
        CREATE TABLE if not exists Student(
                id serial PRIMARY KEY not null,
                name varchar(100) not null,
                gpa numeric(10,2),
                birth timestamp with time zone
            );
        CREATE TABLE if not exists Course(
                id serial PRIMARY KEY not null,
                name varchar(100) not null
            );        
        CREATE TABLE if not exists Course_name(
                id serial PRIMARY KEY not null,
                student_id INTEGER REFERENCES student(id),
                course_id INTEGER REFERENCES course(id)
            );
    """)
    con.commit()


# получаем студентов
def get_students(course_id): 
    cur.execute("select name from Student where id=%s", (course_id))
    pprint(cur.fetchall())


# создает студентов и записывает их на курс
def add_students(course_id, students):
    cur.execute("insert into Course values (default, %s);", (course_id))
    con.commit()

    for student in students:
        cur.execute("""
            insert into Student (name,  gpa, birth) 
            values(%s, %s, %s)""",
            (student['name'], student['gpa'], student['birth']))
        con.commit()

        cur.execute("select id from Student where name=%s;", (student['name'],))
        fetch_name = cur.fetchall()

        cur.execute("insert into Course_name values (default, %s, %s);", (fetch_name[0], course_id))
        con.commit()


# просто создает студента
def add_student(student): 
    cur.execute("insert into Student (name, gpa, birth) values(%s, %s, %s);",
               (student['name'], student['gpa'], student['birth']))
    con.commit()


#получаем имя студента по его id
def get_student(student_id):
    cur.execute("select name from Student where id=%s", (student_id))


if __name__ == '__main__':
    create_db()
    add_students('1', students_list)
    add_student(student_1)
    get_student('3')
    get_students('1')
