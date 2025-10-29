import json
import csv 
#-------------------------------------------------------------------------------
# takes the json file specified and creates the link csv file version
#
# DISCLAIMER: Might have to change the file path for the files when opening/reading
# Since I moved the files around... have a nice day
# ------------------------------------------------------------------------------
def link_convert():
    json_file = input("what is the json file you wish to convert?: ")

    with open(json_file, 'r', encoding='utf-8') as f:
        apps = json.load(f)
    
    csv_file = json_file.replace('./', "") 
    csv_file = csv_file.replace('.json', "_links.csv")

    with open(csv_file, 'w', newline='') as f: 
        writer = csv.writer(f)
        for list in apps:
            for app in list:
                writer.writerow([app['url']])

link_convert()
