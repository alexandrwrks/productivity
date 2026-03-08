import sqlite3
import os

class DataBase:
    def __init__(self, db_name="me_database.db"):
        self.db_name = db_name
        print(f"🚀 Инициализация базы данных: {db_name}")
        self.init_database()

    def init_database(self):
        """ИНИЦИАЛИЗАЦИЯ СТРУКТУРЫ ДАННЫХ"""
        connection = None
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()

            # Таблица студентов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    birth_data TEXT,
                    group_name TEXT,
                    enrollment_year INTEGER
                )
            ''')

            # Таблица преподавателей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Teachers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    department TEXT,
                    position TEXT
                )
            ''')
            
            # Таблица курсов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    credits INTEGER,
                    teacher_id INTEGER,
                    FOREIGN KEY (teacher_id) REFERENCES Teachers (id)
                )
            ''')
            
            # Таблица оценок
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    course_id INTEGER,
                    grade INTEGER,
                    date TEXT,
                    FOREIGN KEY (student_id) REFERENCES Students (id),
                    FOREIGN KEY (course_id) REFERENCES Courses (id)
                )
            ''')
            
            connection.commit()
            print("✅ База данных успешно создана!")
            print("   Созданы таблицы: Students, Teachers, Courses, Grades")

        except sqlite3.Error as e:
            print(f"❌ Ошибка при создании базы данных: {e}")
        finally:
            if connection:
                connection.close()

    def add_sample_data(self):
        """Добавление тестовых данных"""
        connection = None
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            
            print("\n📝 Добавление тестовых данных...")

            # Очищаем таблицы перед добавлением
            cursor.execute("DELETE FROM Grades")
            cursor.execute("DELETE FROM Courses")
            cursor.execute("DELETE FROM Students")
            cursor.execute("DELETE FROM Teachers")
            
            # Сбрасываем автоинкремент
            cursor.execute("DELETE FROM sqlite_sequence")
            
            print("🧹 Таблицы очищены")

            # Добавляем преподавателей
            teachers_data = [
                ('Иван', 'Петров', 'ivan.petrov@university.ru', '+7 (999) 123-45-67', 'Математика', 'Профессор'),
                ('Мария', 'Сидорова', 'maria.sidorova@university.ru', '+7 (999) 234-56-78', 'Физика', 'Доцент'),
                ('Алексей', 'Иванов', 'alexey.ivanov@university.ru', '+7 (999) 345-67-89', 'Программирование', 'Старший преподаватель')
            ]

            for teacher in teachers_data:
                cursor.execute('''
                    INSERT INTO Teachers (first_name, last_name, email, phone, department, position)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', teacher)
                print(f"   ✅ Добавлен преподаватель: {teacher[0]} {teacher[1]}")

            # Добавляем студентов
            students_data = [
                ('Петр', 'Смирнов', 'petr.smirnov@student.ru', '+7 (999) 456-78-90', '2000-05-15', 'ИС-21', 2021),
                ('Анна', 'Козлова', 'anna.kozlova@student.ru', '+7 (999) 567-89-01', '2001-08-23', 'ИС-21', 2021),
                ('Дмитрий', 'Новиков', 'dmitry.novikov@student.ru', '+7 (999) 678-90-12', '2000-11-10', 'МО-22', 2022)
            ]
            
            for student in students_data:
                cursor.execute('''
                    INSERT INTO Students (first_name, last_name, email, phone, birth_data, group_name, enrollment_year)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', student)
                print(f"   ✅ Добавлен студент: {student[0]} {student[1]}")

            # Добавляем курсы
            course_data = [
                ('Высшая математика', 'Математический анализ и линейная алгебра', 4, 1),
                ('Физика', 'Общая физика', 4, 2),
                ('Python программирование', 'Основы Python и ООП', 3, 3),
                ('Базы данных', 'SQL и работа с БД', 3, 3)
            ]

            for course in course_data:
                cursor.execute('''
                    INSERT INTO Courses (name, description, credits, teacher_id)
                    VALUES (?, ?, ?, ?)
                ''', course)
                print(f"   ✅ Добавлен курс: {course[0]}")
                
            connection.commit()
            print("\n✅ Тестовые данные успешно добавлены!")

        except sqlite3.Error as e:
            print(f"❌ Ошибка при добавлении данных: {e}")
            if connection:
                connection.rollback()
        finally:
            if connection:
                connection.close()

    def view_all_data(self):
        """Просмотр всех данных в базе"""
        connection = None
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()

            print("\n" + "="*60)
            print("📊 СОДЕРЖИМОЕ БАЗЫ ДАННЫХ")
            print("="*60)

            # СТУДЕНТЫ
            cursor.execute("SELECT * FROM Students")
            students = cursor.fetchall()
            print(f"\n👨‍🎓 СТУДЕНТЫ (всего: {len(students)})")
            print("-" * 60)
            if students:
                for student in students:
                    print(f"┌ ID: {student[0]}")
                    print(f"├ Имя: {student[1]} {student[2]}")
                    print(f"├ Email: {student[3]}")
                    print(f"├ Телефон: {student[4]}")
                    print(f"├ Дата рождения: {student[5]}")
                    print(f"├ Группа: {student[6]}")
                    print(f"└ Год поступления: {student[7]}\n")
            else:
                print("   Нет данных\n")

            # ПРЕПОДАВАТЕЛИ
            cursor.execute("SELECT * FROM Teachers")
            teachers = cursor.fetchall()
            print(f"👨‍🏫 ПРЕПОДАВАТЕЛИ (всего: {len(teachers)})")
            print("-" * 60)
            if teachers:
                for teacher in teachers:
                    print(f"┌ ID: {teacher[0]}")
                    print(f"├ Имя: {teacher[1]} {teacher[2]}")
                    print(f"├ Email: {teacher[3]}")
                    print(f"├ Телефон: {teacher[4]}")
                    print(f"├ Кафедра: {teacher[5]}")
                    print(f"└ Должность: {teacher[6]}\n")
            else:
                print("   Нет данных\n")

            # КУРСЫ
            cursor.execute('''
                SELECT Courses.id, Courses.name, Courses.description, 
                       Courses.credits, Teachers.first_name, Teachers.last_name
                FROM Courses
                LEFT JOIN Teachers ON Courses.teacher_id = Teachers.id
            ''')
            courses = cursor.fetchall()
            print(f"📚 КУРСЫ (всего: {len(courses)})")
            print("-" * 60)
            if courses:
                for course in courses:
                    print(f"┌ ID: {course[0]}")
                    print(f"├ Название: {course[1]}")
                    print(f"├ Описание: {course[2]}")
                    print(f"├ Кредиты: {course[3]}")
                    if course[4]:
                        print(f"└ Преподаватель: {course[4]} {course[5]}\n")
                    else:
                        print("└ Преподаватель: не назначен\n")
            else:
                print("   Нет данных\n")

        except sqlite3.Error as e:
            print(f"❌ Ошибка при чтении данных: {e}")
        finally:
            if connection:
                connection.close()

    def check_data(self):
        """Проверка наличия данных в таблицах"""
        connection = None
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            
            print("\n📊 Статистика базы данных:")
            tables = ['Teachers', 'Students', 'Courses', 'Grades']
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   • {table}: {count} записей")
                
        except sqlite3.Error as e:
            print(f"❌ Ошибка при проверке: {e}")
        finally:
            if connection:
                connection.close()

# Создаем экземпляр базы данных
db = DataBase()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 РАБОТА С БАЗОЙ ДАННЫХ")
    print("="*60)

    while True:
        print("\nМеню:")
        print("1. Инициализировать базу данных")
        print("2. Добавить тестовые данные")
        print("3. Показать все данные")
        print("4. Проверить статистику")
        print("5. Выйти")
        
        choice = input("\nВыберите действие (1-5): ")
        
        if choice == '1':
            db.init_database()
        elif choice == '2':
            db.add_sample_data()
        elif choice == '3':
            db.view_all_data()
        elif choice == '4':
            db.check_data()
        elif choice == '5':
            print("\n👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.")
    
    print(f"\n📁 Файл базы данных: {db.db_name}")
    print("📝 Ты можешь открыть этот файл в DB Browser for SQLite")