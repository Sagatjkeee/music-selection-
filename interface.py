import sqlite3
import subprocess

def player(link):
    vlc_path = r'X:\VLC\vlc.exe'
    subprocess.Popen([vlc_path, link])
def choose_genre():
    choose_genre = input('Choose your genre:\n Rap -  1 \n Rock - 2\n I will choose: ')

    if choose_genre == '1':
        choose_genre = 'Rap'
    if choose_genre == '2':
        choose_genre = 'Rock'
    return choose_genre

choose_genre = choose_genre()

#def connect():
#    with sqlite3.connect('laba.db') as db:
#        cursor = db.cursor()
#    #return cursor
#    #connect = sqlite3.connect('laba.db')
#    #cursor = connect.cursor()
#    return cursor
#cursor = connect()

def find_length(choose_genre):
    with sqlite3.connect('laba.db') as db:
        cursor = db.cursor()
        result = f"SELECT COUNT(*) FROM kik WHERE Winner = 'True' AND Genre = '{choose_genre}'"
        cursor.execute(result)
        length = cursor.fetchone()
        length = length[0]
        length = int(length)
        #print('Длина в функции - ', length)
        return length

lenght = find_length(choose_genre)

def battle(lenght):
    connect = sqlite3.connect('laba.db')
    cursor = connect.cursor()
    off = 0
    for i in range(lenght):  # длина трушных в выбранном жанре
        query = f"SELECT * FROM kik WHERE Genre = '{choose_genre}' AND Winner = 'True' LIMIT {off}, 2"  # LIMIT - скок надо OFFSET - скок пропустить # нужно сбрасывать off и менять длину строк( по -2 за ход)
        cursor.execute(query)
        connect.commit()
        result1 = cursor.fetchone()  # выбераем 1ю запись из списка
        result2 = cursor.fetchone()
        if result2 is None:
            print("Победитель", result1)
            break
        # result2 = cursor.fetchmany(1) # выбираем нужное кол-во записей из списка
        player(result1[3])
        player(result2[3])
        s1 = len(result1[1])
        s2 = len(result2[1])
        if s1 > s2:
            lenn = s1
        else:
            lenn = s2
        choose_loser = input('Выберите исполнителя:\n' + result1[1].rjust(lenn, " ") + ' - 1\n' + result2[1].rjust(lenn, " ") + ' - 2\nЯ выбираю: ')

        if choose_loser == '1':
            id_loser = result2[0]
            id_winner = result1[0]
        else:
            id_loser = result1[0]
            id_winner = result2[0]
        off += 1
        lenght -= 2
        query = f"UPDATE kik SET winner = 'False' WHERE ID = {id_loser}"
        cursor.execute(query)
        query = f"UPDATE kik SET winner = 'True' WHERE ID = {id_winner}"
        cursor.execute(query)
        #print("Счётчик - ", i)
        #print("Lenght - ", lenght)
        #print("OFF", off)
        #print("ФИНИШ")
        connect.commit()
        if lenght == 0:
            lenght = find_length(choose_genre)
            off = 0

battle(lenght)
with sqlite3.connect('laba.db') as db:
    cursor = db.cursor()
    query = """ SELECT * FROM kik """
    cursor.execute(query)
    for i in cursor:
        print(i)

