from flask import Flask, session, render_template, redirect, request, url_for
from entities import User, Task
from storage import Storage

# Создаём приложение
app = Flask(__name__)

# Конфигурируем
# Устанавливаем ключ, необходимый для шифрования куки сессии
app.secret_key = b'_5#y2L"F4Q8ziDec]/'


# Описываем основные маршруты и их обработчики

# Главная страница
@app.route('/')
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)
        return render_template('pages/index.html', user=user)
    else:
        return redirect('/login')


# Страница с формой входа
@app.route('/login', methods=['GET'])
def login():
    if 'user_id' in session:
        return redirect('/')
    return render_template('pages/login.html', page_title='Auth Example')


# Обработка формы входа
@app.route('/login', methods=['POST'])
def login_action():
    page_title = 'Вход / Auth Example'

    # Введённые данные получаем из тела запроса
    if not request.form['email']:
        return render_template('pages/login.html', page_title=page_title, error='Требуется ввести email')
    if not request.form['password']:
        return render_template('pages/login.html', page_title=page_title, error='Требуется ввести пароль')

    # Ищем пользователя в БД с таким email паролем
    user = Storage.get_user_by_email_and_password(request.form['email'], request.form['password'])

    # Неверные данные для входа
    if not user:
        return render_template('pages/login.html', page_title=page_title, error='Неверный логин или пароль')

    # Сохраняем пользователя в сессии
    session['user_id'] = user.id

    # Перенаправляем на главную страницу
    return redirect(url_for('home'))


# Форма регистрации
@app.route('/registration', methods=['GET'])
def registration():
    return render_template('pages/registration.html', page_title='Регистрация / Auth Example')


# Обработка формы регистрации
@app.route('/registration', methods=['POST'])
def registration_action():
    page_title = 'Регистрация | Auth Example'
    error = None
    # Проверяем данные
    if not request.form['email']:
        error = 'Требуется ввести Email'
    if not request.form['password']:
        error = 'Требуется ввести пароль'
    if not request.form['password2']:
        error = 'Требуется ввести повтор пароля'
    if request.form['password'] != request.form['password2']:
        error = 'Пароли не совпадают'

    # В случае ошибки рендерим тот же шаблон, но с текстом ошибки
    if error:
        return render_template('pages/registration.html', page_title=page_title, error=error)

    check_user = Storage.check_user_by_email(request.form['email'])
    if check_user:
        return render_template('pages/registration.html',page_title=page_title,error='Пользователь с таким логином уже существует')

    # Добавляем пользователя
    Storage.add_user(User(None, request.form['email'], request.form['password']))

    # Делаем вид, что добавление всегда без ошибки
    # Перенаправляем на главную
    return redirect(url_for('home'))


# Выход пользователя
@app.route('/logout')
def logout():
    # Просто выкидываем его из сессии
    session.pop('user_id')
    return redirect(url_for('home'))


@app.route("/tasks", methods=['GET'])
def show_tasks():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)
        tasks = Storage.get_task_by_user(user_id)
        return render_template("pages/task_list.html", page_title="Список задач", tasks=tasks, user=user)
    else:
        return redirect('/login')




@app.route('/task', methods=['GET'])
def new_task():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)
        return render_template('pages/new_task.html', page_title='Добавить задачу', user=user)
    else:
        return redirect('/login')


@app.route('/task', methods=['POST'])
def create_task():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)

        error = None
        if not request.form['title-input']:
            error = 'Требуется ввести заголовок задачи'
        if error:
            return render_template('pages/new_task.html', page_title='Добавить задачу', error=error, user=user)
        Storage.add_task(Task(None, request.form['title-input'], request.form['description-input'], user,0))
        return redirect(url_for('show_tasks'))
    else:
        redirect(url_for('home'))


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id: int):
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)
        task = Storage.get_task_by_id(task_id)
        if task.user.id != user.id:
            return redirect('/tasks')
        else:
            return render_template('pages/task.html', page_title='Отредактировать задачу', task=task, user=user)
    else:
        return redirect('/login')



@app.route('/delete/<int:task_id>', methods=['GET'])
def remove_task(task_id:int):
    if 'user_id' in session:
        Storage.delete_task(task_id)
    else:
        redirect('/login')



@app.route('/create_task/<int:task_id>',methods=['POST'])
def refresh_task(task_id:int):
    if 'user_id' in session:
        user_id=session['user_id']
        user=Storage.get_user_by_id(user_id)
        Storage.update_task(Task(task_id,request.form['title-input'],request.form['description-input'],user,0))
        return  redirect(url_for('show_tasks'))
    else:
        return redirect('/login')



@app.route('/condition/<int:task_id>', methods=['GET'])
def change_condition_task(task_id:int):
    if 'user_id' in session:
        condition=Storage.get_condition(task_id)
        condition=(condition[0]+1)%2
        Storage.change_condition(task_id,condition)
    else:
        redirect('/login')

if __name__ == '__main__':
    app.env = 'development'
    app.run(port=3000, host='0.0.0.0', debug=True)
