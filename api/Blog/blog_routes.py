from api.Blog.blog_model import Blog
from api.Tag.tag_model import Tag
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from api import db

blogs = Blueprint('blogs', __name__)

@blogs.route('/blogs', methods=["POST"])
def create_blog():
    """
    Create a Blog
    """
    data = request.get_json()

    new_blog = Blog(title=data["title"], content=data["content"], feature_image=data["feature_image"])

    for tag in data["tags"]:
        present_tag = Tag.query.filter_by(name=Tag).first()
        if(present_tag):
            present_tag.blogs_associated.append(new_blog)
        else:
            new_tag = Tag(name=tag)
            new_tag.blogs_associated.append(new_blog)
            db.session.add(new_tag)

    db.session.add(new_blog)
    db.session.commit()

    blog_id = getattr(new_blog, "id")
    return jsonify({"id": blog_id})

@blogs.route('/blogs', methods=["GET"])
def get_all_blogs():
    """
    Get all Blogs
    """
    blogs = Blog.query.all()
    serialized_data = []
    for blog in blogs:
        serialized_data.append(blog.serialize)
    return jsonify({"all_blogs": serialized_data})

@blogs.route('/blogs/<int:id>', methods=["GET"])
def get_single_blog(id):
    """
    Get a single Blog by id
    """
    blog = Blog.query.filter_by(id=id).first()
    serialized_blog = blog.serialize

    serialized_blog["tags"] = []
    for tag in blog.tags:
        serialized_blog["tags"].append(tag.serialize)

    return jsonify({"single_blog": serialized_blog})

@blogs.route('/blogs/<int:id>', methods=["PUT"])
def update_blog(id):
    data = request.get_json()
    blog = Blog.query.filter_by(id=id).first_or_404()
    
    if data.get('title'):
        blog.title = data['title']
    if data.get('content'):
        blog.content = data['content']
    if data.get('feature_image'):
        blog.feature_image = data['feature_image']

    update_blog = blog.serialize

    db.session.commit()
    return jsonify({"blog": update_blog})

@blogs.route('/blogs/<int:id>', methods=["DELETE"])
@jwt_required
def delete_blog(id):
    blog = Blog.query.filter_by(id=id).first_or_404()
    db.session.delete(blog)
    db.session.commit()
    return jsonify("Blog delete"), 200