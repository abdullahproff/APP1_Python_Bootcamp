from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Папка для загруженных файлов
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'ogg'}  # Разрешенные расширения
app.secret_key = 'supersecretkey'  # Секретный ключ для Flask (нужен для flash-сообщений)

# Проверка, что файл имеет допустимое расширение
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Главная страница
@app.route('/')
def index():
    # Получаем список загруженных файлов
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

# Загрузка файла
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400  # Возвращаем ошибку 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400  # Возвращаем ошибку 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "File uploaded successfully!", 200  # Возвращаем успешный ответ
    else:
        return "Non-audio file detected", 400  # Возвращаем ошибку 400

# Новый маршрут для получения списка файлов в формате JSON
@app.route('/files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

# Запуск сервера
if __name__ == '__main__':
    # Создаем папку для загрузок, если её нет
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(host='0.0.0.0', port=8888)