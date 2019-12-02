from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import requests


app = Flask(__name__)
app.secret_key = "secret key"
app.config["MONGO_URI"] = "mongodb://localhost:27017/movies"
mongo = PyMongo(app)


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

    poster = json_object['Poster']
    title = json_object['Title']
    rated = json_object['Rated']
    director = json_object['Director']
    runtime = json_object['Runtime']
    plot = json_object['Plot']
    released = json_object['Released']
    watched = 'false'

    ratings = json_object['Ratings']

    for rating in ratings:
        source = rating['Source']
        value = rating['Value']

    if request.method == 'POST':
        fav = mongo.db.userMovies.insert({'_id': id, 'title': title, 'rated': rated, 'poster': poster, 'watched': watched})
        resp = 'Added to Favourites'
        return userFavs()

    #return json_object
    return render_template('info.html', id=id, ratings=ratings, poster=poster, title=title, rated=rated, director=director, runtime=runtime, plot=plot, released=released, watched=watched)


@app.route('/delete/<id>', methods=['POST'])
def delete_movie(id):
    mongo.db.userMovies.delete_one({'_id': id})
    return userFavs()

@app.route('/watched/<id>', methods=['POST'])
def watched_movie(id):
    mongo.db.userMovies.update({'_id':id},{'$set':{'watched': 'true'}})
    return userFavs()

@app.route('/unwatch/<id>', methods=['POST'])
def unwatch_movie(id):
    mongo.db.userMovies.update({'_id':id},{'$set':{'watched': 'false'}})
    return userFavs()


@app.route('/userFavs')
def userFavs():
    favMovies = mongo.db.userMovies.find()
    return render_template('userMovies.html', favMovies=favMovies)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/infosearch')
def infosearch():
	return render_template('info-search.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')