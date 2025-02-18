import pandas as pd
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
from db_operations import read_excel
from validation import validate_user_login 

# Загрузка данных
fishing_rods = read_excel('database/fishing_rods.xlsx')

def authenticate_user(user_type, login, password):
    if user_type == 'customer':
        return validate_user_login(customers, login, password)
    elif user_type == 'seller':
        return validate_user_login(sellers, login, password)
    return False

# Функция поиска удочек 
def search_fishing_rods(type_, brand, season=None):
    type_ = type_.strip().lower()
    brand = brand.strip().lower()

    print("Уникальные типы удочек в базе данных:", fishing_rods['Type'].str.lower().unique())
    print("Уникальные бренды удочек в базе данных:", fishing_rods['Brand'].str.lower().unique())

    # Фильтруем удочки по типу и бренду
    filtered_rods = fishing_rods[
        (fishing_rods['Type'].str.lower() == type_) &  # Фильтруем по типу
        (fishing_rods['Brand'].str.lower() == brand)  # Фильтруем по бренду
    ]

    if season:
        filtered_rods = filtered_rods[filtered_rods['Season'].str.lower() == season.lower()]

    if filtered_rods.empty:
        messagebox.showinfo("Результаты поиска", "Нет удочек, соответствующих выбранным критериям.")
    else:
        # Выводим список удочек
        rods_list = "\n".join(filtered_rods['Name'])
        messagebox.showinfo("Результаты поиска", rods_list)


def search_button_click():
    type_ = type_entry.get()
    brand = brand_entry.get()
    season = season_entry.get()  

    # Вызываем функцию поиска удочек
    search_fishing_rods(type_, brand, season)


root = Tk()
root.title("Поиск удочек")

Label(root, text="Тип удочки:").pack()
type_entry = Entry(root)
type_entry.pack()

Label(root, text="Бренд удочки:").pack()
brand_entry = Entry(root)
brand_entry.pack()

Label(root, text="Сезон (необязательно):").pack()
season_entry = Entry(root)
season_entry.pack()

# Кнопка для поиска
search_button = Button(root, text="Поиск", command=search_button_click)
search_button.pack()

# Запуск интерфейса
root.mainloop()
