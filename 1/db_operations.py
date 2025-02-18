import pandas as pd

# Чтение данных из Excel
def read_excel(file_name):
    return pd.read_excel(file_name)

# Запись данных в Excel
def write_excel(file_name, data):
    data.to_excel(file_name, index=False)

# Получение информации по ID
def get_item_by_id(df, item_id):
    return df[df['ID'] == item_id]

# Добавление новой записи
def add_item(df, item_data):
    df = df.append(item_data, ignore_index=True)
    return df
