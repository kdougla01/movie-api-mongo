from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/movie', methods=['POST'])
def movie():
    apikey = '6f6c977'
    title_search = request.form['title_search']
    r = requests.get('http://www.omdbapi.com/?apikey='+apikey+'&s='+title_search)
    json_object = r.json()

    items = json_object['Search']

    for item in items:
        title = item['Title']
        year = item['Year']
        poster = item['Poster']
        imdbID = item['imdbID']

    return render_template('movie.html', items=items)


@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')