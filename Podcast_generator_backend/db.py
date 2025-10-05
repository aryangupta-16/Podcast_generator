from mongoengine import connect

def init_db():
    connect(
        db="podcast_generator", 
        host="mongodb://localhost:27017"
    )

    print("Connected to MongoDB")