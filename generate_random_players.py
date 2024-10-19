
import sys
import numpy as np
import sqlite3
import scipy

roster_size = 26

# regular position numbers except 10 is relief pitchers, 1 is starters only
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

try:
    mode = sys.argv[1]
except:
    raise ValueError('no mode specified, please choose one of: populate, create, single')

if mode not in [
    'populate',
    'create',
    'single'
] :
    raise ValueError('Invalid arg')

with open('first_names.txt') as f:
    first_names = f.readlines()

with open('last_names.txt') as f:
    last_names = f.readlines()

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
            {
            'contact': 10,
            'power': 10,
            'speed': 20,
            'catch': 50,
            'control': 50,
            'velocity': 50,
            'movement': 50,
            'eye': 10,
        }
        },
        2: {
            {
            'contact': 40,
            'power': 35,
            'speed': 25,
            'catch': 50,
            'control': 15,
            'velocity': 15,
            'movement': 15,
            'eye': 40,
        }
        },
        3: {
            {
            'contact': 60,
            'power': 70,
            'speed': 40,
            'catch': 50,
            'control': 10,
            'velocity': 10,
            'movement': 10,
            'eye': 55,
        }
        },
        4: {
            {
            'contact': 60,
            'power': 40,
            'speed': 70,
            'catch': 60,
            'control': 10,
            'velocity': 10,
            'movement': 10,
            'eye': 50,
        }
        },
        5: {
            {
            'contact': 65,
            'power': 65,
            'speed': 40,
            'catch': 55,
            'control': 10,
            'velocity': 10,
            'movement': 10,
            'eye': 60,
        }
        },
        6: {
            {
            'contact': 50,
            'power': 40,
            'speed': 80,
            'catch': 70,
            'control': 10,
            'velocity': 10,
            'movement': 10,
            'eye': 50,
        }
        },
        7: {
            {
            'contact': 70,
            'power': 70,
            'speed': 50,
            'catch': 50,
            'control': 10,
            'velocity': 15,
            'movement': 10,
            'eye': 50,
        }
        },
        8: {
            {
            'contact': 50,
            'power': 40,
            'speed': 80,
            'catch': 70,
            'control': 10,
            'velocity': 15,
            'movement': 10,
            'eye': 50,
        }
        },
        9: {
            {
            'contact': 60,
            'power': 70,
            'speed': 55,
            'catch': 60,
            'control': 10,
            'velocity': 20,
            'movement': 10,
            'eye': 50,
        }
        },
        10: {
            {
            'contact': 5,
            'power': 5,
            'speed': 5,
            'catch': 40,
            'control': 60,
            'velocity': 80,
            'movement': 70,
            'eye': 5,
        }
        },
    }

    for stat in position_stat_distros[position]:
        output[stat] = scipy.stats.truncnorm(loc = position_stat_distros[position][stat], scale = 20, a = 0, b = 100)
    
    # output = {
    #     'player_id': None,
    # }

    output['age'] = scipy.stats.truncnorm(loc = 30, scale = 3, a = 18, b = 45)
    output['team'] = team
    output['year'] = year

    if position in [2, 4, 5, 6]:
        output['handedness'] = 'Right'
    else:
        output['handedness'] = np.random.choice(['Right', 'Left'])

    con = sqlite3.connect('mlb_simulator.db')
    cur = con.cursor()

    if player_id:
        output['player_id'] = player_id
    else:
        output['player_id'] = cur.execute('SELECT MAX(player_id) FROM Players').fetchone()[0]

    return output

def insert_player(team_id, player):
    pass

con = sqlite3.connect('mlb_simulator.db')
cur = con.cursor()


if mode == 'populate':
    year = cur.execute('SELECT MAX(year) FROM Teams').fetchone()[0]
    team_ids = cur.execute(f'SELECT team_id FROM Teams WHERE year = {year}').fetchall()
    for team in team_ids:
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
            pos_to_generate[pos] = roster[pos] - cur.execute(f'SELECT COUNT(player_id) FROM Players WHERE team = {team} AND position = {pos}').fetchone()[0]

        for pos in pos_to_generate:
            for i in range(pos_to_generate[pos]):
                insert_player(team, generate_player(pos))
        
