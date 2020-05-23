from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

# проверки корректности пользовательских данных
def check_data(album_data):
    '''
    Проверки корректности пользовательских данных
    '''
    list_= ["year", "artist", "genre", "album"] # список параметров-атрибутов альбома
    message = ""
    for key in list_:
        if (album_data.get(key) is None):
            message += '\nОтсутствует {}'.format(key)
    try:
        if (int(album_data.get('year')) < 1700):
            message += '\nНекорректный год выпуска {}. Допустимые значения с 1700 года'.format(album_data.get('year'))
    except (ValueError, TypeError):
        message += '\nГод выпуска должен быть числом' if (album_data.get('year') is not None) else ''
    return message

def save_album(album_data):
    '''
    Сохраняем данные по альбому
    '''
    artist = album_data["artist"]
    album_name = album_data["album"]
    
    message = check_data(album_data)
    if message:
        message += '\nАльбом не создан!'
        result = HTTPError(400, message)
    else:
        album.save(album_data) #сохраняем альбом в базу данных
        result = "Альбом с названием {} артиста {} успешно создан".format(album_name, artist)
    return result

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Количество альбомов у артиста {}: {} <br>".format(artist, len(album_names))
        result += "Список альбомов {}: ".format(artist)
        result += "<br>".join(album_names)
    return result

@route("/albums", method="POST")
def albums():
    album_data = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    # ищем альбом с пользовательскими параметрами
    f_album = album.find_album(album_data)
    if f_album:                 # вызывается магичесский метод __bool__ класса Album
        message = "Альбом с названием {} {} года выпуска существует".format(f_album.album, f_album.year)
        result = HTTPError(409, message)
    else:
        result = save_album(album_data)
        
    return result

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
