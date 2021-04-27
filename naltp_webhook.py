""" NALTP Scores Webhook Maker
This script takes in tagpro.eu links, creates and formats embeds, and sends
a webhook given a key
"""
import requests
import json

WEBHOOK_URL = 'https://discord.com/api/webhooks/836555414329491506/4K-GNBHtgaK43kOcBBMXPZ6ZyFvYcCaHIELXMf1XA_myOUs0MJhnF3Tz2UoFxtL4z7Xz'

def format_score(score1: int, score2: int) -> []:
    output = []
    if (score1 < 10):
        output.append(' ' + str(score1))
    else:
        output.append(str(score1))
    if (score2 < 10):
        output.append(str(score2) + ' ')
    else:
        output.append(str(score2))
    return output

# add each link str into an iterable list
eu_links = []
# command line input stuff
print('What week is this game?')
week = int(input())
print('Input game ONE half ONE tagpro.eu link (ex. https://tagpro.eu/?match=2862215)')
g1h1_url = input()
eu_links.append([g1h1_url, 0])
print('Input game ONE half TWO tagpro.eu link')
g1h2_url = input()
eu_links.append([g1h2_url, 0])
print('Does this game ONE have overtime? Input 0 for no, 1 for yes')
g1ot = int(input())
if g1ot:
    print('Input game ONE OT ONE tagpro.eu link')
    g1ot1_url = input()
    eu_links.append([g1ot1_url, 1])
    print('Input game ONE OT TWO tagpro.eu link')
    g1ot2_url = input()
    eu_links.append([g1ot2_url, 1])
else:
    eu_links.append(False) # add filler value to signify no OT
    eu_links.append(False)

print('Input game TWO half ONE tagpro.eu link')
g2h1_url = input()
print('Input game TWO half ONE tagpro.eu link')
g2h2_url = input()
print('Does this game TWO have overtime? Input 0 for no, 1 for yes')
g2ot = int(input())
if g2ot:
    print('Input game TWO OT ONE tagpro.eu link')
    g2ot1_url = input()
    eu_links.append([g2ot1_url, 1])
    print('Input game ONE OT TWO tagpro.eu link')
    g2ot2_url = input()
    eu_links.append([g2ot2_url, 1])
else:
    eu_links.append(False) # add filler value to signify no OT
    eu_links.append(False)

#print('Do any of these games have overtime? Input 0 for no, 1 for yes')
#OT = int(input())
#if (OT):
#    print('You will be given a json that will have to be edited and manually sent via discohook.org\n\n')

print('Input the Youtube VOD link')
youtube_vod = input()

print('Input the Twitch VOD link')
twitch_vod = input()

print('Input the reaction thread link')
reaction_thread = input()

# organize the useful information into a list
t1_name = ''
t2_name = ''
match = []
i = 0
for url in eu_links:

    match.append([])
    if url: # make sure the eu_links[index] has data in it
        # grab the json data from the eu
        url_response = requests.get(url[0][0:18] + 'data/' + url[0][18:len(url)])
        json = url_response.json()
        if (i == 0) { # set team 1 & 2 names in a vars
            t1_name = json['teams'][0]['name']
            t2_name = json['teams'][1]['name']
        }

        match[i].append(url)

        map = json['map']['name']
        match[i].append(map)

        if (json['teams'][0]['name'] == t1_name):
            match[i].append(json['teams'][0]['score'])
            match[i].append(json['teams'][1]['score'])
        else:
            match[i].append(json['teams'][1]['score'])
            match[i].append(json['teams'][0]['score'])

        if (match[i][2] > match[i][3]):
            match[i].append(t1_name)
        elif (match[i][2] < match[i][3]):
            match[i].append(t2_name)
        else:
            match[i].append('TIE')

    else: # this game has no OT
        match[i] = False

    i+=1




# g1_map = g1h1_json['map']['name']
# match['G1'] = {'map' : g1_map}

# g1_t1_name = g1h1_json['teams'][0]['name']
# g1h1_t1_score = g1h1_json['teams'][0]['score']
# g1h1_t1_score_txt = ''
#if (g1h1_t1_score < 10):
#    g1h1_t1_score_txt = ' ' + str(g1h1_t1_score)
#else:
#    g1h1_t1_score_txt = str(g1h1_t1_score)

#g1_t2_name = g1h1_json['teams'][1]['name']
#g1h1_t2_score = g1h1_json['teams'][1]['score']

#g1h1_winner = ''
#if (g1h1_t1_score > g1h1_t2_score):
#    g1h1_winner = g1_t1_name
#elif (g1h1_t2_score > g1h1_t1_score):
#    g1h1_winner = g1h1_t2_score
#else:
#    g1h1_winner = 'TIE'

#scores = list()

#scores.append([g1h1_t1_score, g1h1_t2_score, g1h1_winner])


league_text = ''
league_color = 0
if (t1_name == 'M'):
    league_text = 'Majors'
    league_color = 8084480
elif (t1_name == 'N'):
    league_text = 'Minors'
    league_color = 4360181
elif (t1_name == 'A'):
    league_text = 'A-Team'
    league_color = 16741120
elif (t1_name == 'B'): # need to add >2 game formatting
    league_text = 'B-Team'
    league_color = 12539392


# print(g1_map)
# print(league_text + '\n' + g1_t1_name + ' : ' + str(g1h1_t1_score) + '\n' + g1_t2_name + ' : ' + str(g1h1_t2_score))

# build json output
output_dict = {
  "embeds": [
    {
      "title": (league_text + ' Week ' + str(week) + ' : ' + t1_name + ' vs ' + t2_name),
      "description": ('[**Youtube**](' + youtube_vod + ') | [Twitch](' + twitch_vod + ') | [Reaction Thread](' + reaction_thread + ')\n'),
      "color": league_color,
      "fields": []
    }
  ]
}

# build json output
"""
output_dict = {
  "embeds": [
    {
      "title": (league_text + ' Week ' + str(week) + ' : ' + t1_name + ' vs ' + t2_name),
      "description": ('[**Youtube**](' + youtube_vod + ') | [Twitch](' + twitch_vod + ') | [Reaction Thread](' + reaction_thread + ')\n'),
      "color": league_color,
      "fields": [
        {
          "name": "__**" + g1_map + " **__",
          "value": "[`H1:      6 - 1 NIP`]() \n[`H2:      4 - 0 NIP`]()\n`Total:  10 - 1 NIP`\n",
          "inline": True
        },
        {
          "name": "__**Cedar**__",
          "value": "[`H1:     12 - 2 NIP`]() \n[`H2:      5 - 2 NIP`]()\n`Total:  17 - 4 NIP`",
          "inline": True
        }
        ]
    }
  ]
}
"""

output_json_str = json.dumps(output_dict)

print(output_json_str)

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
