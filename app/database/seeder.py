'''
Solo se ejecuta para crear la primera vez la Bd
'''
import sqlite3 as sql

DB_PATH = "F:\CartografiasSonoraServer\app\database\DbCarto.db"


def createDB():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE posiciones (
                   latitude real,
                   longitude real,
                   name text,
                   date text,
                   time text,
                   audio_name text
                   )"""
    )
    conn.commit()
    conn.close()


def addValues():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    data = [
        (43.360870938239664, -5.5092986378873094, "L'Argamusu", "20/03/2025", "14:25", "hola.wav"),
        (45334555, 675756, "Nava", "21/03/2025", "12:00", "cucuc.wav"),
        (4533333, 666666, "La Texuca", "01/12/2023", "21:00", "aaaa.wav"),
        (1111111, 11112222, "Bocarral", "13/01/2024", "01:25", "bbbbb.wav"),
    ]
    cursor.executemany('''INSERT INTO posiciones VALUES (?, ?, ?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()


if __name__ == "__main__":
   createDB()
   addValues()
