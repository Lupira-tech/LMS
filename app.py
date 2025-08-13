from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db" #db location
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))
    def to_dict(self): return {"id": self.id, "name": self.name, "description": self.description} #db structure

with app.app_context():
    db.create_all()

@app.route("/items", methods=["GET"])
def get_items(): return jsonify([i.to_dict() for i in Item.query.all()])

@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json() or {}
    if not data.get("name"): abort(400, "Missing 'name'")
    item = Item(**data)
    db.session.add(item); db.session.commit()
    return jsonify({"message": "Item created", "item": item.to_dict()}), 201

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json() or {}
    for k in ["name","description"]:
        if k in data: setattr(item, k, data[k])
    db.session.commit()
    return jsonify({"message": "Item updated", "item": item.to_dict()})

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item); db.session.commit()
    return jsonify({"message": "Item deleted", "id": item_id})

if __name__ == "__main__":
    app.run("""""")
