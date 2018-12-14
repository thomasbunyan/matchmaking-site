#Dumping the data to be used as fixtures do it locally
python manage.py dumpdata --natural-foreign --natural-primary --exclude=auth.Permission --exclude=contenttypes --exclude=sessions --exclude=admin --format=yaml --indent=4 > db2.yaml

#Load the fixtures using
heroku run python manage.py populate_db
