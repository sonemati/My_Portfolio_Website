from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from bs4 import BeautifulSoup
import requests

markup = requests.get("https://github.com/sonemati?tab=repositories").text
soup = BeautifulSoup(markup, 'html.parser')
proj = [project.getText().strip('\n ').removesuffix('Public') for project in soup.find_all(name="h3", class_="wb-break-all")]
languages = [project.getText() for project in soup.find_all(name="span", itemprop="programmingLanguage")]
descriptions = [project.getText().strip('\n ') for project in soup.find_all(name="p", itemprop="description")]

main_path = 'static/images/'
info = []
for i, value in enumerate(languages):
    if 'django' in descriptions[i].lower():
        lang = 'Python - Django'
        path = f'{main_path}django.png'
    elif 'flask' in descriptions[i].lower():
        lang = 'Python - Flask'
        path = f'{main_path}flask.png'
    else:
        lang = languages[i]
        path = f'{main_path}{lang.lower()}.png'
    info.append({'lang': lang, 'desc': descriptions[i], 'path': path, 'link': f'https://github.com/sonemati/{proj[i]}'})

projects = {}
for i, key in enumerate(proj):
    projects[key] = info[i]

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def home():
    return render_template('index.html', projects=projects)


if __name__ == '__main__':
    app.run(debug=True)
