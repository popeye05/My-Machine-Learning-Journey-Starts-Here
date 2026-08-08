import pandas as pd
import requests
#Gte SMatch events, i.e Parsing that field from the Json Content 
def get_match_ids():
    url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/43/3.json"
    r = requests.get(url)
    ids=[]
    rjs= r.json()
    for i in rjs:
            ids.append(i["match_id"])
    return ids
#Gte Substitution events, i.e Parsing that field from the Json Content 
def get_substitution_events(events):
    subs = []
    for i in events:
        if i["type"]["name"] == "Substitution":
            subs.append(i)
    return subs
#Getting the goal events
def get_goal_events(events):
    goals = []
    for i in events:
        if i["type"]["name"] == "Shot" and i["shot"]["outcome"]["name"] == "Goal":
            goals.append(i)
    return goals
#Team Goals - Opponents goals
def get_score_diff(goals, team_name, minute):
    team_goals = 0
    opponent_goals = 0
    for g in goals:
        if g["minute"] < minute:
            if g["team"]["name"] == team_name:
                team_goals+=1
            else:
               opponent_goals +=1
    return team_goals - opponent_goals
#How Many substitute the team has used
def get_subs_used(subs, team_name, minute):
    team_subs = 0
    opp_subs = 0
    for s in subs:
        if s["minute"] < minute:
                    if s["team"]["name"] == team_name:
                        team_subs+=1
                   
    return team_subs
#this will parse all the events
def get_all_events(match_id):
     url = f"https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json"
         
     r = requests.get(url)
     rjs= r.json()
     return rjs
#this will get the team details also
def get_teams(events):
    teams = set()
    for event in events:
        teams.add(event["team"]["name"])
    return list(teams)
#Finally Checks if in the 5 Minute window any substitution happened or ont ,that's it!
def sub_happens_in_window(subs, team_name, window_start):
    for s in subs:
      if s["minute"] >= window_start and s["minute"] <window_start +5:
          if s["team"]["name"] == team_name:
              return True
    return False

#Now Heres the main data set we're going to build
def build_match_dataset(match_id):
    events = get_all_events(match_id)
    teams = get_teams(events)
    goals = get_goal_events(events)
    subs = get_substitution_events(events)
    
    rows = []
    for team in teams:
        for window_start in range(0, 120, 5):
            row = {
                "minute": window_start,
                "team": team,
                "score_diff": get_score_diff(goals, team, window_start),
                "subs_used_so_far": get_subs_used(subs, team, window_start),
                "sub_happens": int(sub_happens_in_window(subs, team, window_start))
            }
            rows.append(row)
    return rows

#Finally the main thing is, building this whole dataset which will use the above f(x) for each match and that function uses all the functions builtso far
def build_full_dataset():
    match_ids = get_match_ids()
    all_rows = []
    for match_id in match_ids:
        all_rows.extend(build_match_dataset(match_id))
    return all_rows


if __name__ == "__main__":
    full_data = build_full_dataset()
    #This is where we create the dataset and we convert the dictionary into csv
    df = pd.DataFrame(full_data)
    df.to_csv("substitution_dataset.csv", index=False)