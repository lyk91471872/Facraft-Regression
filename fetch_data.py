import numpy as np
import sqlite3

def fetch_data(player='all_players'):
    conn = sqlite3.connect('records.db')
    cursor = conn.cursor()
    if player=='all_players':
        condition = ''
    else:
        condition = ' where player==\'' + player + '\''
    fps = np.array([[_[0]] for _ in cursor.execute('select fps from records' + condition).fetchall()])
    score = np.array([_[0] for _ in cursor.execute('select score from records' + condition).fetchall()])
    cursor.close()
    conn.close()
    return fps, score
