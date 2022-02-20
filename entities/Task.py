from .User import User;


class Task:
    """Класс задачи
    :param id: идентификатор
    :type id: int
    :param title: название
    :type title: string
    :param description: описание
    :type description: string
    :param user: пользователь
    :type user: User
    :param condition: состояние
    :type condition: int"""

    def __init__(self, id: int, title: str, description: str, user: User, condition: int):
        self.id = id
        self.title = title
        self.description = description
        self.user = user
        self.condition=condition
