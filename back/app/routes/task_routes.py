from flask import Blueprint, request, jsonify, current_app, abort
from bson import ObjectId

task_bp = Blueprint("tasks", __name__)

def col():
    return current_app.db.get_collection("tasks")

def serialize_task(doc):
    return {
        "id": str(doc["_id"]),
        "title": doc.get("title", ""),
        "completed": bool(doc.get("completed", False)),
    }

def to_oid(task_id: str):
    try:
        return ObjectId(task_id)
    except Exception:
        abort(400, description="invalid task id")

@task_bp.get("/")
def get_tasks():
    tasks = [serialize_task(d) for d in col().find().sort("_id", -1)]
    return jsonify(tasks), 200

@task_bp.post("/")
def create_task():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify(error="title is required"), 400

    doc = {"title": title, "completed": bool(data.get("completed", False))}
    res = col().insert_one(doc)
    doc["_id"] = res.inserted_id
    return jsonify(serialize_task(doc)), 201

@task_bp.get("/<task_id>")
def get_task(task_id):
    oid = to_oid(task_id)
    doc = col().find_one({"_id": oid})
    if not doc:
        return jsonify(error="task not found"), 404
    return jsonify(serialize_task(doc)), 200

@task_bp.put("/<task_id>")
def update_task(task_id):
    oid = to_oid(task_id)
    data = request.get_json(silent=True) or {}

    updates = {}
    if "title" in data:
        updates["title"] = (data.get("title") or "").strip()
    if "completed" in data:
        updates["completed"] = bool(data.get("completed"))

    if not updates:
        return jsonify(error="no fields to update"), 400

    r = col().update_one({"_id": oid}, {"$set": updates})
    if r.matched_count == 0:
        return jsonify(error="task not found"), 404

    doc = col().find_one({"_id": oid})
    return jsonify(serialize_task(doc)), 200

@task_bp.delete("/<task_id>")
def delete_task(task_id):
    oid = to_oid(task_id)
    r = col().delete_one({"_id": oid})
    if r.deleted_count == 0:
        return jsonify(error="task not found"), 404
    return "", 204
