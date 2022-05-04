#Imports
import json
import os
import csv

#Read in the JSON data
folder = 'partial_dataset'
file_names = os.listdir(folder)

#List fields for CSV
fields = ['id','innings','innings_team','over','delivery','batter','bowler','non_striker','batter_runs','extra_runs',
          'total_runs']

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
                row = [game_id,innings_number,i['team'],over['over'],deliv_count,deliv['batter'],
                       deliv['bowler'],deliv['non_striker'],deliv['runs']['batter'],deliv['runs']['extras'],
                      deliv['runs']['total']]
                rows.append(row)
                
                deliv_count += 1
        
        innings_number += 1
    
    #Write to a CSV file
    filename = game_id + '.csv'

    with open('csv_files/'+filename, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile, lineterminator='\n') 

        # writing the fields 
        csvwriter.writerow(fields) 

        # writing the data rows 
        csvwriter.writerows(rows)
