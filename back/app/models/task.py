from bson.objectid import ObjectId

def serialize_task(task):

    return {
        "_id": str(task["_id"]),
        "title": task["title"],
        "completed": task["completed"]
    }