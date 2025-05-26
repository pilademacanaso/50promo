from flask import Flask, redirect, request
import string
import random
import os  # <- ESTE FALTABA

app = Flask(__name__)

# Diccionario para almacenar URLs acortadas
url_mapping = {}

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choices(characters, k=6))
    return short_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        short_url = generate_short_url()
        url_mapping[short_url] = original_url
        domain = request.host_url
        return f'Short URL: <a href="{domain}{short_url}">{domain}{short_url}</a>
    return '''
        <form method="post">
            URL to shorten: <input type="text" name="url">
            <input type="submit" value="Shorten">
        </form>
    '''

@app.route('/<short_url>')
def redirect_to_url(short_url):
    original_url = url_mapping.get(short_url)
    if original_url:
        return redirect(original_url)
    return 'URL not found', 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
