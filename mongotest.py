import pymongo

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.thing
collection = db.thing2

db.collection.insert_many(
    [
        {
            "name": "Harvey",
            "cat": "Category 4"
        },
        {
            "name": "Irma",
            "cat": "Category 5"
        }
    ]
)

print(list(db.collection.find()))