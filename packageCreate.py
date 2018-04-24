##import dependencies for Google Drive API
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import gspread

##following lines are to set up authentication to your google drive to access
##changed items log
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)


client = gspread.authorize(creds)


sheet = client.open("CoorsTek - Changed Items Log").sheet1

data = sheet.get_all_values()

#following code is to parse through data gathered from google drive
constructive_items_dict = {}
destructive_items_dict = {}
#go through the data gathered and start creating dictionary of all data types specified and member items
for item in data:
    if item[8] == 'Constructive':
        if item[6] in constructive_items_dict:
            constructive_items_dict[item[6]].append(str(item[7]))
        else:
            constructive_items_dict[item[6]] = [str(item[7])]

    elif item[8] == 'Destructive':
        if item[6] in destructive_items_dict:
            destructive_items_dict[item[6]].append(str(item[7]))
        else:
            destructive_items_dict[item[6]] = [str(item[7])]
constructive_package = ''
destructive_package = ''
#go through dict created above and format each type based on requirements for package.xml file
messageC = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Package xmlns=\"http://soap.sforce.com/2006/04/metadata\">\n'

for item in constructive_items_dict:
    messageC += '<types>\n'
    for x in constructive_items_dict[item]:
        messageC += '\t<members>' + x + '</members>\n'
    messageC += '\t<name>' + item + '</name>'
    messageC += '\n\t</types>\n'
constructive_package += messageC
    
constructive_package += '\t<version>41.0</version>\n</Package>'

messageD = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Package xmlns=\"http://soap.sforce.com/2006/04/metadata\">\n'

for item in destructive_items_dict:
    messageD += '<types>\n'
    for x in destructive_items_dict[item]:
        messageD += '\t<members>' + x + '</members>\n'
    messageD += '\t<name>' + item + '</name>'
    messageD += '\n\t</types>\n'
destructive_package += messageD
    
destructive_package += '\t<version>41.0</version>\n</Package>'



#create package.xml file in same directory and write formatted contents to that file
file = open('package.xml', mode= 'w')

file.write(constructive_package)

file.close()

#create package.xml file in same directory and write formatted contents to that file
file = open('destructiveChanges.xml', mode= 'w')

file.write(destructive_package)

file.close()









