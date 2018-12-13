#Dumping the data to be used as fixtures do it locally
python manage.py dumpdata --natural-foreign --natural-primary --exclude=auth.Permission --exclude=contenttypes --exclude=sessions --exclude=admin --format=json --indent=4 > db.json

#Manually remove anything you do not want included

//Loading data on the server
heroku run python manage.py loaddata db.json

//Reseting the database on heroku server
heroku run python manage.py reset_db --router=default

//Alternative Drop
heroku run python manage.py flush 
