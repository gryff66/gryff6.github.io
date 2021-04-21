import requests
import json

week = 1
g1h1url = 'https://tagpro.eu/?match=2869477'
g1h2url = ''
g2h1url = ''
g2h2url = ''
g1h1url_response = requests.get(g1h1url[0:18] + 'data/' + g1h1url[18:len(g1h1url)])
g1h1_json = g1h1url_response.json()

t1_scores = list()
t2_scores = list()


g1_map = g1h1_json['map']['name']

g1_t1_name = g1h1_json['teams'][0]['name']
g1h1_t1_score = g1h1_json['teams'][0]['score']
g1h1_t1_score_txt = ''
if (g1h1_t1_score < 10):
    g1h1_t1_score_txt = ' ' + str(g1h1_t1_score)
else:
    g1h1_t1_score_txt = str(g1h1_t1_score)

g1_t2_name = g1h1_json['teams'][1]['name']
g1h1_t2_score = g1h1_json['teams'][1]['score']

g1h1_winner = ''
if (g1h1_t1_score > g1h1_t2_score):
    g1h1_winner = g1_t1_name
elif (g1h1_t2_score > g1h1_t1_score):
    g1h1_winner = g1h1_t2_score
else:
    g1h1_winner = 'TIE'

scores = list()

scores.append([g1h1_t1_score, g1h1_t2_score, g1h1_winner])


league_text = ''
if (g1_t1_name[0] == 'M'):
    league_text = 'Majors'
elif (g1_t1_name[0] == 'N'):
    league_text = 'Minors'
elif (g1_t1_name[0] == 'A'):
    league_text = 'A-Team'
elif (g1_t1_name[0] == 'B'): # need to add >2 game formatting
    league_text = 'B-Team'

league_color = 0
if (g1_t1_name[0] == 'M'):
    league_color = 1
elif (g1_t1_name[0] == 'N'):
    league_color = 2
elif (g1_t1_name[0] == 'A'):
    league_color = 3
elif (g1_t1_name[0] == 'B'):
    league_color = 4

print(g1_map)
print(league_text + '\n' + g1_t1_name + ' : ' + str(g1h1_t1_score) + '\n' + g1_t2_name + ' : ' + str(g1h1_t2_score))

# build json output
output_dict = {
  "embeds": [
    {
      "title": (league_text + ' Week ' + str(week) + ' : ' + g1_t1_name + ' vs ' + g1_t2_name),
      "description": "[**Youtube**]() | [Twitch]() | [Wire Thread]() | [Reaction Thread]()\n",
      "color": league_color,
      "fields": [
        {
          "name": "__**" + g1_map + " **__",
          "value": "[`H1:      6 - 1 NIP`]() \n[`H2:      4 - 0 NIP`]()\n`Total:  10 - 1 NIP`\n",
          "inline": 'true'
        },
        {
          "name": "__**Cedar**__",
          "value": "[`H1:     12 - 2 NIP`]() \n[`H2:      5 - 2 NIP`]()\n`Total:  17 - 4 NIP`",
          "inline": 'true'
        }
        ]
      }
    }
  ]
}

#output_dict = {
#"embeds" : {
#        "title" : (league_text + ' Week ' + str(week) + ' : ' + g1_t1_name + ' vs ' + g1_t2_name),
#        "description" : "[**Youtube**]() | [Twitch]() | [Wire Thread]() | [Reaction Thread]()\n",
#        "color" : league_color,
#        "fields" : {
#
#        }
#    }
#}
