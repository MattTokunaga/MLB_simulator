import sqlite3
import numpy as np
import calendar
from datetime import date
from datetime import timedelta
import copy
import json

current_year = 2024
number_of_teams = 0

teams = [
    ("Giants", "San Francisco", "nlwest"),
    ("Dodgers", "Los Angeles", "nlwest"),
    ("Padres", "San Diego", "nlwest"),
    ("Rockies", "Colorado", "nlwest"),
    ("Diamondbacks", "Arizona", "nlwest"),
    ("Cardinals", "St. Louis", "nlcentral"),
    ("Brewers", "Milwaukee", "nlcentral"),
    ("Reds", "Cincinnati", "nlcentral"),
    ("Pirates", "Pittsburgh", "nlcentral"),
    ("Cubs", "Chicago", "nlcentral"),
    ("Marlins", "Miami", "nleast"),
    ("Phillies", "Philadelphia", "nleast"),
    ("Mets", "New York", "nleast"),
    ("Braves", "Atlanta", "nleast"),
    ("Nationals", "Washington", "nleast"),
    ("Athletics", "Oakland", "alwest"),
    ("Rangers", "Texas", "alwest"),
    ("Mariners", "Seattle", "alwest"),
    ("Angels", "Anaheim", "alwest"),
    ("Astros", "Houston", "alwest"),
    ("Royals", "Kansas City", "alcentral"),
    ("White Sox", "Chicago", "alcentral"),
    ("Guardians", "Cleveland", "alcentral"),
    ("Twins", "Minnesota", "alcentral"),
    ("Tigers", "Detroit", "alcentral"),
    ("Yankees", "New York", "aleast"),
    ("Red Sox", "Boston", "aleast"),
    ("Blue Jays", "Toronto", "aleast"),
    ("Orioles", "Baltimore", "aleast"),
    ("Rays", "Tampa Bay", "aleast"),
]

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

def simulate_pitch():
    pass

def simulate_plate_appearance():
    pass

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




