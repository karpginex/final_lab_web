import sqlite3
from pathlib import Path
from typing import List

from werkzeug.security import check_password_hash, generate_password_hash
from entities import User, Task

# Подключаемся к БД
db_path = '/'.join([str(Path(__file__).parent), '..', 'db', 'database.sqlite'])
db = sqlite3.connect(db_path, check_same_thread=False)


class Storage:
    @staticmethod
    def add_user(user: User):
        """Добавление пользователя
        :param user:    новый пользователь
        :type user:     User"""
        db.execute('INSERT INTO users (email, password) VALUES (?, ?)',
                   (user.email, generate_password_hash(user.password)))
        db.commit()

    @staticmethod
    def get_user_by_email_and_password(email: str, passwordHash: str) -> User:
        """Найти пользователя по email и паролю
        :param email:       электронная почта
        :type email:        str
        :param passwordHash:    хэш пароля
        :type passwordHash:     str
        :return: пользователь
        :rtype: User
        """
        user_data = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
        if user_data and check_password_hash(user_data[2], passwordHash):
            return User(id=user_data[0], email=user_data[1], password=user_data[2])
        else:
            return None

    @staticmethod
    def check_user_by_email(email:str)->User:
        """Найти пользователя по email
        :param email:       электронная почта
        :type email:        str
        :return: да/нет
        :rtype: bool
        """
        user_data=db.execute('SELECT * FROM users WHERE email=?',(email,)).fetchone()
        if user_data:
            return True
        else:
            return False

    @staticmethod
    def get_user_by_id(id: int) -> User:
        """Найти пользователя по id
        :param id:  идентификатор пользователя
        :type id:   int
        :return:    пользователь
        :rtype:     User"""
        user_data = db.execute('SELECT * FROM users WHERE id=?', (id,)).fetchone()
        if user_data:
            return User(id=user_data[0], email=user_data[1], password=user_data[2])
        else:
            return None

    @staticmethod
    def get_task_by_user(user_id: int):
        """
        :param user_id: ентификатор пользователя
        :type user_id: int
        :return: список задач
        :rtype: Tasks[]
        """
        tasks = db.execute("SELECT tasks.id, tasks.title, tasks.description, tasks.id_user, tasks.condition from tasks INNER JOIN users ON tasks.id_user = users.id where users.id=?",
                           (user_id,)).fetchall()
        tasks_list = []
        for task in tasks:
            tasks_list.append(Task(id=task[0],
                                   title=task[1],
                                   description=task[2],
                                   user=Storage.get_user_by_id(task[3]),
                                   condition=task[4]))
        return tasks_list

    @staticmethod
    def get_task_by_id(task_id: int) -> Task:
        """
        :param task_id: идентификатор задачи
        :type task_id: int
        :return: задача
        :rtype: Task
        """
        task_data = db.execute('SELECT * from tasks where tasks.id=?', (task_id,)).fetchone()
        if task_data:
            user = Storage.get_user_by_id(task_data[3])
            return Task(id=task_data[0], title=task_data[1], description=task_data[2], user=user, condition=task_data[4])
        else:
            return None

    @staticmethod
    def add_task(task: Task):
        """Добавление задачи
        :param task: задача
        :type task: Task"""
        db.execute('INSERT INTO tasks (title, description, id_user,condition ) VALUES (?,?,?,?)',
                   (task.title, task.description, task.user.id,0))
        db.commit()

    @staticmethod
    def delete_task(task_id:int):
        """Удаление задачи
        :param task_id: id задачи
        :type task_id: int"""
        db.execute('DELETE FROM tasks WHERE tasks.id=?',(task_id,))
        db.commit()

    @staticmethod
    def change_condition(task_id:int, condition:int):
        """Изменение состояния задачи
        :param task_id: id задачи
        :param condition: новое состояние задачи
        :type task_id: int
        :type condition: int"""
        db.execute('UPDATE tasks SET condition=? WHERE id=?',(condition,task_id,))
        db.commit()

    @staticmethod
    def get_condition(task_id:int)->int:
        """Получение состояния задачи
        :param task_id: id задачи
        :type task_id: int
        :return статус задачи
        :rtype: int"""
        condition = db.execute('SELECT condition FROM tasks WHERE id=?',(task_id,)).fetchone()
        return condition


    @staticmethod
    def update_task(task: Task):
        """Обновление задачи
        :param task: задача
        :type task: Task"""
        db.execute('UPDATE tasks SET title=?, description=? WHERE id=?',(task.title,task.description,task.id,))
        db.commit()