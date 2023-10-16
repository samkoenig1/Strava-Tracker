# Strava-Tracker
This is a simple python dash application to pull data from your strava application, and display back simple stats such as (1) Total  Distance (2) Avg miles per hour (3) Number of Activities and (4) Average Speed all over time. 

In order to run this program, you'll need:

A Strava account.
- At least one activity recorded on that Strava account and one saved piece of gear associated with that activity.
- A personal API application on that Strava account.
- and the corresponding client_id, client_secret and refresh_token for that API application.

How to get client_id and client_secret:

- Create an API Application on Strava at https://www.strava.com/settings/api and set the Authorization Callback Domain to localhost
- Navigate back to https://www.strava.com/settings/api and you should see Client ID, Client Secret, Your Access Token, and Your Refresh Token
- Note: Do NOT use this refresh token. This token only has refresh access, and the token we need to generate needs read-all access. 

How to request a refresh_token

- Replace the values in the following template with the appropriate values from your API application's settings page and navigate to the URL in a browser: https://www.strava.com/oauth/authorize?client_id=[your_client_id]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all
-Copy the code provided in the URL after authorizing your app. The URL should look like this: http://localhost/exchange_token?state=&code=[CODE]&scope=read,activity:read_all
- Make the following GET request either from the commandline or a GUI like Postman or HTTPie:


How to add these values to the program
Once you have your refresh_token, client_secret and client_id ready, you can either replace the values in the payload array with your values or add them to the login.example.py file and remove the "example" from the file name. The login file is imported in the main program and its values are inserted into the payload via f-strings.

payload = {
    'client_id': f'{login.client_id}',
    'client_secret': f'{login.client_secret}',
    'refresh_token': f'{login.refresh_token}',
    'grant_type': "refresh_token",
    'f': 'json'
}
