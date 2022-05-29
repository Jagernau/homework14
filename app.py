from flask import Flask, jsonify, request
import utils


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


#вьюшки
@app.route("/movie/<title>")#1
def film_from_title(title):
    """страница с данными про искомый фильм"""
    one_film = utils.get_film(title) 
    return jsonify(one_film)


@app.route("/genre/<genre>")#4
def film_from_genre(genre):
    """страница отдающая фильмы по жанру"""
    films = utils.get_genre(genre)
    return jsonify(films)


@app.route("/movie/year/to/year")#2
def film_from_detween_years():
    """страницы фильмов между годами"""
    first = request.args.get("first")
    last = request.args.get("last")
    year_to_year = utils.get_years(first,last)
    return jsonify(year_to_year)


@app.route("/rating/<choice>")#3
def films_children(choice):
    """страница с детскими фильмами"""
    film = []
    if choice == "children":
        film = utils.get_rating("G")
    if choice == "family":
        film = utils.get_rating("G", "PG", "PG-13")
    return jsonify(film)

if __name__ == "__main__":
    app.run()

