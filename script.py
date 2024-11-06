import sqlite3
import numpy as np
import calendar
from datetime import date
from datetime import timedelta
import pandas as pd
import copy
import json

current_year = 2025
number_of_teams = 0

teams = []
with open('teams.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        split = line.split(' ')
        teams.append((split[0], split[1], split[2]))        

#region <failed attempts to generate schedule>
# def generate_schedule(year, teams):
#     output = {}
    
#     # separate the division
#     divisions = {}
#     divisions_inverse = {}
#     for team in teams:
#         if team[2] in divisions:
#             divisions[team[2]].append(team[0])
#         else:
#             divisions[team[2]] = [team[0]]
#         divisions_inverse[team[0]] = team[2]
    

#     # create list of team names sorted alphabetically
#     team_names = sorted([team[0] for team in teams])

#     # designate one team in the opposing league to be the interleague rival
#     # would usually be designated matchups like yankees-mets, giants-as, etc
#     # just picks one in the counterpart division (al east with nl east, etc)
#     interleague_rivals = {}
#     for team in teams:
#         team_name = team[0]
#         if team_name in interleague_rivals:
#             continue
#         else:
#             if team[2][0] == "n":
#                 counterpart = "a" + team[2][1:]
#             else:
#                 counterpart = "n" + team[2][1:]
#             rival = np.random.choice(divisions[counterpart])
#             while rival in interleague_rivals:
#                 rival = np.random.choice(divisions[counterpart])
#             interleague_rivals[team_name] = rival
#             interleague_rivals[rival] = team_name

#     # creates all series so that they can be placed in the schedule later
#     # format: (home, away, number of games, series no.)
#     series_list = []

#     # decides who will be the home team in certain series
#     # if true, the alphabetically first team will be home team
#     home_first = year % 2 == 0

#     # randomizes the division order, this is used to create four game series in intraleague
#     random_divs = {}
#     for division in divisions:
#         random_divs[division] = np.random.choice(divisions[division], 5, replace=False)
#     # print(random_divs)

#     # dictionary defining relationships between divisions, used to create foru game series in intraleague
#     div_relations = {
#         0: "west",
#         1: "central",
#         2: "east",
#         "west": 0,
#         "central": 1,
#         "east": 2
#     }

#     for team_tup in teams:
#         team = team_tup[0]
#         # interleague rival games
#         series_list.append((team, interleague_rivals[team], 2, 1))
#         series_list.append((interleague_rivals[team], team, 2, 1))

#         # division games
#         for div_rival in divisions[team_tup[2]]:
#             if div_rival == team:
#                 continue
#             two_teams = sorted([team, div_rival])
#             if home_first:
#                 pass
#             else:
#                 two_teams = two_teams[::-1]
#             series_list.append((two_teams[0], two_teams[1], 4, 1))
#             series_list.append((two_teams[0], two_teams[1], 3, 1))
#             series_list.append((two_teams[1], two_teams[0], 3, 1))
#             series_list.append((two_teams[1], two_teams[0], 3, 2))

#         # intraleague

#         # logic to handle random four game series
#         div_pos = sum([i if random_divs[team_tup[2]][i] == team else 0 for i in [0, 1, 2, 3, 4]])
#         league = team_tup[2][:2]
#         four_game_intra_teams = [
#             random_divs[league + div_relations[(div_relations[team_tup[2][2:]] + 1) % 3]][div_pos],
#             random_divs[league + div_relations[(div_relations[team_tup[2][2:]] + 2) % 3]][div_pos],
#             random_divs[league + div_relations[(div_relations[team_tup[2][2:]] + 1) % 3]][(div_pos - 1) % 5],
#             random_divs[league + div_relations[(div_relations[team_tup[2][2:]] - 1) % 3]][(div_pos + 1) % 5]
#         ]

#         # records all intraleague teams that still need to have series scheduled against
#         remaining_intraleague = list(filter(lambda x: x[2][:2] == league, teams))
#         remaining_intraleague = list(map(lambda x: x[0], remaining_intraleague))
#         remaining_intraleague.remove(team)

#         # adds 3 and 4 game series against teams that they play a 4 game series against
#         for four_game_rival in four_game_intra_teams:
#             two_teams = sorted([team, four_game_rival])
#             if home_first:
#                 pass
#             else:
#                 two_teams = two_teams[::-1]
#             series_list.append((two_teams[0], two_teams[1], 4, 1))
#             series_list.append((two_teams[1], two_teams[0], 3, 1))
#             remaining_intraleague.remove(four_game_rival)
        
#         # adds two three game series for all the other intraleague teams
#         for remaining_team in remaining_intraleague:
#             series_list.append((remaining_team, team, 3, 1))
#             series_list.append((team, remaining_team, 3, 1))

#         # interleague
#         # removes interleague rival from list, already played them
#         remaining_interleague = list(filter(lambda x: x[2][:2] != league, teams))
#         remaining_interleague = list(map(lambda x: x[0], remaining_interleague))
#         remaining_interleague.remove(interleague_rivals[team])

#         # adds three game series against the rest of the interleague teams
#         for remaining_team in remaining_interleague:
#             two_teams = sorted([team, remaining_team])
#             if home_first:
#                 pass
#             else:
#                 two_teams = two_teams[::-1]
#             series_list.append((two_teams[0], two_teams[1], 3, 1))

    
#     # series list includes repeats, collapses it down to unique series
#     series_set = set(series_list)

#     # find the third tuesday of march to start the season on
#     month = 3
#     cal = calendar.monthcalendar(year, month)
#     tuesdays = 0
#     for week in cal:
#         if week[calendar.TUESDAY] != 0:
#             tuesdays += 1
#             if tuesdays == 3:
#                 third_tuesday = date(year, month, week[calendar.TUESDAY])
    
#     # find the second tuesday of july to have the all star break
#     all_star_month = 7
#     cal = calendar.monthcalendar(year, all_star_month)
#     tuesdays = 0
#     for week in cal:
#         if week[calendar.TUESDAY] != 0:
#             tuesdays += 1
#             if tuesdays == 3:
#                 all_star_tuesday = date(year, all_star_month, week[calendar.TUESDAY])
#                 all_star_friday = all_star_tuesday + timedelta(days = 3)

#     # creates list of dates that three and four game series can start on
#     weekday_dates = []
#     weekend_dates = []
#     for i in range(27):
#         weekday_dates.append(third_tuesday + timedelta(days = 7*i))
#         weekend_dates.append(third_tuesday + timedelta(days = 3 + 7*i))
    
#     weekday_dates.remove(all_star_tuesday)
#     weekend_dates.remove(all_star_friday)

#     # weekday and weekend series for each team
#     team_split_schedules = {}
#     for team_tup in teams:
#         team_split_schedules[team_tup[0]] = [[], []]

#     series_randomized_list = np.random.permutation(list(series_set))

#     # for series in series_randomized_list:
#     #     if int(series[2]) == 4:
#     #         team_split_schedules[series[0]][1].append(series)
#     #         team_split_schedules[series[1]][1].append(series)
#     #     elif int(series[2]) == 2:
#     #         team_split_schedules[series[0]][1].append(series)
#     #         team_split_schedules[series[1]][1].append(series)
#     #     else:
#     #         if divisions_inverse[series[0]][2:] == divisions_inverse[series[1]][2:]:
#     #             team_split_schedules[series[0]][1].append(series)
#     #             team_split_schedules[series[1]][1].append(series)
#     #         else:
#     #             team_split_schedules[series[0]][0].append(series)
#     #             team_split_schedules[series[1]][0].append(series)

#     threes_dict = {}
#     fours_dict = {}
#     for ser in series_set:
#         sorted_teams = tuple(sorted([ser[0], ser[1]]))
#         if int(ser[2]) == 4:
#             if sorted_teams in fours_dict:
#                 fours_dict[sorted_teams] += 1
#             else:
#                 fours_dict[sorted_teams] = 1
#             continue
#         if sorted_teams in threes_dict:
#             threes_dict[sorted_teams] += 1
#         else:
#             threes_dict[sorted_teams] = 1

    
#     team_day_dicts = {}
#     for team in team_names:
#         team_day_dicts[team] = {}
#     counter = 0
#     for team in team_names:
#         team_fours = list(filter(lambda x:(x[0] == team or x[1] == team) and int(x[2]) == 4, series_set))
#         team_threes = list(filter(lambda x:(x[0] == team or x[1] == team) and int(x[2]) != 4, series_set))
#         for preexisting_ser in team_day_dicts[team].values():
#             if int(preexisting_ser[2]) == 4:
#                 if preexisting_ser[0] == "Angels" or preexisting_ser[1] == "Angels":
#                     if team != "Angels":
#                         print(preexisting_ser, team)
#                 team_fours.remove(preexisting_ser)
#             else:
#                 team_threes.remove(preexisting_ser)
#         if team == "Mariners":
#             print(team_day_dicts[team].values())
#             print(("Angels", "Mariners", 4, 1) in team_day_dicts[team].values())
#             # print(team_day_dicts[team].values())
#         randomized_dates = np.random.choice(weekend_dates, len(weekend_dates), replace=False)
#         for day in randomized_dates:
#             daily_fours = list(filter(lambda x: (day not in team_day_dicts[x[0]]) and (day not in team_day_dicts[x[1]]), team_fours))
#             print(daily_fours)
#             if day in team_day_dicts[team].keys():
#                 pass
#             else:
#                 if len(team_fours) > 0:

#                     to_insert = daily_fours[np.random.choice(range(len(daily_fours)))]
#                     team_fours.remove(to_insert)
#                     team_day_dicts[to_insert[0]][day] = to_insert
#                     team_day_dicts[to_insert[1]][day] = to_insert
#                     if to_insert == ("Angels", "Mariners", 4, 1):
#                         print(team_day_dicts["Mariners"].values())
#                 else:
#                     to_insert = team_threes[np.random.choice(range(len(team_threes)))]
#                     team_threes.remove(to_insert)
#                     team_day_dicts[to_insert[0]][day] = to_insert
#                     team_day_dicts[to_insert[1]][day] = to_insert
#                     counter += 1
#         for day in np.random.choice(weekday_dates, len(weekday_dates), replace= False):
#             if day in team_day_dicts[team]:
#                 pass
#             else:
#                 to_insert = team_threes[np.random.choice(range(len(team_threes)))]
#                 team_threes.remove(to_insert)
#                 team_day_dicts[to_insert[0]][day] = to_insert
#                 team_day_dicts[to_insert[1]][day] = to_insert


#     # for day in weekday_dates:
#     #     output[day] = []
#     #     possible_pairs = list(filter(lambda x: threes_dict[x] != 0, threes_dict.keys()))
#     #     pair_count = 0
#     #     paired_teams = []
#     #     while pair_count < 15:
#     #         possible_pairs = list(filter(lambda x:threes_dict[x] != 0 and x[0] not in paired_teams and x[1] not in paired_teams, threes_dict.keys()))

#     #         pair = possible_pairs[np.random.choice(range(len(possible_pairs)))]

#     #         valid_series = list(filter(lambda x: (x[0] == pair[0] or x[0] == pair[1]) and (x[1] == pair[0] or x[1] == pair[1]) and (int(x[2]) != 4), series_set))

#     #         series_to_schedule = valid_series[np.random.choice(range(len(valid_series)))]

#     #         paired_teams.append(pair[0])
#     #         paired_teams.append(pair[1])
#     #         output[day].append(series_to_schedule)
#     #         pair_count += 1
#     #         threes_dict[tuple(sorted(pair))] -= 1
        

#     # for day in weekend_dates:
#     #     output[day] = []
#     #     possible_pairs1 = list(filter(lambda x: threes_dict[x] != 0, threes_dict.keys()))
#     #     possible_pairs2 = list(filter(lambda x: fours_dict[x] != 0, fours_dict.keys()))
#     #     possible_pairs = possible_pairs1 + possible_pairs2
#     #     pair_count = 0
#     #     paired_teams = []
#     #     while pair_count < 15:
#     #         possible_pairs1 = list(filter(lambda x:fours_dict[x] != 0 and x[0] not in paired_teams and x[1] not in paired_teams, fours_dict.keys()))
#     #         possible_pairs2 = list(filter(lambda x:threes_dict[x] != 0 and x[0] not in paired_teams and x[1] not in paired_teams, threes_dict.keys()))
#     #         possible_pairs = possible_pairs1 + possible_pairs2
#     #         pair = possible_pairs[np.random.choice(range(len(possible_pairs)))]
#     #         valid_series = list(filter(lambda x: (x[0] == pair[0] or x[0] == pair[1]) and (x[1] == pair[0] or x[1] == pair[1]), series_set))
            
#     #         series_to_schedule = valid_series[np.random.choice(range(len(valid_series)))]

#     #         paired_teams.append(pair[0])
#     #         paired_teams.append(pair[1])
#     #         output[day].append(series_to_schedule)
#     #         pair_count += 1
#     #         if int(series_to_schedule[2]) == 4:
#     #             fours_dict[tuple(sorted(pair))] -= 1
#     #         else:
#     #             fours_dict[tuple(sorted(pair))] -= 1

#     return team_day_dicts
#endregion

def clear_table(table_name):
    con = sqlite3.connect("mlb_simulator.db")
    cur = con.cursor()
    try:
        cur.execute(f"DELETE FROM {table_name}")
    except:
        print('Error: probably a nonexistent table')

def insert_into_table(table, to_insert):
    num_to_add = len(to_insert)
    con = sqlite3.connect("mlb_simulator.db")
    cur = con.cursor()
    if type(to_insert) == tuple:
        to_insert = list(to_insert)
    elif type(to_insert) != list:
        raise ValueError('to_insert is neither a list nor a tuple')
    insert_string = 'INSERT INTO '+ table +' VALUES (' + "?,"*(num_to_add-1) + '?)'
    cur.execute(insert_string, to_insert)
    con.commit()

# function to generate a schedule
def generate_schedule(year, teams):
    # define output dictionary
    generated_schedule = {}

    # open the schudule template that was made from 2023 season
    with open('schedule_template.json') as json_file:
        sched_template_dict = json.load(json_file)

    # define team dictionary to turn the numbers in the template into teamss
    team_dict = {}
    for i in range(1, 31):
        team_dict[i] = teams[i-1][1] +' '+ teams[i-1][0]        
    shuffled_nums = []
    for i in range(len(teams) // 5):
        shuffled_nums += list(np.random.choice(range(5*i + 1, 5*i + 6), 5, replace = False))
    shuffled_nums_dic = {}
    for i in range(30):
        shuffled_nums_dic[i + 1] = shuffled_nums[i]

    # find the third tuesday of march to start the season on
    month = 3
    cal = calendar.monthcalendar(year, month)
    tuesdays = 0
    for week in cal:
        if week[calendar.TUESDAY] != 0:
            tuesdays += 1
            if tuesdays == 3:
                third_tuesday = date(year, month, week[calendar.TUESDAY])

    # shuffles the numbers in the template
    for day in sched_template_dict:
        generated_schedule[third_tuesday + timedelta(int(day))] = [(shuffled_nums_dic[game[0]], shuffled_nums_dic[game[1]]) for game in sched_template_dict[day]]
    
    # replaces numbers with teams
    for date_key in generated_schedule:
        generated_schedule[date_key] = [(team_dict[game[0]], team_dict[game[1]]) for game in generated_schedule[date_key]]

    # return the generated schedule
    return generated_schedule

def simulate_pitch(pa_constants, pitch_id, pitcher_id, batter_id):
    # SIMULATE PITCH FUNCTION
    # takes in pitcher stats and batter stats in the form of a dictionary:

    # FOR PITCHERS:
    # 'handedness'
    # 'control'
    # 'velocity'
    # 'movement'

    # FOR BATTERS:
    # 'handedness'
    # 'contact'
    # 'power'
    # 'speed'
    # 'eye'

    # defines variables to be inserted into database row
    swinging_strike_insert = 0
    ball_insert = 0
    foul_insert = 0
    in_play_insert = 0
    called_strike_insert = 0
    hit_by_pitch_insert = 0
    is_fastball = False
    is_strike = False
    swing = False
    contact = False


    def rand_sim(situation):
        if np.random.rand() <= pa_constants[situation]:
            return True
        else:
            return False
        
    # def insert_pitch_into_database():
    #     con = sqlite3.connect("mlb_simulator.db")
    #     cur = con.cursor()
    #     to_insert = [
    #         pitch_id,
    #         pitcher_id,
    #         batter_id,
    #         swinging_strike_insert,
    #         ball_insert,
    #         called_strike_insert,
    #         foul_insert,
    #         in_play_insert,
    #         hit_by_pitch_insert,
    #         int(is_fastball),
    #         int(is_strike),
    #         int(swing),
    #         int(contact)
    #     ]
    #     cur.execute('INSERT INTO Pitches VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', to_insert)
    #     con.commit()

    if rand_sim('hit_by_pitch_chance'):
        if np.random.choice([1, 2, 3]) == 1:
            is_fastball = False
        else:
            is_fastball = True
        hit_by_pitch_insert = 1
        to_insert = [
            pitch_id,
            pitcher_id,
            batter_id,
            swinging_strike_insert,
            ball_insert,
            called_strike_insert,
            foul_insert,
            in_play_insert,
            hit_by_pitch_insert,
            int(is_fastball),
            int(is_strike),
            int(swing),
            int(contact)
        ]
        insert_into_table('Pitches', to_insert)
        return 'Hit by pitch'

    is_fastball = rand_sim('fastball_chance')
    
    if is_fastball:
        is_strike = rand_sim('fastball_strike_chance')
    else:
        is_strike = rand_sim('non_fastball_strike_chance')

    if is_strike:
        if is_fastball:
            swing = rand_sim('fastball_strike_swing_chance')
        else:
            swing = rand_sim('non_fastball_strike_swing_chance')
    else:
        if is_fastball:
            swing = rand_sim('fastball_ball_swing_chance')
        else:
            swing = rand_sim('non_fastball_ball_swing_chance')
    
    if not swing:
        if is_strike:
            called_strike_insert = 1
            to_insert = [
                pitch_id,
                pitcher_id,
                batter_id,
                swinging_strike_insert,
                ball_insert,
                called_strike_insert,
                foul_insert,
                in_play_insert,
                hit_by_pitch_insert,
                int(is_fastball),
                int(is_strike),
                int(swing),
                int(contact)
            ]
            insert_into_table('Pitches', to_insert)
            return 'Called strike'
        else:
            ball_insert = 1
            to_insert = [
                pitch_id,
                pitcher_id,
                batter_id,
                swinging_strike_insert,
                ball_insert,
                called_strike_insert,
                foul_insert,
                in_play_insert,
                hit_by_pitch_insert,
                int(is_fastball),
                int(is_strike),
                int(swing),
                int(contact)
            ]
            insert_into_table('Pitches', to_insert)
            return 'Ball'


    if is_fastball:
        if is_strike:
            contact = rand_sim('fastball_strike_contact_chance')
        else:
            contact = rand_sim('fastball_ball_contact_chance')
    else:
        if is_strike:
            contact = rand_sim('non_fastball_strike_contact_chance')
        else:
            contact = rand_sim('non_fastball_ball_contact_chance')
    
    if not contact:
        swinging_strike_insert = 1
        to_insert = [
            pitch_id,
            pitcher_id,
            batter_id,
            swinging_strike_insert,
            ball_insert,
            called_strike_insert,
            foul_insert,
            in_play_insert,
            hit_by_pitch_insert,
            int(is_fastball),
            int(is_strike),
            int(swing),
            int(contact)
        ]
        insert_into_table('Pitches', to_insert)
        return 'Swinging strike'
    
    if is_fastball:
        if is_strike:
            foul = rand_sim('fastball_strike_foul_chance')
        else:
            foul = rand_sim('fastball_ball_foul_chance')
    else:
        if is_strike:
            foul = rand_sim('non_fastball_strike_foul_chance')
        else:
            foul = rand_sim('non_fastball_ball_foul_chance')
    
    if foul:
        foul_insert = 1
        to_insert = [
            pitch_id,
            pitcher_id,
            batter_id,
            swinging_strike_insert,
            ball_insert,
            called_strike_insert,
            foul_insert,
            in_play_insert,
            hit_by_pitch_insert,
            int(is_fastball),
            int(is_strike),
            int(swing),
            int(contact)
        ]
        insert_into_table('Pitches', to_insert)
        return 'Foul'
    else:
        in_play_insert = 1
        to_insert = [
            pitch_id,
            pitcher_id,
            batter_id,
            swinging_strike_insert,
            ball_insert,
            called_strike_insert,
            foul_insert,
            in_play_insert,
            hit_by_pitch_insert,
            int(is_fastball),
            int(is_strike),
            int(swing),
            int(contact)
        ]
        insert_into_table('Pitches', to_insert)
        return 'In play'
    

def simulate_plate_appearance(pitcher_stats, batter_stats, situation, plate_app_id):
    # constants based on statcast data and my own judgement
    # statcast zones were used with heart and shadow being considered strikes, else balls
    base_pa_constants = {
        'hit_by_pitch_chance': 0.003, # hbp / total pitches
        'fastball_chance': 0.56, # fastballs / total pitches
        'fastball_strike_chance': 0.65, # fastball strikes / total fastballs
        'non_fastball_strike_chance': 0.5, # non fastball strikes / total non fastballs
        'fastball_strike_swing_chance': 0.8, # fastball strike swings / total fastball strikes
        'non_fastball_strike_swing_chance': 0.7, # non fastball strike swings / total non fastball strikes
        'fastball_ball_swing_chance': 0.2, # fastball ball swings / total fastball balls
        'non_fastball_ball_swing_chance': 0.25, # non fastball ball swings / total non fastball balls
        'fastball_strike_contact_chance': 0.85, # fastball strike contacts / total fastball strike swings
        'non_fastball_strike_contact_chance': 0.8, # non fastball strike contacts / total non fastball strike swings
        'fastball_ball_contact_chance': 0.75, # fastball ball contacts / total ball strike swings
        'non_fastball_ball_contact_chance': 0.65, # non fastball ball contacts / total non fastball ball swings
        'fastball_strike_foul_chance': 0.55, # fastball strike fouls / total fastball strike contacts
        'non_fastball_strike_foul_chance': 0.5, # non fastball strike fouls / total non fastball strike contacts
        'fastball_ball_foul_chance': 0.7, # fastball ball fouls / total fastball ball contacts
        'non_fastball_ball_foul_chance': 0.6 # non fastball ball fouls / total non fastball ball contacts
    }

    # input 0 to 100
    # uses cos curve for stat benefits
    def adjust_base(base, input, higher_stat_higher_rate):
        scale = 1/10
        dist = min(np.abs(base - 1), base)
        if higher_stat_higher_rate:
            pass
        else: 
            input = 100 - input
        return scale * dist * np.cos(np.pi / 100 * (input - 100))



    updated_pa_constants = {
        'hit_by_pitch_chance': base_pa_constants['hit_by_pitch_chance'] + \
            adjust_base(base_pa_constants['hit_by_pitch_chance'], pitcher_stats['control'], False) , 
        'fastball_chance': base_pa_constants['fastball_chance'] + \
            adjust_base(base_pa_constants['fastball_chance'], pitcher_stats['velocity'], True) + \
            adjust_base(base_pa_constants['fastball_chance'], pitcher_stats['movement'], False),
        'fastball_strike_chance': base_pa_constants['fastball_strike_chance'] + \
            adjust_base(base_pa_constants['fastball_strike_chance'], pitcher_stats['control'], True), 
        'non_fastball_strike_chance': base_pa_constants['non_fastball_strike_chance'] + \
            adjust_base(base_pa_constants['non_fastball_strike_chance'], pitcher_stats['control'], True), 
        'fastball_strike_swing_chance': base_pa_constants['fastball_strike_swing_chance'] + \
            adjust_base(base_pa_constants['fastball_strike_swing_chance'], batter_stats['eye'], True) + \
            adjust_base(base_pa_constants['fastball_strike_swing_chance'], pitcher_stats['velocity'], False), 
        'non_fastball_strike_swing_chance': base_pa_constants['non_fastball_strike_swing_chance'] + \
            adjust_base(base_pa_constants['non_fastball_strike_swing_chance'], batter_stats['eye'], True) + \
            adjust_base(base_pa_constants['non_fastball_strike_swing_chance'], pitcher_stats['movement'], False), 
        'fastball_ball_swing_chance': base_pa_constants['fastball_ball_swing_chance'] + \
            adjust_base(base_pa_constants['fastball_ball_swing_chance'], batter_stats['eye'], False) + \
            adjust_base(base_pa_constants['fastball_ball_swing_chance'], pitcher_stats['velocity'], True), 
        'non_fastball_ball_swing_chance': base_pa_constants['non_fastball_ball_swing_chance'] + \
            adjust_base(base_pa_constants['non_fastball_ball_swing_chance'], batter_stats['eye'], False) + \
            adjust_base(base_pa_constants['fastball_ball_swing_chance'], pitcher_stats['movement'], True),
        'fastball_strike_contact_chance': base_pa_constants['fastball_strike_contact_chance'] + \
            adjust_base(base_pa_constants['fastball_strike_contact_chance'], batter_stats['contact'], True) + \
            adjust_base(base_pa_constants['fastball_strike_contact_chance'], pitcher_stats['velocity'], False),
        'non_fastball_strike_contact_chance': base_pa_constants['non_fastball_strike_contact_chance'] + \
            adjust_base(base_pa_constants['non_fastball_strike_contact_chance'], batter_stats['contact'], True) + \
            adjust_base(base_pa_constants['non_fastball_strike_contact_chance'], pitcher_stats['movement'], False),
        'fastball_ball_contact_chance': base_pa_constants['fastball_ball_contact_chance'] + \
            adjust_base(base_pa_constants['fastball_ball_contact_chance'], batter_stats['contact'], True) + \
            adjust_base(base_pa_constants['fastball_ball_contact_chance'], pitcher_stats['velocity'], False), 
        'non_fastball_ball_contact_chance': base_pa_constants['non_fastball_ball_contact_chance'] + \
            adjust_base(base_pa_constants['non_fastball_ball_contact_chance'], batter_stats['contact'], True) + \
            adjust_base(base_pa_constants['non_fastball_ball_contact_chance'], pitcher_stats['movement'], False), 
        'fastball_strike_foul_chance': base_pa_constants['fastball_strike_foul_chance'] + \
            adjust_base(base_pa_constants['fastball_strike_foul_chance'], batter_stats['contact'], False), 
        'non_fastball_strike_foul_chance': base_pa_constants['non_fastball_strike_foul_chance'] + \
            adjust_base(base_pa_constants['non_fastball_strike_foul_chance'], batter_stats['contact'], False), 
        'fastball_ball_foul_chance': base_pa_constants['fastball_ball_foul_chance'] + \
            adjust_base(base_pa_constants['fastball_ball_foul_chance'], batter_stats['contact'], False), 
        'non_fastball_ball_foul_chance': base_pa_constants['non_fastball_ball_foul_chance'] + \
            adjust_base(base_pa_constants['non_fastball_ball_foul_chance'], batter_stats['contact'], False)
    }

    pitch_counter = 0
    ball_counter = 0
    strike_counter = 0
    
    con = sqlite3.connect('mlb_simulator.db')
    cur = con.cursor()
    most_recent_pitch = cur.execute('SELECT MAX(pitch_id) FROM Pitches').fetchone()[0]
    if most_recent_pitch:
        starting_pitch_id = most_recent_pitch + 1
    else:
        starting_pitch_id = 1
    while pitch_counter <= 100:
        pitch_result = simulate_pitch(updated_pa_constants, starting_pitch_id + pitch_counter, pitcher_stats['player_id'], batter_stats['player_id'])
        # print(pitch_result)
        pitch_counter += 1
        if pitch_result == 'Ball':
            ball_counter += 1
        elif pitch_result == 'Called strike' or pitch_result == 'Swinging strike':
            strike_counter += 1
        elif pitch_result == 'Foul':
            if strike_counter < 2:
                strike_counter += 1
            else:
                continue
        elif pitch_result == 'Hit by pitch':
            ball_counter += 1
            pa_result = 'Hit by pitch'
            break
        elif pitch_result == 'In play':
            pa_result = 'In play'
            break
        
        if strike_counter == 3:
            pa_result = 'Strikeout'
            break
        
        if ball_counter == 4:
            pa_result = 'Walk'
            break

    if pa_result == 'In play':
        pa_result = simulate_in_play(pitcher_stats, batter_stats, situation, starting_pitch_id + pitch_counter -1, plate_app_id)

    to_insert = (
        plate_app_id,
        pitcher_stats['player_id'],
        batter_stats['player_id'],
        pa_result
    )

    return

def simulate_in_play(pitcher_stats, batter_stats, situation, pitch_id, plate_app_id):
    exit_velo_probs = pd.read_csv('exit_velo_probs.csv')
    rounded_las = pd.read_csv('rounded_las.csv')
    # options:
    # single, double, triple, home run, error, groundout, flyout, double play, triple play, fielders choice

    # pick direction
    direction_probabilities = {
        'pull': .42,
        'middle': .34,
        'oppo': .24
    }
    right_direcs = {
        'pull': 'left',
        'middle': 'center',
        'oppo': 'right'
    }
    left_direcs = {
        'pull': 'right',
        'middle': 'center',
        'oppo': 'left'
    }

    rel_direc = np.random.choice(['pull', 'middle', 'oppo'], p = [direction_probabilities['pull'], direction_probabilities['middle'], direction_probabilities['oppo']])
    bat_hand = batter_stats['handedness']
    if bat_hand == 'RIGHT':
        direc = right_direcs[rel_direc]
    if bat_hand == 'LEFT':
        direc = left_direcs[rel_direc]

    # pick exit velo/launch angle
    exve = np.random.choice(np.array(exit_velo_probs['Exit velo']), p = np.array(exit_velo_probs['BBE']))
    la_bbe = rounded_las[rounded_las['Exit velo'] == exve][['rounded_la', 'BBE']]
    la_bbe = la_bbe.assign(prob = la_bbe['BBE'] / la_bbe['BBE'].sum())
    laan = np.random.choice(np.array(la_bbe['rounded_la']), p = np.array(la_bbe['prob']))
    specific_exve_laan = rounded_las[(rounded_las['Exit velo'] == exve) & (rounded_las['rounded_la'] == laan)]
    bbe = specific_exve_laan['BBE'].iloc[0]
    oneb_prob = specific_exve_laan['1b'].iloc[0] / bbe
    twob_prob = specific_exve_laan['2b'].iloc[0] / bbe
    threeb_prob = specific_exve_laan['3b'].iloc[0] / bbe
    homer_prob = specific_exve_laan['HR'].iloc[0] / bbe
    out_prob = 1 - oneb_prob - twob_prob - threeb_prob - homer_prob

    # decide type of hit (or out)
    res = np.random.choice(['Single', 'Double', 'Triple', 'Home run', 'Out'], p = [oneb_prob, twob_prob, threeb_prob, homer_prob, out_prob])
    if res == 'Home run':
        return 'Home run'


    # decide position hit to
    first_probs = {
        'RIGHT': 5/14,
        'LEFT': 11/27
    }
    second_probs = {
        'RIGHT': 9/14,
        'LEFT': 16/27
    }
    third_probs = {
        'RIGHT': 15/31,
        'LEFT': 8/18
    }
    short_probs = {
        'RIGHT': 16/31,
        'LEFT': 10/18
    }
    pitcher_given_center_if = 4/5

    gb_rate = 0.43
    infield_single_rate = 0.07
    grounder_or_flyball = None

    if direc == 'center':
        if res == 'Single':
            if np.random.random() <= infield_single_rate:
                grounder_or_flyball = 'Ground ball'
                if np.random.random() <= pitcher_given_center_if:
                    pos = 1
                else:
                    pos = 2
            else:
                grounder_or_flyball = 'Fly ball'
                pos = 8
        elif res == 'Out':
            if np.random.random() <= gb_rate:
                grounder_or_flyball = 'Ground ball'
                if np.random.random() <= pitcher_given_center_if:
                    pos = 1
                else:
                    pos = 2
            else:
                grounder_or_flyball = 'Fly ball'
                pos = 8
        else:
            grounder_or_flyball = 'Fly ball'
            pos = 8
    elif direc == 'left':
        if res == 'Single':
            if np.random.random() <= infield_single_rate:
                grounder_or_flyball = 'Ground ball'
                if np.random.random() <= short_probs[bat_hand]:
                    pos = 6
                else:
                    pos = 5
            else:
                grounder_or_flyball = 'Fly ball'
                pos = 7
        elif res == 'Out':
            if np.random.random() <= gb_rate:
                grounder_or_flyball = 'Ground ball'
                if np.random.random() <= short_probs[bat_hand]:
                    pos = 6
                else:
                    pos = 5
            else:
                grounder_or_flyball = 'Fly ball'
                pos = 7
        else:
            grounder_or_flyball = 'Fly ball'
            pos = 7
    elif direc == 'right':
        if res == 'Single':
            if np.random.random() <= infield_single_rate:
                grounder_or_flyball = 'Ground ball'
                if np.random.random() <= second_probs[bat_hand]:
                    pos = 4
                else:
                    pos = 3
            else:
                grounder_or_flyball = 'Fly ball'
                pos = 9
        elif res == 'Out':
            if np.random.random() <= gb_rate:
                grounder_or_flyball = 'Ground ball'
                if np.random.random() <= second_probs[bat_hand]:
                    pos = 4
                else:
                    pos = 3
            else:
                grounder_or_flyball = 'Fly ball'
                pos = 9
        else:
            grounder_or_flyball = 'Fly ball'
            pos = 9

    # check for double plays and tag ups
    # implement later
    play_id = situation['initial_play_id'] + situation['plays_in_inning_so_far']
    year = situation['Year']
    pitcher_id = pitcher_stats['player_id']
    batter_id = batter_stats['player_id']
    fielder_id = situation['fielder_ids'][pos]
    play_type = grounder_or_flyball
    play_result = res
    first_runner_id = situation['runner_ids']['first']
    second_runner_id =situation['runner_ids']['second']
    third_runner_id = situation['runner_ids']['third']
    runs_scored = 0# runs_scored
    outs_made = 0 #outs_made
    inning = situation['inning']
    half_inning = situation['half_inning']
    pitch_id = pitch_id

    to_insert = (
        play_id,
        year,
        pitcher_id,
        batter_id,
        fielder_id,
        play_type,
        play_result,
        first_runner_id,
        second_runner_id,
        third_runner_id,
        runs_scored,
        outs_made,
        inning,
        half_inning,
        pitch_id,
        plate_app_id
    )

    insert_into_table('InPlays', to_insert)
    return res

def simulate_half_inning():
    pass

def simulate_inning():
    pass

def simulate_game():
    pass

def simulate_season(year, teams):
    # connect to sqlite database
    con = sqlite3.connect("mlb_simulator.db")
    cur = con.cursor()

    # see if the given year is already in database
    tups = cur.execute("SELECT DISTINCT(year) FROM Seasons").fetchall()
    years = [tup[0] for tup in tups]
    if year in years:
        print("Error: Season already in record.")
        return False
    
    # generate schedule
    schedule = generate_schedule(year, teams)

# outcomes = {}
# for i in range(1000):
#     outcomes[simulate_plate_appearance({
#         'control': 50,
#         'velocity': 50,
#         'movement': 50
#     }, {
#         'contact': 50,
#         'power': 50,
#         'eye': 50
#     })] += 1

# print(outcomes)


# N = 10000
# outcomes = {}
# for i in range(N):
#     result = simulate_plate_appearance({
#         'control': 50,
#         'velocity': 50,
#         'movement': 50
#     }, {
#         'contact': 50,
#         'power': 50,
#         'eye': 50
#     })
#     if result in outcomes:
#         outcomes[result] += 1
#     else:
#         outcomes[result] = 1
# for key in outcomes:
#     outcomes[key] = outcomes[key]/N
# print(outcomes)

# base_pa_constants = {
#         'hit_by_pitch_chance': 0.003, # hbp / total pitches
#         'fastball_chance': 0.5, # fastballs / total pitches
#         'fastball_strike_chance': 0.65, # fastball strikes / total fastballs
#         'non_fastball_strike_chance': 0.5, # non fastball strikes / total non fastballs
#         'fastball_strike_swing_chance': 0.7, # fastball strike swings / total fastball strikes
#         'non_fastball_strike_swing_chance': 0.7, # non fastball strike swings / total non fastball strikes
#         'fastball_ball_swing_chance': 0.15, # fastball ball swings / total fastball balls
#         'non_fastball_ball_swing_chance': 0.25, # non fastball ball swings / total non fastball balls
#         'fastball_strike_contact_chance': 0.85, # fastball strike contacts / total fastball strike swings
#         'non_fastball_strike_contact_chance': 0.75, # non fastball strike contacts / total non fastball strike swings
#         'fastball_ball_contact_chance': 0.6, # fastball ball contacts / total ball strike swings
#         'non_fastball_ball_contact_chance': 0.35, # non fastball ball contacts / total non fastball ball swings
#         'fastball_strike_foul_chance': 0.55, # fastball strike fouls / total fastball strike contacts
#         'non_fastball_strike_foul_chance': 0.5, # non fastball strike fouls / total non fastball strike contacts
#         'fastball_ball_foul_chance': 0.7, # fastball ball fouls / total fastball ball contacts
#         'non_fastball_ball_foul_chance': 0.6 # non fastball ball fouls / total non fastball ball contacts
# }

# pitch_outcomes = {
#     'Swinging strike': 0,
#     'Called strike': 0,
#     'Ball': 0,
#     'In play': 0,
#     'Hit by pitch': 0,
#     'Foul': 0
# }
# for i in range(N):
#     result = simulate_pitch(base_pa_constants)
#     if result in pitch_outcomes:
#         pitch_outcomes[result] += 1
#     else:
#         pitch_outcomes[result] = 1
# for key in pitch_outcomes:
#     pitch_outcomes[key] = np.round(pitch_outcomes[key]/N * 100, 2)
# print(pitch_outcomes)

test_situation = {
    'initial_play_id': 1,
    'plays_in_inning_so_far': 0,
    'Year': 2024,
    'fielder_ids': {
    1: 1,2: 2,3: 3,4: 4,5: 5,6: 6,7: 7,8: 8,9: 9,10: None
    },
    'runner_ids' : {
    'first': 11, 'second': 12, 'third': 13
    },
    'inning': 1,
    'half_inning': 'Top'
}
testres = simulate_in_play({
        'control': 50,
        'velocity': 50,
        'movement': 50,
        'player_id': 1,
        'handedness': 'RIGHT'
    }, {
        'contact': 50,
        'power': 50,
        'eye': 50,
        'player_id': 10,
        'handedness': 'LEFT'
    },
    test_situation,
    1,
    1)

print(testres)

# con = sqlite3.connect("mlb_simulator.db")
# cur = con.cursor()
# print(cur.execute('pragma table_info(InPlays)').fetchall())