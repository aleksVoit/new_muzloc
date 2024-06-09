from flask import Flask, render_template, request, jsonify
import psycopg2
import configparser

app = Flask(__name__)

# Чтение конфигурационного файла
config = configparser.ConfigParser()
config.read('config.ini')

# Получение параметров подключения к базе данных
user = config.get('DEV_DB', 'USER')
password = config.get('DEV_DB', 'PASSWORD')
domain = config.get('DEV_DB', 'DOMAIN')
port = config.get('DEV_DB', 'PORT')
db = config.get('DEV_DB', 'DB_NAME')


# Функция для подключения к базе данных PostgreSQL
def connect_to_database():
    conn = psycopg2.connect(
        dbname=db,
        user=user,
        password=password,
        host=domain,
        port=port
    )
    return conn


# Получение всех пользователей из базы данных
def get_users():
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("SELECT * FROM accounts")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users


# Добавление нового пользователя в базу данных
def add_user(name, email, phone, password):
    conn = connect_to_database()
    cur = conn.cursor()

    cur.execute("INSERT INTO accounts (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
    cur.execute("select max(account_id) from accounts")
    acc_id = cur.fetchone()[0]
    cur.execute("INSERT INTO registrations (password, account_id) VALUES (%s, %s)", (password, acc_id))
    cur.execute("INSERT INTO profiles (birthday, bio, location, photo, music, video, post, account_id) \
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (None, None, None, None, None, None, None, acc_id))
    conn.commit()
    cur.close()
    conn.close()


def update_user_profile(birthday, bio, location, photo, video, music, post, acc_id):
    conn = connect_to_database()
    cur = conn.cursor()

    if birthday:
        cur.execute("UPDATE profiles SET birthday = %s WHERE account_id = %s", (birthday, acc_id))

    if bio:
        cur.execute("UPDATE profiles SET bio = %s WHERE account_id = %s", (bio, acc_id))

    if location:
        cur.execute("UPDATE profiles SET location = %s WHERE account_id = %s", (location, acc_id))

    if photo:
        cur.execute("UPDATE profiles SET photo = %s WHERE account_id = %s", (photo, acc_id))

    if video:
        cur.execute("UPDATE profiles SET video = %s WHERE account_id = %s", (video, acc_id))

    if music:
        cur.execute("UPDATE profiles SET music = %s WHERE account_id = %s", (music, acc_id))

    if post:
        cur.execute("UPDATE profiles SET post = %s WHERE account_id = %s", (post, acc_id))

    # cur.execute("INSERT INTO accounts (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
    # cur.execute("select max(account_id) from accounts")
    # acc_id = cur.fetchone()[0]
    # cur.execute("INSERT INTO registrations (password, account_id) VALUES (%s, %s)", (password, acc_id))
    # cur.execute("INSERT INTO profiles (birthday, bio, location, photo, music, video, post, account_id) \
    #              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (None, None, None, None, None, None, None, acc_id))

    conn.commit()
    cur.close()
    conn.close()


# Основная страница
@app.route('/')
def index():
    users = get_users()
    return render_template('index.html', users=users)


# Обработка данных формы регистрации
@app.route('/register_new_user', methods=['POST'])
def register_new_user():
    print('register_new_user')
    if request.is_json:
        data = request.get_json()
        name = data['name']
        email = data['email']
        phone = data['phone']
        password = data['password']
        print('here adding user')
        add_user(name, email, phone, password)
        return jsonify({'message': 'Пользователь успешно зарегистрирован'})
    else:
        return jsonify({'error': 'Request Content-Type was not application/json'}), 400


@app.route('/update_profile/<account_id>', methods=['POST'])
def update_profile(account_id):
    print('update profile>>>', account_id)
    if request.is_json:
        data = request.get_json()
        birthday = data['birthday']
        bio = data['bio']
        city = data['location']
        photo = data['photo']
        video = data['video']
        music = data['music']
        post = data['post']
        print('here adding user profile')
        update_user_profile(birthday, bio, city, photo, video, music, post, account_id)
        return jsonify({'message': 'Пользователь успешно зарегистрирован'})
    else:
        return jsonify({'error': 'Request Content-Type was not application/json'}), 400


@app.route('/login', methods=['POST'])
def login():
    print('login here')
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = connect_to_database()
    cur = conn.cursor()

    cur.execute("select account_id from accounts where email=%s", (email,))
    acc_id = cur.fetchall()[0][0]

    cur.execute("select password from registrations where account_id=%s", (acc_id,))
    pswd = cur.fetchall()[0][0]

    # Обработка логина (это просто пример, на практике вы бы проверяли данные в БД)
    if pswd == password:
        print('return json')
        return jsonify({"message": "Успешный вход", 'account_id': acc_id})
    else:
        return jsonify({"error": "Неверное имя пользователя или пароль"}), 400


@app.route('/user/<account_id>', methods=['GET'])
def user_page(account_id):
    print('user page render')
    conn = connect_to_database()
    cur = conn.cursor()

    cur.execute('select name from accounts where account_id=%s', (account_id,))
    username = cur.fetchone()[0]

    return render_template('user.html', account_id=account_id, username=username)


@app.route('/register-page', methods=['GET'])
def register():
    print('register_page')
    return render_template('registration.html')


@app.route('/update-profile-page/<account_id>', methods=['GET'])
def edit_profile(account_id):
    print('edit profile --- main.py')
    return render_template('edit_profile.html', account_id=account_id)


@app.route('/new_user_confirmation', methods=['GET'])
def new_user_confirmation():
    print('confirmation_page')
    return render_template('new_user_confirmation.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
