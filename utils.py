import sqlite3
from json import dumps

name = ['title', 'country', 'release_year', 'listed_in', 'description', 'rating']

def get_db():
    """курсор sqlite базы"""
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        return cursor


def get_film(title):
    """выводит фильм по названию"""
    cur = get_db()
    arg = f"""
        SELECT {name[0]}, {name[1]}, {name[2]}, {name[3]}, {name[4]}
        FROM 'netflix'
        WHERE title = '{str(title)}'
        ORDER BY release_year DESC
        LIMIT 1
    """
    cur.execute(arg)
    film = cur.fetchall()
    js = {}
    if len(film) > 0:
        for i in range(5):
            js[name[i]]=film[0][i]
             
        return js
    return js
    

def get_genre(genre):
    """выводит фильмы по жанру"""
    cur = get_db()
    arg = f"""
        SELECT {name[0]}, {name[4]}
        FROM 'netflix'
        WHERE type = 'Movie'
        AND listed_in = '{str(genre)}' OR listed_in = '{str(genre)}%'
        ORDER BY release_year DESC
        LIMIT 10
    """
    cur.execute(arg)
    films = cur.fetchall()
    js = []
    if len(films) > 0:
        for i in films:
            js.append({name[0]:i[0],name[4]:i[1].strip("\n")})
        return js
    return js


def get_years(first,last):
    """выводит фильмы от first до last"""
    if first  == None:
        first = 1900
    if last == None:
        last = 2022
    cur = get_db()
    arg = f"""
        SELECT {name[0]}, {name[2]}
        FROM 'netflix'
        WHERE {name[2]} BETWEEN {first} AND {last}
        AND type = 'Movie'
        ORDER BY {name[2]}
        LIMIT 100
    """
    cur.execute(arg)
    films = cur.fetchall()
    js = []
    if len(films) > 0:
        for i in films:
            js.append({name[0]:i[0],name[2]:i[1]})
        return js
    return js


def get_rating(*ratings):
    """выводит фильмы по рейтингу"""
    rat = len(ratings)
    cur = get_db()
    if rat > 1:
        arg = f"""
            SELECT {name[0]}, {name[5]}, {name[4]}
            FROM 'netflix'
            WHERE {name[5]} IN {ratings}
            AND type = 'Movie'
        """
    else:
        arg = f"""
            SELECT {name[0]}, {name[5]}, {name[4]}
            FROM 'netflix'
            WHERE {name[5]} = '{ratings[0]}'
            AND type = 'Movie'
        """
            
    cur.execute(arg)
    films = cur.fetchall()
    js = []
    if len(films) > 0:
        for i in films:
            js.append({name[0]:i[0], name[5]:i[1], name[4]:i[2]})
        return js
    return films
print(get_rating("G"))

#шаг 5 функция с 2 актёрами
def get_actors(one_actor,two_actor):
    cur = get_db()
    arg = f"""
        SELECT DISTINCT netflix.cast
        FROM 'netflix'
        WHERE netflix.cast LIKE '%{one_actor}%{two_actor}%'

    """
    cur.execute(arg)
    actors = cur.fetchall()
    unic = set()
    allin = list()
    bro=list()
    for i in actors:
        actor = i[0].split(", ")
        for x in actor:
            unic.add(x)
            allin.append(x)
    for i in unic:
        if allin.count(i) > 2 and i != one_actor and i != two_actor:
            bro.append(i)
    return bro
    
#print(get_actors("Rose McIver", "Ben Lamb"))


#шаг 6 функция принимающая 3и аргумента тип, год, жанр
def sorting(type_, year_, genre_):
    """функция возвращает фильмы по типу году и жанру в json"""
    cur = get_db()
    arg = f"""
        SELECT {name[0]}, {name[4]} 
        FROM 'netflix'
        WHERE type = '{type_}' AND release_year = '{year_}' AND listed_in = '{genre_}'

    """
    cur.execute(arg)
    result = cur.fetchall()
    films = []
    if len(result) > 0:
        for i in result:
            films.append({name[0]: i[0], name[4]: i[1].rstrip("\n")})
        return dumps(films, indent=3)
    return dumps(films, indent=3)

#print(sorting("Movie", 1980, "Dramas"))



