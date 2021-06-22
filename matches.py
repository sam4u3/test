import os.path
import pandas
from collections import Counter


def read_csv(path):
    data = pandas.read_csv(path)
    return data


def get_top_winner(g):
    return g['winner'].value_counts().idxmax()


def sort_by_value(item):
    return item[1]


if __name__ == '__main__':
    csv_path = os.path.abspath('./matches.csv')
    matches_data = read_csv(csv_path).fillna('')

    team1 = dict(matches_data['team1'].value_counts())
    team2 = dict(matches_data['team1'].value_counts())
    a_counter = Counter(team1)
    b_counter = Counter(team2)
    add_dict = a_counter + b_counter
    team3 = dict(add_dict)

    team_win_percentage = {}
    for team, count in matches_data['winner'].value_counts().drop('').items():
        percentage = (count / team3[team]) * 100
        team_win_percentage[team] = percentage

    print('Most win % matches :', sorted(team_win_percentage.items(), key=sort_by_value)[-1])
    print('Most Loss % matches : ', sorted(team_win_percentage.items(), key=sort_by_value)[0])
    print('Highest awarded player : ', matches_data['player_of_match'].value_counts().index[0])

    toss_win_percentage = {}
    for team, count in matches_data['toss_winner'].value_counts().items():
        percentage = (count / team3[team]) * 100
        toss_win_percentage[team] = percentage

    print('Lowest % toss wins : ', sorted(toss_win_percentage.items(), key=lambda k:round(k[1]))[0])

    not_normal = matches_data.loc[matches_data['result'] != 'normal']
    print('% of not normal result : ',len(not_normal)/len(matches_data)*100)

    # Team(s) which won the toss but lost the match highest number of times
    final = {}
    for toss_winner, match_winner in zip(matches_data['toss_winner'], matches_data['winner']):
        if toss_winner != match_winner:
            if toss_winner not in final:
                final[toss_winner] = 1
            else:
                final[toss_winner] += 1

    print('Won toss but lost match :', sorted(final.items(), key=sort_by_value, reverse=True)[0])

    final = {}
    for toss_winner, match_winner, toss_decision in zip(matches_data['toss_winner'], matches_data['winner'],
                                                        matches_data['toss_decision']):
        if toss_decision == 'bat' and toss_winner == match_winner:
            if toss_winner not in final:
                final[toss_winner] = 1
            else:
                final[toss_winner] += 1

    print('Toss winner and match win :', sorted(final.items(), key=sort_by_value, reverse=True)[0])
