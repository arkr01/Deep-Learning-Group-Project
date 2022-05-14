#Imports
import json
import os
import csv

#Read in the JSON data
folder = 'all_json'
file_names = os.listdir(folder)

#Some sets
#all_players = set()
all_batters = set()
all_bowlers = set()
wicket_types = set()
venues = set()

file_names_to_use = []

number_of_games = 100

game_counter = 0
for f_name in file_names:
    if game_counter >= number_of_games:
        break
    
    #Ignore the readme file
    if f_name == 'README.txt':
        continue
        
    #Read the JSON file
    file = open(folder + '\\' + f_name)
    data = json.load(file)
    
    #Only want T20 data
    if data['info']['match_type'] != "T20":
        continue
    
    #Collect all the players into sets
    for i in data['innings']:
        for o in i['overs']:
            for d in o['deliveries']:
                all_batters.add(data['info']['registry']['people'][d['batter']])
                all_bowlers.add(data['info']['registry']['people'][d['bowler']])
    
#     for p in data['info']['registry']['people']:
#         all_players.add(data['info']['registry']['people'][p])
    
    #Do same for wicket types
    for i in data['innings']:
        for o in i['overs']:
            for d in o['deliveries']:
                if 'wickets' in d:
                    wicket_types.add(d['wickets'][0]['kind'])
    
    #Do same for venues
    venues.add(data['info']['venue'])
    
    file_names_to_use.append(f_name)
    
    game_counter += 1
        
#List fields for CSV
fields = ['game_id','venue','innings','innings_team','over','delivery','batter_name','batter_id',
          'bowler_name','bowler_id',
          'batter_runs','extra_runs','total_runs','wicket','wicket_kind','t_runs_0','t_runs_1','t_runs_2','t_runs_3',
         't_runs_4','t_runs_5','t_runs_6','t_runs_7','t_runs_8']

#Re-defining batter and bowler IDs
indices = range(len(all_bowlers))
bowler_dict = {k : v for (k,v) in zip(tuple(all_bowlers),indices)}
indices = range(len(all_batters))
batter_dict = {k : v for (k,v) in zip(tuple(all_batters),indices)}

for v in venues:
    fields.append("v_" + v)
for wt in wicket_types:
    fields.append("wicket_" + wt)
for batter in all_batters:
    fields.append("batter_"+str(batter_dict[batter]))
for bowler in all_bowlers:
    fields.append("bowler_"+str(bowler_dict[bowler]))

#Useful for one-hot
indices = range(len(fields))
field_dict = {k : v for (k,v) in zip(fields,indices)}

games = []

for f_name in file_names_to_use:
    
    #Ignore the readme file
    if f_name == 'README.txt':
        continue
        
    #Read the JSON file
    file = open(folder + '\\' + f_name)
    data = json.load(file)


    #Some preliminary stuff
    rows = []
    game_id = f_name.split('.')[0]  #take the first part of the file name and use this as the game id

    #Iterate through the innings
    innings_number = 0
    for i in data['innings']:
        #Iterate through the overs
        for over in i['overs']:
            #Iterate through deliveries
            deliv_count = 0
            for deliv in over['deliveries']:
                row = [0]*len(fields) #initialise as all zeros 

                #Fill in the info
                row[0] = game_id
                row[1] = data['info']['venue']
                row[2] = innings_number
                row[3] = i['team']
                row[4] = over['over']
                row[5] = deliv_count
                row[6] = deliv['batter']
                row[7] = batter_dict[data['info']['registry']['people'][deliv['batter']]]
                row[8] = deliv['bowler']
                row[9] = bowler_dict[data['info']['registry']['people'][deliv['bowler']]]
                row[10] = deliv['runs']['batter']
                row[11] = deliv['runs']['extras']
                row[12] = deliv['runs']['total']

                if "wickets" in deliv:
                    row[13] = 1
                    row[14] = deliv["wickets"][0]["kind"]
                else:
                    row[14] = "NA"


                #Do the one-hot bit
                #For number of runs
                label = "t_runs_" + str(deliv['runs']['total'])
                row[fields.index(label)] = 1

                #For wickets
                row[fields.index("v_" + data['info']['venue'])] = 1

                #For venues
                if "wickets" in deliv:
                    row[fields.index("wicket_" + deliv["wickets"][0]["kind"])] = 1


                #For the batter/bowler
                batter_key = 'batter_' + str(batter_dict[data['info']['registry']['people'][deliv['batter']]])
                bowler_key = 'bowler_' + str(bowler_dict[data['info']['registry']['people'][deliv['bowler']]])
                #non_striker_key = 'non_striker_' + data['info']['registry']['people'][deliv['non_striker']]

                batter_index = field_dict[batter_key]
                bowler_index = field_dict[bowler_key]
                #non_striker_index = field_dict[non_striker_key]

                row[batter_index] = 1
                row[bowler_index] = 1
                #row[non_striker_index] = 1


                #Append this row
                rows.append(row)

                deliv_count += 1

        innings_number += 1

    games.append(rows)


#Write to a CSV file
#filename = game_id + '.csv'
filename = 'cricsheet_data_partial.csv'


with open('csv_files/'+filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile, lineterminator='\n') 

    # writing the fields 
    csvwriter.writerow(fields) 
    
    for rows in games:
        # writing the data rows 
        csvwriter.writerows(rows)
