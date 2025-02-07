class ClientModel:
    def __init__(self, repository):
        self.repository = repository
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        clients = self.get_all_clients()
        for observer in self.observers:
            observer.refresh(clients)

    def get_all_clients(self):
        return self.repository.get_all_clients()

    def add_client(self, client_data):
        if not client_data.get("last_name") or not client_data.get("first_name"):
            raise ValueError("Фамилия и имя обязательны для заполнения.")
        client_id = self.repository.add_object(client_data)
        if client_id is None:
            raise ValueError("Ошибка добавления клиента.")
        self.notify_observers()
        return client_id
