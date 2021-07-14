from datastore import Datastore

ds = Datastore().setup()

records = ds.fetch_all()
print(len(records))