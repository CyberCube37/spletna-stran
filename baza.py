import sqlite3

IME_BAZE = 'podatki.sqlite'


def ustvari_tabele():
    """ Naredi dve tabeli: Users in Scores. """
    povezava = sqlite3.connect(IME_BAZE)
    povezava.execute("DROP TABLE IF EXISTS Users")
    povezava.execute("DROP TABLE IF EXISTS Scores")
    povezava.execute("CREATE TABLE Users (username varchar(100), password varchar(100))")
    povezava.execute(
        "CREATE TABLE Scores (user_id int, napake int, beseda varchar(100))")
    povezava.commit()
    povezava.close()

def zakodiraj_geslo(password):
    """ Zakodira geslo in ga vrne """
    import hashlib, binascii
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000)
    return binascii.hexlify(dk).decode()

def dobi_najboljse():
    """ Najdi 10 iger z najmanj napakami. """
    povezava = sqlite3.connect(IME_BAZE)
    rezultat = povezava.execute("""
        SELECT Users.username, Scores.napake, Scores.beseda
        FROM Scores
        JOIN Users ON Scores.user_id=Users.rowid
        ORDER BY Scores.napake
        """)
    return rezultat.fetchmany(10)


def vstavi_novega_uporabnika(username, password):
    povezava = sqlite3.connect(IME_BAZE)
    povezava.execute(
        "INSERT INTO Users (username, password) VALUES (?, ?)",
        (username, zakodiraj_geslo(password)))
    povezava.commit()
    povezava.close()


def vstavi_novo_igro(user_id, napake, beseda):
    """ Vstavi novo igro v tabelo Scores. """
    povezava = sqlite3.connect(IME_BAZE)
    povezava.execute(
        "INSERT INTO Scores VALUES (?, ?, ?)", (user_id, napake, beseda))
    povezava.commit()
    povezava.close()

def dobi_uporabnika(user_id=None, username=None, password=None):
    povezava = sqlite3.connect(IME_BAZE)
    if user_id is not None:
        rezultat = povezava.execute("SELECT * FROM Users WHERE rowid=?", (user_id,))
    elif username is not None and password is not None:
        rezultat = povezava.execute("SELECT * FROM Users WHERE username=? and password=?", (username, zakodiraj_geslo(password)))
    elif username is not None:
        rezultat = povezava.execute("SELECT * FROM Users WHERE username=?", (username,))
    else:
        pass
    return rezultat.fetchone()

if __name__ == "__main__":
    ustvari_tabele()
    vstavi_novega_uporabnika('kirito', 'asuna')
    pov = sqlite3.connect(IME_BAZE)
    r = pov.execute("select * from Users").fetchall()
    print(r)