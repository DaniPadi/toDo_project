from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from .. import db
from ..models.task import serialize_task

task_bp = Blueprint("tasks", __name__)


hola = "Jenkins"
@task_bp.route("/", methods=["GET"])
def get_tasks():
    tasks = [serialize_task(task) for task in db.tasks.find()]

    return jsonify(tasks)


@task_bp.route("/", methods=["POST"])
def create_task():
    data = request.json
    task = {"title": data.get("title", ""), "completed": False}
    result = db.tasks.insert_one(task)
    
    return jsonify({"_id": str(result.inserted_id)}), 201


@task_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = db.tasks.find_one({"_id": ObjectId(task_id)})
    if task:
        return jsonify(serialize_task(task))
    
    return jsonify({"error:" "task not found"}), 404


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json
    updated = db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"title": data.get("title", ""), "completed": data.get("completed" , False) }} 
    )
    if updated.modified_count > 0:
            return jsonify({"msg": "task updated"}), 301
    
    return jsonify({"error:" "task not Found"}), 404




@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
     deleted = db.tasks.delete_one({"_id": ObjectId(task_id)})

     if deleted.deleted_count > 0:
          return jsonify({"msg": "task deleted"})
     
     return jsonify({"error": "Task not Found"}), 404
