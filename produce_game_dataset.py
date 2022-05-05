#Imports
import json
import os
import csv

#Read in the JSON data
folder = 'partial_dataset'
file_names = os.listdir(folder)

#Obtain a set of all players involved in the games 
all_players = set()

for f_name in file_names:
    #Ignore the readme file
    if f_name == 'README.txt':
        continue
        
    #Read the JSON file
    file = open(folder + '\\' + f_name)
    data = json.load(file)
    
    for p in data['info']['registry']['people']:
        all_players.add(data['info']['registry']['people'][p])

        
#Start preparing to create the CSV file again, but with one-hot for players
#List fields for CSV
fields = ['game_id','innings','innings_team','over','delivery','batter_name','batter_id',
          'bowler_name','bowler_id','non_striker_name','non_striker_id',
          'batter_runs','extra_runs','total_runs']
for pos in ['batter','bowler','non_striker']:
    for player in all_players:
        fields.append(pos + "_" + player)

#Useful for one-hot
indices = range(len(fields))
field_dict = {k : v for (k,v) in zip(fields,indices)}

games = []

for f_name in file_names:
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
                row[1] = innings_number
                row[2] = i['team']
                row[3] = over['over']
                row[4] = deliv_count
                row[5] = deliv['batter']
                row[6] = data['info']['registry']['people'][deliv['batter']]
                row[7] = deliv['bowler']
                row[8] = data['info']['registry']['people'][deliv['bowler']]
                row[9] = deliv['non_striker']
                row[10] = data['info']['registry']['people'][deliv['non_striker']]
                row[11] = deliv['runs']['batter'],deliv['runs']['extras']
                row[12] = deliv['runs']['total']
                
                #Do the one-hot bit
                batter_key = 'batter_' + data['info']['registry']['people'][deliv['batter']]
                bowler_key = 'bowler_' + data['info']['registry']['people'][deliv['bowler']]
                non_striker_key = 'non_striker_' + data['info']['registry']['people'][deliv['non_striker']]
                
                batter_index = field_dict[batter_key]
                bowler_index = field_dict[bowler_key]
                non_striker_index = field_dict[non_striker_key]
                
                row[batter_index] = 1
                row[bowler_index] = 1
                row[non_striker_index] = 1
                
                
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
