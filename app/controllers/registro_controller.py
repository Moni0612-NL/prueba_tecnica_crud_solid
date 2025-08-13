from flask import Blueprint, request, jsonify
from app.repositories.registro_repository import RegistroRepository

bp = Blueprint('registros', __name__)
repo = RegistroRepository()

@bp.route('/', methods=['GET'])
def list_registros():
    regs = repo.list_all()
    return jsonify([r.to_dict() for r in regs])

@bp.route('/<int:id>', methods=['GET'])
def get_registro(id):
    r = repo.get(id)
    if not r:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify(r.to_dict())

@bp.route('/', methods=['POST'])
def create_registro():
    data = request.get_json()
    value = data.get('value')
    category = data.get('category')
    if value is None or category is None:
        return jsonify({"error": "value y category son requeridos"}), 400
    r = repo.create(value=value, category=category)
    return jsonify(r.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_registro(id):
    r = repo.get(id)
    if not r:
        return jsonify({"error": "No encontrado"}), 404
    data = request.get_json()
    r.value = data.get('value', r.value)
    r.category = data.get('category', r.category)
    r = repo.update(r)
    return jsonify(r.to_dict())

@bp.route('/<int:id>', methods=['DELETE'])
def delete_registro(id):
    r = repo.get(id)
    if not r:
        return jsonify({"error": "No encontrado"}), 404
    repo.delete(r)
    return jsonify({"deleted": True})

