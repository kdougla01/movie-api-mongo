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

    #return json_object
    #return str(items)
    return render_template('movie.html', items=items)

@app.route('/info', defaults={'id': 'tt4654462'})
@app.route('/info/<id>', methods=['POST','GET'])
def info(id):
    apikey = '6f6c977'
    imdb_search = id
    r = requests.get('http://www.omdbapi.com/?apikey='+apikey+'&i='+imdb_search)
    json_object = r.json()

    #items = json_object['ID']

    #for item in json_object:
    poster = json_object['Poster']
    title = json_object['Title']
    rated = json_object['Rated']
    director = json_object['Director']
    runtime = json_object['Runtime']
    plot = json_object['Plot']
    released = json_object['Released']

    ratings = json_object['Ratings']

    for rating in ratings:
        source = rating['Source']
        value = rating['Value']

    #return json_object
    return render_template('info.html', ratings=ratings, poster=poster, title=title, rated=rated, director=director, runtime=runtime, plot=plot, released=released)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/infosearch')
def infosearch():
	return render_template('info-search.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')