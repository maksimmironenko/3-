import mysql.connector

class ClientRepDB:
    def __init__(self, db_config):
        self.connection = mysql.connector.connect(**db_config)  # Подключение к БД
        self.cursor = self.connection.cursor(dictionary=True)  # Результаты в виде словаря

    def get_all_clients(self):
        """Получает всех клиентов из базы данных с алиасами для удобства в Python"""
        query = """
        SELECT 
            id,
            LastName AS last_name,
            FirstName AS first_name,
            MiddleName AS middle_name,
            Address AS address,
            Phone AS phone
        FROM clients
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_by_id(self, client_id):
        """ Получить клиента по ID """
        query = "SELECT * FROM clients WHERE id = %s"
        self.cursor.execute(query, (client_id,))
        result = self.cursor.fetchone()
        return result

    def get_k_n_short_list(self, page_number, kolvo):
        """ Получить список клиентов с определённой страницы """
        start = (page_number - 1) * kolvo
        query = "SELECT * FROM clients LIMIT %s, %s"
        self.cursor.execute(query, (start, kolvo))
        result = self.cursor.fetchall()
        return result

    def add_object(self, new_client):
        """ Добавить нового клиента """
        query = """
        INSERT INTO clients (LastName, FirstName, MiddleName, Address, Phone)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (
            new_client['last_name'],
            new_client['first_name'],
            new_client['middle_name'],
            new_client['address'],
            new_client['phone']
        ))
        self.connection.commit()  # Сохраняем изменения
        return self.cursor.lastrowid  # Возвращаем ID нового клиента

    def replace_by_id(self, client_id, new_client):
        """ Обновить данные клиента по ID """
        query = """
        UPDATE clients 
        SET last_name = %s, first_name = %s, middle_name = %s, address = %s, phone = %s 
        WHERE id = %s
        """
        self.cursor.execute(query, (
            new_client['last_name'],
            new_client['first_name'],
            new_client['middle_name'],
            new_client['address'],
            new_client['phone'],
            client_id
        ))
        self.connection.commit()
        return self.cursor.rowcount > 0  # True, если строка обновлена

    def delete_by_id(self, client_id):
        """ Удалить клиента по ID """
        query = "DELETE FROM clients WHERE id = %s"
        self.cursor.execute(query, (client_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0  # True, если строка удалена

    def get_count(self):
        """ Получить количество клиентов """
        query = "SELECT COUNT(*) FROM clients"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result['COUNT(*)']

    def close(self):
        """ Закрыть соединение с БД """
        self.cursor.close()
        self.connection.close()
