from flask import Flask, request, render_template, jsonify
import re

app = Flask(__name__)

# Функция для извлечения артикула из ссылки
def extract_article(input_text):
    match = re.search(r'/catalog/(\d+)/', input_text)
    if match:
        return match.group(1)
    return input_text  # Если это уже артикул

@app.route('/')
def home():
    return render_template('index.html')  # Загрузка index.html из папки templates

@app.route('/search', methods=['POST'])
def search():
    # Получаем значение артикула или ссылки и выбранные соцсети
    article_input = request.form['article']
    selected_sites = request.form.getlist('socials')

    # Извлекаем артикул из ссылки или используем введенный текст как артикул
    article = extract_article(article_input)

    # Формируем Google Dork-запрос для выбранных соцсетей
    site_templates = {
        'instagram': 'site:instagram.com "{}"',
        'tiktok': 'site:tiktok.com "{}"',
        'youtube': 'site:youtube.com "{}"',
    }

    # Создаем поисковые запросы для каждой выбранной соцсети
    queries = [site_templates[site].format(article) for site in selected_sites]
    full_query = " OR ".join(queries)

    # URL для Google-поиска
    google_url = f"https://www.google.com/search?q={full_query}"
    return jsonify({'url': google_url})  # Возвращаем JSON с URL для открытия в новой вкладке

if __name__ == '__main__':
    app.run(debug=True)
