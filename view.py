import tkinter as tk
from tkinter import ttk

class ClientView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.controller = None  # Контроллер будет установлен позже
        self.title("Управление клиентами")
        self.geometry("800x600")
        self.create_widgets()

    def set_controller(self, controller):
        """Устанавливает контроллер и обновляет команду кнопки."""
        self.controller = controller
        # Теперь, когда контроллер установлен, обновляем команду кнопки
        self.add_button.config(state="normal", command=self.controller.open_add_client_window)

    def create_widgets(self):
        # Создаем кнопку добавления клиента в неактивном состоянии,
        # так как контроллер еще не установлен.
        self.add_button = tk.Button(self, text="Добавить клиента", state="disabled")
        self.add_button.pack(pady=10)

        # Создаем таблицу для отображения клиентов
        self.table = ttk.Treeview(
            self,
            columns=("ID", "Фамилия", "Имя", "Отчество", "Адрес", "Телефон"),
            show="headings"
        )
        self.table.heading("ID", text="ID")
        self.table.heading("Фамилия", text="Фамилия")
        self.table.heading("Имя", text="Имя")
        self.table.heading("Отчество", text="Отчество")
        self.table.heading("Адрес", text="Адрес")
        self.table.heading("Телефон", text="Телефон")
        self.table.bind("<Double-1>", self.open_client_details)
        self.table.pack(fill=tk.BOTH, expand=True)

    def refresh(self, clients):
        """Обновляет данные в таблице."""
        for row in self.table.get_children():
            self.table.delete(row)
        for client in clients:
            self.table.insert("", "end", values=(
                client["id"],
                client["last_name"],
                client["first_name"],
                client["middle_name"],
                client["address"],
                client["phone"]
            ))

    def show_success(self, message):
        """Показывает окно с сообщением об успехе."""
        success_window = tk.Toplevel(self)
        success_window.title("Успех")
        tk.Label(success_window, text=message).pack(pady=20)
        tk.Button(success_window, text="OK", command=success_window.destroy).pack()

    def show_error(self, message):
        """Показывает окно с сообщением об ошибке."""
        error_window = tk.Toplevel(self)
        error_window.title("Ошибка")
        tk.Label(error_window, text=message).pack(pady=20)
        tk.Button(error_window, text="OK", command=error_window.destroy).pack()

    def open_client_details(self, event):
        """Открывает подробную информацию о выбранном клиенте."""
        selected_item = self.table.selection()
        if not selected_item:
            return
        client_id = self.table.item(selected_item)["values"][0]
        self.controller.show_client_details(client_id)




class ClientAddView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Добавить клиента")
        self.geometry("400x400")

        # Поле "Имя"
        self.first_name_label = tk.Label(self, text="Имя")
        self.first_name_label.pack(pady=5)
        self.first_name_entry = tk.Entry(self)
        self.first_name_entry.pack(pady=5)

        # Поле "Фамилия"
        self.last_name_label = tk.Label(self, text="Фамилия")
        self.last_name_label.pack(pady=5)
        self.last_name_entry = tk.Entry(self)
        self.last_name_entry.pack(pady=5)

        # Поле "Отчество"
        self.middle_name_label = tk.Label(self, text="Отчество")
        self.middle_name_label.pack(pady=5)
        self.middle_name_entry = tk.Entry(self)
        self.middle_name_entry.pack(pady=5)

        # Поле "Адрес"
        self.address_label = tk.Label(self, text="Адрес")
        self.address_label.pack(pady=5)
        self.address_entry = tk.Entry(self)
        self.address_entry.pack(pady=5)

        # Поле "Телефон"
        self.phone_label = tk.Label(self, text="Телефон")
        self.phone_label.pack(pady=5)
        self.phone_entry = tk.Entry(self)
        self.phone_entry.pack(pady=5)

        # Кнопка "Сохранить"
        self.save_button = tk.Button(self, text="Сохранить", command=self.save_client)
        self.save_button.pack(pady=20)

    def save_client(self):
        # Сбор данных из всех полей
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        middle_name = self.middle_name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        client_data = {
            "first_name": first_name,
            "last_name": last_name,
            "middle_name": middle_name,
            "address": address,
            "phone": phone
        }
        # Передаем данные в контроллер для добавления клиента
        self.controller.add_client(client_data)
        self.destroy()
