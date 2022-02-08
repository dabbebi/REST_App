from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os
from flask_cors import CORS

# Init app
app = Flask(__name__)
#config headers
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Post Class/Model
class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  post = db.Column(db.String(300))
  

  def __init__(self, name, post):
    self.name = name
    self.post = post

# Post Schema
class PostSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'post')

# Init schema
post_schema = PostSchema()
posts_schema = PostSchema(many=True)

# Create a Post
@app.route('/post', methods=['POST'])
def add_post():
  name = request.json['name']
  post = request.json['post']

  new_post = Post(name, post)

  db.session.add(new_post)
  db.session.commit()

  return post_schema.jsonify(new_post)

# Get All Posts
@app.route('/post', methods=['GET'])
def get_posts():
  all_posts = Post.query.all()
  result = posts_schema.dump(all_posts)
  return jsonify(result)

# Get Single Post
@app.route('/post/<id>', methods=['GET'])
def get_post(id):
  post = Post.query.get(id)
  return post_schema.jsonify(post)

# Update a Post
@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
  my_post = Post.query.get(id)

  name = request.json['name']
  post = request.json['post']

  my_post.name = name
  my_post.post = post

  db.session.commit()

  return post_schema.jsonify(my_post)

# Delete Post
@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
  post = Post.query.get(id)
  db.session.delete(post)
  db.session.commit()

  return post_schema.jsonify(post)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)