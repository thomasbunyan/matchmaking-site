#Dumping the data to be used as fixtures do it locally
python manage.py dumpdata --natural-foreign --natural-primary --exclude=contenttypes --exclude=sessions --exclude=admin --format=json --indent=4 > fx.json

//Loading data on the server
heroku run python manage.py loaddate filename.json

//Reseting the database on heroku server
heroku run python manage.py reset_db --router=default