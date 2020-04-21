from pprint import pprint
import psycopg2 as pg


con = pg.connect(database = 'test_db',
                user = 'admin',
                password = 1234)

cur = con.cursor()


a_single_student = {'name':'Sergey', 'gpa':4.8, 'birth':'1988-01-31'}
students_list = [{'name':'Pavel', 'gpa':5.3, 'birth':'1987-05-23'},
                 {'name':'Anton', 'gpa':5.8, 'birth':'1985-12-9'},
                 {'name':'Denis', 'gpa':4.0, 'birth':'1986-05-30'}]


# создаем таблицы
def create_db():
    cur.execute('''
        CREATE TABLE if not exists student
            (
                id SERIAL PRIMARY KEY,
                name varchar(100) NOT NULL,
                gpa numeric(10, 2),
                birth timestamp with time zone        
            );
        
        CREATE TABLE if not exists course
            (
                id SERIAL PRIMARY KEY,
                name varchar(100) NOT NULL
            );

        CREATE TABLE if not exists course_name
            (
                id SERIAL PRIMARY KEY,
                student_id INT REFERENCES student(id),
                course_id INT REFERENCES course(id)
            )
        ''')
    con.commit()


# возвращает студентов определенного курса
def get_students(course_id): 
    cur.execute('''
        SELECT student_id
        FROM course_name
        WHERE course_id = %s
    ''', (course_id,))
    temporary_students_list = cur.fetchall()
    print(f'\nвывод информации по всем студентам с курса №{course_id}')
    for i in temporary_students_list:
        cur.execute('''
            SELECT name, gpa
            FROM student
            WHERE id=%s
        ''', (i,))
        student_info = cur.fetchall()
        print(student_info)


# создает студентов и записывает их на курс
def add_students(course_id, students):
    cur.execute('INSERT INTO course VALUES(default, %s)', (course_id))        

    for student in students:
        cur.execute('''
            INSERT INTO student
            VALUES
            (default, %s, %s, %s)
        ''', (student['name'], student['gpa'], student['birth']))
        con.commit()

        cur.execute('''
            SELECT id
            FROM student
            WHERE name=%s
        ''', (student['name'],))
        student_id = cur.fetchall()
        cur.execute('''
            INSERT INTO course_name
            VALUES
            (default, %s, %s)
        ''', (student_id[0], course_id))
        con.commit()


# просто создает студента
def add_student(student): 
    cur.execute('''
        INSERT INTO student
        VALUES
        (default, %s, %s, %s)
    ''', (student['name'], student['gpa'], student['birth']))
    con.commit()


# получаем данные студента
def get_student(student_id):
    cur.execute('''
        SELECT name, gpa
        FROM student
        WHERE id = %s
    ''',(student_id,))
    student = cur.fetchall()
    con.commit()
    print(f'вывод одного студента:\n{student}')


if __name__ == '__main__':
    create_db()
    add_students('1', students_list)
    add_student(a_single_student)
    get_student('1')
    get_students(1)
    con.close()