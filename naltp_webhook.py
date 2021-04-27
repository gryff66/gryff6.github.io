""" NALTP Scores Webhook Maker
This script takes in tagpro.eu links, creates and formats embeds, and sends
a webhook given a key
"""
import requests
import json
import subprocess

WEBHOOK_URL = 'https://discord.com/api/webhooks/836555414329491506/4K-GNBHtgaK43kOcBBMXPZ6ZyFvYcCaHIELXMf1XA_myOUs0MJhnF3Tz2UoFxtL4z7Xz'

def format_score(score1: int, score2: int) -> []:
    output = []
    if (int(score1) < 10):
        output.append(' ' + str(score1))
    else:
        output.append(str(score1))
    if (int(score2) < 10):
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

print('Input game TWO half ONE tagpro.eu link')
g2h1_url = input()
eu_links.append([g2h1_url, 0])
print('Input game TWO half ONE tagpro.eu link')
g2h2_url = input()
eu_links.append([g2h2_url, 0])
print('Does this game TWO have overtime? Input 0 for no, 1 for yes')
g2ot = int(input())
if g2ot:
    print('Input game TWO OT ONE tagpro.eu link')
    g2ot1_url = input()
    eu_links.append([g2ot1_url, 1])
    print('Input game ONE OT TWO tagpro.eu link')
    g2ot2_url = input()
    eu_links.append([g2ot2_url, 1])

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
    # grab the json data from the eu
    print(url[0][0:18] + 'data/' + url[0][18:len(url[0])])
    url_response = requests.get(url[0][0:18] + 'data/' + url[0][18:len(url[0])])
    print(url_response)
    url_json = url_response.json()
    if (i == 0): # set team 1 & 2 names in a vars
        t1_name = url_json['teams'][0]['name']
        t2_name = url_json['teams'][1]['name']


    match[i].append(url[0])

    map = url_json['map']['name']
    match[i].append(map)

    if (url_json['teams'][0]['name'] == t1_name):
        match[i].append(int(url_json['teams'][0]['score']))
        match[i].append(int(url_json['teams'][1]['score']))
    else:
        match[i].append(int(url_json['teams'][1]['score']))
        match[i].append(int(url_json['teams'][0]['score']))

    if (match[i][2] > match[i][3]):
        match[i].append(t1_name)
    elif (match[i][2] < match[i][3]):
        match[i].append(t2_name)
    else:
        match[i].append('TIE')

    if url[1]: # half is an OT half
        match[i].append(True)
    else:
        match[i].append(False)

    i+=1


league_text = ''
league_color = 0
if (t1_name[0] == 'M'):
    league_text = 'Majors'
    league_color = 8084480
elif (t1_name[0] == 'N'):
    league_text = 'Minors'
    league_color = 4360181
elif (t1_name[0] == 'A'):
    league_text = 'A-Team'
    league_color = 16741120
elif (t1_name[0] == 'B'): # need to add >2 game formatting
    league_text = 'B-Team'
    league_color = 12539392

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

# build fields dict and adds it to output_dict[fields]
print(len)
i = 0
while i < len(match):
    field = {}

    h1_score_txt = format_score(match[i][2], match[i][3])
    h2_score_txt = format_score(match[i+1][2], match[i+1][3])
    total_score_txt = format_score(match[i][2] + match[i+1][2], match[i][3] + match[i+1][3])

    game_winner = 'TIE'
    if (match[i][2] + match[i+1][2] > match[i][3] + match[i+1][3]):
        game_winner = t1_name
    elif (match[i][2] + match[i+1][2] < match[i][3] + match[i+1][3]):
        game_winner = t2_name


    ot_txt = ''
    if (match[i][5]):
        ot_txt = 'OT'
    field['name'] = "__**" + match[i][1] + " " + ot_txt + " **__"
    field['value'] = ("[`H1:    " + h1_score_txt[0] + " - " + h1_score_txt[1] + " " + match[i][4] + "`](" + match[i][0] + ") \n[`H2:    " + h2_score_txt[0] + " - " + h2_score_txt[1] + " " + match[i+1][4] + "`](" + match[i+1][0] + ")\n`Total: " + total_score_txt[0] + " - " + total_score_txt[1] + " " + game_winner + "`\n")
    field['inline'] = True

    output_dict["embeds"][0]["fields"].append(field)

    i+=2

output_json_str = json.dumps(output_dict)

exit_code = subprocess.run(["curl", "-X", "POST", "-H", "Content-Type: application/json", "-d", output_json_str, WEBHOOK_URL])
