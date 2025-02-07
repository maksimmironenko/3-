from view import ClientView, ClientAddView  # Убедитесь, что ClientAddView есть в файле view
from model import ClientModel

class ClientController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.add_observer(self)  # Регистрируем контроллер как наблюдателя
        self.refresh_clients()

    def refresh_clients(self):
        """Обновление списка клиентов в представлении"""
        clients = self.model.get_all_clients()
        self.view.refresh(clients)  # Обновляем интерфейс с клиентами

    def show_client_details(self, client_id):
        """Показать подробности о клиенте"""
        client = self.model.get_client_by_id(client_id)
        if client:
            self.view.show_client_details(client)  # Передаем данные в представление

    def open_add_client_window(self):
        """Открыть окно для добавления нового клиента"""
        add_view = ClientAddView(self.view)  # Создаем представление для добавления
        add_view.controller = self  # Устанавливаем текущий контроллер для добавления
        add_view.grab_set()  # Блокировка основного окна пока открыто окно добавления

    def add_client(self, client_data):
        """Добавить клиента через модель"""
        try:
            client_id = self.model.add_client(client_data)
            self.view.show_success(f"Клиент добавлен с ID {client_id}")
            self.refresh_clients()  # Обновить список после добавления
        except ValueError as e:
            self.view.show_error(str(e))  # Показываем ошибку валидации
