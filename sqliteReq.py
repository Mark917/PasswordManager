import sqlite3

conn = sqlite3.connect('database.db')

def Inserisci(Servizio, Nickname, Email, Passkey):
    conn = sqlite3.connect('database.db')
    account = conn.execute('SELECT * FROM Password').fetchall()
    conn.execute('INSERT INTO Password (Servizio, Nickname, Email, Passkey) VALUES (?, ?, ?, ?)', (Servizio, Nickname, Email, Passkey))
    conn.commit()
    conn.close()

def PrendiDati(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Servizio, Nickname, Email, passkey FROM Password WHERE id = ?", (id,))
    dettagli = cursor.fetchall()
    return dettagli
    conn.close()

def PrendiDatiServizi():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Servizio, id FROM Password")
    Servizi = cursor.fetchall()
    conn.commit()
    conn.close()
    return Servizi

def Elimina(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Password WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def Modifica(colonna, newDato, id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    AggiornaDato = f"UPDATE Password SET {colonna} = ? WHERE id = ?"
    cursor.execute(AggiornaDato, (newDato, id))
    conn.commit()
    conn.close()