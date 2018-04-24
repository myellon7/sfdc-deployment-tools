********************************
********************************
***                          ***
***   @author: Mark Yellon   ***
***   @since 4/24/2018       ***
***                          ***
***                          ***
********************************
********************************
PRE-REQUISITES:

- Python 3.0 or higher installed on your machine

- navigate to the following link and follow the instructions to install the Google APIs client library for Python:
	https://developers.google.com/api-client-library/python/start/installation

1. Navigate to https://console.developers.google.com/apis/dashboard
2. Create a project
3. You should now be on the APIs and servies dashboard. Click the Enable APIs and Services button
4. Search for and select the Google Sheets API. Click Enable.
5. Navigate to the Credentials section on the lefthand side of the page. Click Create Credentials and using the down arrow selector, Select Service Account key
6. Rename the downloaded file as 'client_secret.json' and place it in the same directory as the one where the packageCreate.py file is located
7. Find the client_email parameter in the client_secret.json file and share the changed items log with that email address. This step is crucial, as you will encounter errors if you do not do this

ASSUMPTIONS:
1. Sheet that will be parsed into package.xml and destructive_changes.xml is the FIRST sheet in a workbook