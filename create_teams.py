
import sys
import sqlite3

year = int(sys.argv[1])

teams = []
with open('teams.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        split = line.split(' ')
        city = ' '.join(split[1:-1])
        teams.append((split[0], city, split[-1]))   

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
