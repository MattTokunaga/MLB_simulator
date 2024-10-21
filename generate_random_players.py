
import sys
import numpy as np
import sqlite3
import scipy
from create_teams import create_teams

roster_size = 26

# regular position numbers except 10 is relief pitchers, 1 is starters only
# based on a roster size of 26
typical_roster = {
    1: 5,
    2: 2,
    3: 2,
    4: 1,
    5: 1,
    6: 2,
    7: 2,
    8: 2,
    9: 1,
    10: 8
}

# this roster variable updates dynamically with given roster size, keeps ratios
roster = {
    1: 5,
    2: 2,
    3: 2,
    4: 1,
    5: 1,
    6: 2,
    7: 2,
    8: 2,
    9: 1,
    10: 8
}

# updates roster numbers based on given roster size
while sum(roster.values()) != roster_size:
    distances = {
        key: typical_roster[key] * roster_size / 26 - roster[key] for key in typical_roster
    }
    min_dist = min(distances.values())
    max_dist = max(distances.values())
    if np.abs(min_dist) > np.abs(max_dist):
        argmin = min(distances, key = distances.get)
        roster[argmin] -= 1
    else:
        argmax = max(distances, key = distances.get)
        roster[argmax] += 1

# ensures mode is given
try:
    mode = sys.argv[1]
except:
    raise ValueError('no mode specified, please choose one of: populate, create, single')

# ensures mode is either populate, create, or single
# populate fills teams from the most recent year until they have full rosters
# create makes teams for the most recent year + 1 then populates them
if mode not in [
    'populate',
    'create',
    'single'
] :
    raise ValueError('Invalid arg')

# function to create one random player
def generate_player(team, year, position = None, player_id = None):    
    output = {
        'player_id': None,
        'handedness': None,
        'position': None,
        'contact': None,
        'power': None,
        'speed': None,
        'catch': None,
        'team': None,
        'year': None,
        'age': None,
        'control': None,
        'velocity': None,
        'movement': None,
        'eye': None,
    }

    if position:
        pass
    else:
        position = np.random.choice(np.arange(10) + 1, p = np.array(list(roster.values())) / roster_size)
    
    output['position'] = position
    
    # constants based on how i feel
    # represent middle of the normal distribution
    position_stat_distros = {
        1: {
            'contact': 10,
            'power': 10,
            'speed': 20,
            'catch': 50,
            'control': 70,
            'velocity': 60,
            'movement': 60,
            'eye': 10,
        },
        2: {
            'contact': 40,
            'power': 35,
            'speed': 25,
            'catch': 50,
            'control': 15,
            'velocity': 15,
            'movement': 15,
            'eye': 40,
        },
        3: {
            'contact': 60,
            'power': 70,
            'speed': 40,
            'catch': 50,
            'control': 10,
            'velocity': 10,
            'movement': 10,
            'eye': 55,
        },
        4: {
            'contact': 60,
            'power': 40,
            'speed': 70,
            'catch': 60,
            'control': 10,
            'velocity': 10,
            'movement': 10,
            'eye': 50,
        },
        5: {
            'contact': 65,
            'power': 65,
            'speed': 40,
            'catch': 55,
            'control': 10,
            'velocity': 10,
            'movement': 10,
            'eye': 60,
        },
        6: {
            'contact': 50,
            'power': 40,
            'speed': 80,
            'catch': 70,
            'control': 10,
            'velocity': 10,
            'movement': 10,
            'eye': 50,
        },
        7: {
            'contact': 70,
            'power': 70,
            'speed': 50,
            'catch': 50,
            'control': 10,
            'velocity': 15,
            'movement': 10,
            'eye': 50,
        },
        8: {
            'contact': 50,
            'power': 40,
            'speed': 80,
            'catch': 70,
            'control': 10,
            'velocity': 15,
            'movement': 10,
            'eye': 50,
        },
        9: {
            'contact': 60,
            'power': 70,
            'speed': 55,
            'catch': 60,
            'control': 10,
            'velocity': 20,
            'movement': 10,
            'eye': 50,
        },
        10: {
            'contact': 5,
            'power': 5,
            'speed': 5,
            'catch': 40,
            'control': 60,
            'velocity': 80,
            'movement': 70,
            'eye': 5,
        },
    }

    distro_scale = 20
    for stat in position_stat_distros[position]:
        mid = position_stat_distros[position][stat]
        output[stat] = np.round(scipy.stats.truncnorm(loc = mid, scale = distro_scale, a = -mid/distro_scale , b = (100 - mid)/distro_scale).rvs())
    
    # output = {
    #     'player_id': None,
    # }

    output['age'] = np.round(scipy.stats.truncnorm(-4, 5, loc = 30, scale = 3).rvs())
    output['team'] = team
    output['year'] = year

    if position in [2, 4, 5, 6]:
        output['handedness'] = 'RIGHT'
    else:
        output['handedness'] = np.random.choice(['RIGHT', 'LEFT'])

    con = sqlite3.connect('mlb_simulator.db')
    cur = con.cursor()

    if player_id:
        if cur.execute('SELECT player_id FROM Players WHERE player_id = ?', [player_id]).fetchone():
            raise ValueError('Player ID already exists')
        output['player_id'] = player_id
    else:
        max_player_id = cur.execute('SELECT MAX(player_id) FROM Players').fetchone()[0]
        if max_player_id:
            output['player_id'] = max_player_id + 1
        else:
            output['player_id'] = 1

    

    if np.random.rand() <= 0.005:
        with open('active_players.txt', 'r') as f:
            names = f.readlines()
        name = np.random.choice(names)
        output['first_name'] = name.split(' ')[0]
        output['last_name'] = ' '.join(name.split(' ')[1:]) + ' Jr.'
    else:
        with open('first_names.txt', 'r') as fn:
            firsts = fn.readlines()
        output['first_name'] = np.random.choice(firsts)
        with open('last_names.txt', 'r') as ln:
            lasts = ln.readlines()
        output['last_name'] = np.random.choice(lasts)

    return output

# function to insert player into database
def insert_player(player):
    to_insert = [
        player['player_id'],
        player['handedness'],
        player['position'],
        player['contact'],
        player['power'],
        player['speed'],
        player['catch'],
        player['team'],
        player['year'],
        player['age'],
        player['control'],
        player['velocity'],
        player['movement'],
        player['eye'],
        player['first_name'],
        player['last_name'],
    ]
    con = sqlite3.connect('mlb_simulator.db')
    cur = con.cursor()
    cur.execute(f"INSERT INTO Players VALUES(?, ?, ?, ?, ?, ?, ? , ?, ?, ?, ?, ?, ?, ?, ? ,?)", to_insert)
    con.commit()
    return True


def populate(roster, verbose = False):
    con = sqlite3.connect('mlb_simulator.db')
    cur = con.cursor()
    year = cur.execute('SELECT MAX(year) FROM Teams').fetchone()[0]
    team_ids = cur.execute(f'SELECT team_id FROM Teams WHERE year = {year}').fetchall()
    for team in team_ids:
        team = team[0]
        pos_to_generate = {
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0,
                6: 0,
                7: 0,
                8: 0,
                9: 0,
                10: 0
            }
        for pos in roster:
            pos_to_generate[pos] = roster[pos] - cur.execute(f'SELECT COUNT(player_id) FROM Players WHERE team = ? AND position = ?', [team, pos]).fetchone()[0]

        for pos in pos_to_generate:
            for i in range(pos_to_generate[pos]):
                insert_player(generate_player(team, year, pos))
        if verbose:
            print(f'Finished populating {team}')
    

if mode == 'populate':
    populate(roster)
        
if mode == 'create':
    con = sqlite3.connect('mlb_simulator.db')
    cur = con.cursor()
    year = cur.execute('SELECT MAX(year) FROM Teams').fetchone()
    if year:
        year = year[0] + 1
    else:
        year = 1
    create_teams(year)
    populate(roster, True)

if mode == 'single':
    print("not implemented yet")