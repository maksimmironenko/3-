from model import ClientModel
from ClientRepDB import ClientRepDB  # Ваш класс для работы с БД
from view import ClientView
from controler import ClientController


def main():
    # Создаем конфигурацию подключения к БД
    db_config = {
        "user": "root",
        "password": "Gop2288a",  # Проверьте пароль
        "host": "localhost",
        "database": "clients_new"
    }

    # Создаем объект репозитория и модель
    client_repository = ClientRepDB(db_config)
    client_model = ClientModel(client_repository)

    # Создаем представление
    client_view = ClientView()

    # Создаем контроллер, передавая ему модель и представление
    client_controller = ClientController(client_model, client_view)

    # Если в ClientView предусмотрен метод set_controller, можно установить контроллер:
    client_view.set_controller(client_controller)

    # Загружаем список клиентов (если метод refresh_clients вызывается в контроллере, он уже выполнится)
    client_controller.refresh_clients()

    # Запускаем главный цикл приложения
    client_view.mainloop()


if __name__ == "__main__":
    main()
