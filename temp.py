import psycopg2

def update_db(data: dict):
    # Замените параметрами вашей базы данных
    db_params = {
        'host': 'your_database_host',
        'database': 'your_database_name',
        'user': 'your_database_user',
        'password': 'your_database_password'
    }

    # Подключение к базе данных PostgreSQL
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            for record_id, update_values in data.items():
                # Проверяем существование записи с указанным идентификатором (например, столбец 'id')
                select_query = f"SELECT COUNT(*) FROM your_table_name WHERE id = %s"
                cursor.execute(select_query, (record_id,))
                record_count = cursor.fetchone()[0]

                if record_count > 0:
                    # Если запись существует, выполняем обновление данных
                    update_query = f"UPDATE your_table_name SET column1 = %s, column2 = %s WHERE id = %s"
                    data_to_update = (update_values['column1'], update_values['column2'], record_id)
                    cursor.execute(update_query, data_to_update)
                else:
                    # Если запись не существует, можно выполнить другие действия, например, создать новую запись
                    pass

            # Фиксируем изменения в базе данных (необязательно, если вы хотите автоматически фиксировать изменения, используйте conn.autocommit = True)
            conn.commit()

# Пример вызова метода update_db() с данными для обновления
data_to_update = {
    'id1': {'column1': 'new_value1', 'column2': 'new_value2'},
    'id2': {'column1': 'new_value3', 'column2': 'new_value4'}
}

update_db(data_to_update)
