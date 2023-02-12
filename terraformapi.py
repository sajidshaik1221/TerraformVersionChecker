import requests
import base64
import json
import sys
import csv
import fire
import hcl2
import hcl
import configparser
#CodePath  TFEToken
# CREATE OBJECT
config_file = configparser.ConfigParser()

# READ CONFIG FILE
config_file.read("C:\\temp\\Terraform scrapping\\configurations.ini")
 
# UPDATE A FIELD VALUE

#print(config_file)

#print('cmd entry:', sys.argv[1])
number = 1
found = 0
#moduleName=sys.argv[1]
#key=sys.argv[2] -- need to be uncommented

my_list_ddiff={}
my_list = {}
tfe_list ={}
headers = {'Authorization': "Bearer {}".format(config_file["KeySettings"]["TFEToken"])}
#headers = {'Authorization': "Bearer {}".format(key)} -- need to be uncommented



with(open(config_file["KeySettings"]["CodePath"], 'r')) as file:
           dict12 = hcl2.load(file)

#with(open('I:\Dipankar\main.tf', 'r')) as f:
          #  dict1 = json.load(f)

#print(config_file["KeySettings"]["URLStartPart"])

for modules in dict12.get("module", []):	
	for module in modules.values():	
		#print(list(modules.keys())[0])		
		
		v=module['version']
		# print(v)	
		my_list[list(modules.keys())[0]] =v
 


print('From local modules and corresponding version :')
print(my_list)

#url = 'https://tfe.jpmchase.net/api/v2/organizations/ATLAS-MODULE-REGISTRY/registry-modules'
for key_item in my_list:

    # print(key_item)
    # print(my_list[key_item])
    
    for number in range(20):

        url = config_file["KeySettings"]["TFEURLStartPart"] + str(number) + config_file["KeySettings"]["TFEURLEndPart"]
        resp = requests.get(url=url, headers=headers )

        j = resp.json()
        for p in j['data']:
            #print('trying')
            if str(p['attributes']['name']) == key_item :
                print('checking for',key_item)
                if (str(p['attributes']['version-statuses'][0]['version']) == str(my_list[key_item])):
                    number = number	
                else:
                    tfe_list[str(p['attributes']['name'])] = str(p['attributes']['version-statuses'][0]['version'])
                
            else:
                #print('not')
                number = number + 1
        
print('Below is the mismatch of version compared to TFE latest with local code base :')
print(tfe_list)
#print (number)
