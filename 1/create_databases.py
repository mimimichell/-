import pandas as pd
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox


data = {
    'ID': [1, 2, 3, 4],
    'Name': ['Удочка для спиннинга', 'Карповая удочка', 'Поплавочная удочка', 'Мормышка'],
    'Brand': ['Shimano', 'Daiwa', 'Abu Garcia', 'Okuma'],
    'Type': ['Спиннинг', 'Карповая', 'Поплавочная', 'Мормышка'],
    'Price': [5000, 10000, 3000, 1500],
    'Season': ['Летний', 'Зимний', 'Летний', 'Зимний']  
}


fishing_rods = pd.DataFrame(data)


def search_fishing_rods(type_, brand, season=None):
    type_ = type_.strip().lower()
    brand = brand.strip().lower()
    season = season.strip().lower() if season else None

    print("Уникальные типы удочек в базе данных:", fishing_rods['Type'].str.lower().unique())
    print("Уникальные бренды удочек в базе данных:", fishing_rods['Brand'].str.lower().unique())
    print("Выбранный тип:", type_)
    print("Выбранный бренд:", brand)
    print("Выбранный сезон:", season)


    filtered_rods = fishing_rods[
        (fishing_rods['Type'].str.lower() == type_) &  
        (fishing_rods['Brand'].str.lower() == brand)  
    ]

    if season:
        filtered_rods = filtered_rods[filtered_rods['Season'].str.lower() == season]


    if filtered_rods.empty:
        messagebox.showinfo("Результаты поиска", "Нет удочек, соответствующих выбранным критериям.")
    else:
        rods_list = "\n".join(filtered_rods['Name'])
        messagebox.showinfo("Результаты поиска", rods_list)


def search_button_click():
    type_ = type_entry.get()
    brand = brand_entry.get()
    season = season_entry.get()  

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

search_button = Button(root, text="Поиск", command=search_button_click)
search_button.pack()

root.mainloop()
