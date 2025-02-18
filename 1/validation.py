import pandas as pd

# Проверка логина и пароля
def validate_user_login(df, login, password):
    try:
        user = df[(df['Login'] == login) & (df['password'] == password)]
        
        # Проверка
        if user.empty:
            return False
        return True
    except Exception as e:
        print(f"Ошибка при проверке логина и пароля: {e}")
        return False

data = {
    'Login': ['user1', 'user2', 'user3'],
    'password': ['pass1', 'pass2', 'pass3']
}


df = pd.DataFrame(data)

login = 'user1'
password = 'pass1'

# Проверяем логин и пароль
is_valid = validate_user_login(df, login, password)

if is_valid:
    print("Логин и пароль правильные.")
else:
    print("Логин или пароль неправильные.")
