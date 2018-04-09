## import xlwings library
import xlwings as xw

##import dependencies for Google Drive API
from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

##following lines are to set up authentication to your google drive to access
##changed items log
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
    
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))
##files = DRIVE.files().list().execute().get('files', [])



## instantiate a workbook object
wb = xw.Book('CT Items Log.xlsx')
## gather the worksheet name and data range that will be processed
##data_sheet = input("Please enter the name of the worksheet that contains your data: ")
data_sheet = 'S2W2 - 219'
data_range = input("Please enter the data range you'd like to convert to a package.xml: ")

##create sheet object with desired sheet
sheet = wb.sheets(data_sheet)
##gather data object based on data range specified in input
data = sheet.range(data_range)


constructive_items_dict = {}
destructive_items_dict = {}
#go through the data gathered and start creating dictionary of all data types specified and member items
for item in data.value:
    if item[4] == 'Constructive':
        if item[2] in constructive_items_dict:
            constructive_items_dict[item[2]].append(str(item[3]))
        else:
            constructive_items_dict[item[2]] = [str(item[3])]

    elif item[4] == 'Destructive':
        if item[2] in destructive_items_dict:
            destructive_items_dict[item[2]].append(str(item[3]))
        else:
            destructive_items_dict[item[2]] = [str(item[3])]
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








