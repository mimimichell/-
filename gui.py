import pandas as pd
import tkinter as tk
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
from tkinter import simpledialog
from db_operations import read_excel, write_excel
from validation import validate_user_login

# Загрузка данных из Excel
fishing_rods = read_excel('database/fishing_rods.xlsx')
customers = read_excel('database/customers.xlsx')
sellers = read_excel('database/sellers.xlsx')
sales = read_excel('database/sales.xlsx')
returns = read_excel('database/returns.xlsx')  
search_criteria = read_excel('database/search_criteria.xlsx')

# Функция для авторизации
def authenticate_user(user_type, login, password):
    if user_type == 'customer':
        return validate_user_login(customers, login, password)
    elif user_type == 'seller':
        return validate_user_login(sellers, login, password)
    return False

# Главный экран
def main_window(root):
    root.title("Информационная система рыболовного магазина")

    label = tk.Label(root, text="Выберите роль:")
    label.pack(pady=10)

    customer_button = tk.Button(root, text="Покупатель", command=lambda: login_window(root, "customer"))
    customer_button.pack(pady=5)

    seller_button = tk.Button(root, text="Продавец", command=lambda: login_window(root, "seller"))
    seller_button.pack(pady=5)

# Окно авторизации
def login_window(root, user_type):
    login = simpledialog.askstring("Логин", "Введите логин:")
    password = simpledialog.askstring("Пароль", "Введите пароль:", show='*')

    if authenticate_user(user_type, login, password):
        messagebox.showinfo("Успех", f"Добро пожаловать, {user_type}!")
        if user_type == 'customer':
            customer_choice_window(root)
        else:
            seller_choice_window(root)
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")

# Окно выбора действий для покупателя
def customer_choice_window(root):
    customer_window = tk.Toplevel(root)
    customer_window.title("Выберите действие")

    search_button = tk.Button(customer_window, text="Поиск удочек", command=lambda: search_fishing_rods_window(root))
    search_button.pack(pady=5)

    sales_button = tk.Button(customer_window, text="Мои покупки", command=lambda: view_sales_window(root))
    sales_button.pack(pady=5)

    return_button = tk.Button(customer_window, text="Возврат удочки", command=lambda: return_fishing_rod_window(root))
    return_button.pack(pady=5)

    buy_button = tk.Button(customer_window, text="Купить удочку", command=lambda: buy_fishing_rod(root))
    buy_button.pack(pady=5)

# Окно выбора действий для продавца
def seller_choice_window(root):
    seller_window = tk.Toplevel(root)
    seller_window.title("Выберите действие")

    sales_button = tk.Button(seller_window, text="Продажа", command=lambda: manage_sales_window(root))
    sales_button.pack(pady=5)

    rods_button = tk.Button(seller_window, text="Удочки", command=lambda: manage_fishing_rods_window(root))
    rods_button.pack(pady=5)

    # Кнопка для добавления товара
    add_rod_button = tk.Button(seller_window, text="Добавить товар", command=lambda: add_fishing_rod_window(root))
    add_rod_button.pack(pady=5)

# Окно для добавления нового товара 
def add_fishing_rod_window(root):
    add_rod_window = tk.Toplevel(root)
    add_rod_window.title("Добавить товар")

    # Ввод данных о товаре
    name_label = tk.Label(add_rod_window, text="Название удочки:")
    name_label.pack(pady=5)
    name_entry = tk.Entry(add_rod_window)
    name_entry.pack(pady=5)

    brand_label = tk.Label(add_rod_window, text="Бренд удочки:")
    brand_label.pack(pady=5)
    brand_entry = tk.Entry(add_rod_window)
    brand_entry.pack(pady=5)

    type_label = tk.Label(add_rod_window, text="Тип удочки:")
    type_label.pack(pady=5)
    type_entry = tk.Entry(add_rod_window)
    type_entry.pack(pady=5)

    price_label = tk.Label(add_rod_window, text="Цена удочки:")
    price_label.pack(pady=5)
    price_entry = tk.Entry(add_rod_window)
    price_entry.pack(pady=5)

    season_label = tk.Label(add_rod_window, text="Сезон удочки:")
    season_label.pack(pady=5)
    season_entry = tk.Entry(add_rod_window)
    season_entry.pack(pady=5)

    # Функция для добавления нового товара в базу данных
    def add_rod_to_database():
        global fishing_rods  

        name = name_entry.get().strip()
        brand = brand_entry.get().strip()
        rod_type = type_entry.get().strip()
        price = price_entry.get().strip()
        season = season_entry.get().strip()

        if not name or not brand or not rod_type or not price or not season:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            new_rod = pd.DataFrame({
                'ID': [len(fishing_rods) + 1],
                'Name': [name],
                'Brand': [brand],
                'Type': [rod_type],
                'Price': [int(price)],  
                'Season': [season]
            })

            fishing_rods = pd.concat([fishing_rods, new_rod], ignore_index=True)

            # Сохраняем изменения в Excel
            fishing_rods.to_excel('database/fishing_rods.xlsx', index=False)

            messagebox.showinfo("Успех", f"Товар '{name}' добавлен в базу данных!")

            
            add_rod_window.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при добавлении товара: {e}")

    # Кнопка для добавления товара
    add_button = tk.Button(add_rod_window, text="Добавить товар", command=add_rod_to_database)
    add_button.pack(pady=10)

# Функция поиска удочек
def search_fishing_rods(type_, brand, season=None):
    type_ = type_.strip().lower()
    brand = brand.strip().lower()

    filtered_rods = fishing_rods[
        (fishing_rods['Type'].str.lower() == type_) &
        (fishing_rods['Brand'].str.lower() == brand)
    ]

    if season:
        filtered_rods = filtered_rods[filtered_rods['Season'].str.lower() == season.lower()]

    if filtered_rods.empty:
        messagebox.showinfo("Результаты поиска", "Нет удочек, соответствующих выбранным критериям.")
    else:
        rods_list = "\n".join(filtered_rods['Name'])
        messagebox.showinfo("Результаты поиска", rods_list)

# Окно для поиска удочек
def search_fishing_rods_window(root):
    search_window = tk.Toplevel(root)
    search_window.title("Поиск удочек")

    type_label = tk.Label(search_window, text="Выберите тип удочки:")
    type_label.pack(pady=5)
    type_var = tk.StringVar(search_window)
    type_var.set(search_criteria['Type'].iloc[0])
    type_menu = tk.OptionMenu(search_window, type_var, *search_criteria['Type'].unique())
    type_menu.pack(pady=5)

    brand_label = tk.Label(search_window, text="Выберите бренд:")
    brand_label.pack(pady=5)
    brand_var = tk.StringVar(search_window)
    brand_var.set(search_criteria['Brand'].iloc[0])
    brand_menu = tk.OptionMenu(search_window, brand_var, *search_criteria['Brand'].unique())
    brand_menu.pack(pady=5)

    season_label = tk.Label(search_window, text="Выберите сезон:")
    season_label.pack(pady=5)
    season_var = tk.StringVar(search_window)
    season_var.set("Лето")
    season_menu = tk.OptionMenu(search_window, season_var, "Весна", "Лето", "Осень", "Зима")
    season_menu.pack(pady=5)

    search_button = tk.Button(search_window, text="Поиск", command=lambda: perform_search(type_var.get(), brand_var.get(), season_var.get()))
    search_button.pack(pady=10)

def perform_search(type_, brand, season):
    type_ = type_.strip().lower()
    brand = brand.strip().lower()
    season = season.strip().lower()

    filtered_rods = fishing_rods[
        (fishing_rods['Type'].str.lower() == type_) &
        (fishing_rods['Brand'].str.lower() == brand) &
        (fishing_rods['Season'].str.lower() == season)
    ]

    if filtered_rods.empty:
        messagebox.showinfo("Результаты поиска", "Нет удочек, соответствующих выбранным критериям.")
    else:
        rods_list = "\n".join(filtered_rods['Name'])
        messagebox.showinfo("Результаты поиска", rods_list)

# Запуск интерфейса
if __name__ == '__main__':
    root = tk.Tk()
    main_window(root)
    root.mainloop()
