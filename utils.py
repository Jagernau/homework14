import sqlite3

name = ['title', 'country', 'release_year', 'listed_in', 'description']

def get_db():
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        return cursor


def get_film(title):
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
    if type(first) and type(last) != int:
        first = 0
        last = 0
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



