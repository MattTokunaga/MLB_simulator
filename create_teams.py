
import sys
import sqlite3


def create_teams(year):
    teams = []
    with open('teams.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            split = line.split(', ')
            teams.append((split))   

    con = sqlite3.connect('mlb_simulator.db')
    cur = con.cursor()
    try:
        team_id_to_insert = int(cur.execute('SELECT MAX(team_id) FROM Teams').fetchone()[0]) + 1
    except:
        team_id_to_insert = 1

    for team in teams:
        cur.execute(f"INSERT INTO Teams VALUES({team_id_to_insert}, {year}, '{team[0]}', '{team[1]}', '{team[2]}')")
        con.commit()
        team_id_to_insert += 1

if __name__ == '__main__':
    year = int(sys.argv[1])
    create_teams(year)