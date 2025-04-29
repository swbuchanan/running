# running

This project is inspired by http://pac.tom7.org/index.shtml, but significantly less well-defined and less likely to be completed.
It's also based in Canberra.

Currently all I have is some boilerplate code that will let me plot gpx files on a map.

# Setup

This is currently not a very user-friendly workflow.
Create a virtualenv and install the dependencies in `requirements.txt`.
Create a file called .env that contains the following variables.
The right hand sides of all these lines will need to be filled in by different arcane and distasteful methods; there is information available in various places on the internet for how to obtain the data.
```
STRAVA_CLIENT_ID = 
STRAVA_CLIENT_SECRET = 
STRAVA_VERIFY_TOKEN = 
AUTH_CODE = 
ACCESS_TOKEN = 
REFRESH_TOKEN = 
```

Now, before you go on a run, start the app with
`make serve` and then `make serve-app`, followed by `make register`.
The `make register` command will need to be done about once a day; the access token that you get from this process is only temporary, and there is a script run by this command that will refresh it.

## to-do:
- a lot of running
- a more organized database of runs
- some way of auto-downloading my strava activities and updating the database
- set up some rules for the project
- blog post
- more stuff??
