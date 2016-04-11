
heroku pg:backups capture --app ecampus-oregonstate-buddyup
curl -o ecampus-oregonstate-buddyup.dump `heroku pg:backups public-url --app ecampus-oregonstate-buddyup`
heroku pg:backups capture --app oit-buddyup
curl -o oit-buddyup.dump `heroku pg:backups public-url --app oit-buddyup`
heroku pg:backups capture --app oregonstate-buddyup
curl -o oregonstate-buddyup.dump `heroku pg:backups public-url --app oregonstate-buddyup`
heroku pg:backups capture --app buddyup
curl -o buddyup.dump `heroku pg:backups public-url --app buddyup`
heroku pg:backups capture --app buddyup-canadacollege
curl -o buddyup-canadacollege.dump `heroku pg:backups public-url --app buddyup-canadacollege`
heroku pg:backups capture --app buddyup-collegeofsanmateo
curl -o buddyup-collegeofsanmateo.dump `heroku pg:backups public-url --app buddyup-collegeofsanmateo`
heroku pg:backups capture --app buddyup-skylinecollege
curl -o buddyup-skylinecollege.dump `heroku pg:backups public-url --app buddyup-skylinecollege`
heroku pg:backups capture --app buddyup-stanford
curl -o buddyup-stanford.dump `heroku pg:backups public-url --app buddyup-stanford`
heroku pg:backups capture --app buddyup-sydney
curl -o buddyup-sydney.dump `heroku pg:backups public-url --app buddyup-sydney`