from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, User, PrivateReview, Review, reviews_schema, review_schema, private_review_schema, private_reviews_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'Working?': 'Yes'}

@api.route('/reviews', methods = ['POST'])
@token_required
def create_review(current_user_token):
    show = request.json['show']
    author = request.json['author']
    rating = request.json['rating']
    review = request.json['review']
    user_token = current_user_token.token

    review = Review(show, author, rating, review, user_token = user_token )

    db.session.add(review)
    db.session.commit()

    response = review_schema.dump(review)
    return jsonify(response)

@api.route('/reviews', methods = ['GET'])
@token_required
def get_review(current_user_token):
    reviews = Review.query.all()
    response = reviews_schema.dump(reviews)
    return jsonify(response)

@api.route('/reviews/<id>', methods = ['GET'])
@token_required
def get_single_review(id):
    review = Review.query.get(id)
    response = review_schema.dump(review)
    return jsonify(response)

@api.route('/reviews/<id>', methods = ['POST','PUT'])
@token_required
def update_review(current_user_token, id):
    review = Review.query.get(id) 
    if review.user_token != current_user_token.token:
        print('Wrong user token')
        return
    review.show = request.json['show']
    review.author = request.json['author']
    review.rating = request.json['rating']
    review.review = request.json['review']
    

    db.session.commit()
    response = private_review_schema.dump(review)
    return jsonify(response)

@api.route('/reviews/<id>', methods = ['DELETE'])
@token_required
def delete_review(current_user_token, id):
    review = Review.query.get(id)
    if review.user_token != current_user_token.token:
        print('Wrong user token')
        return
    db.session.delete(review)
    db.session.commit()
    response = review_schema.dump(review)
    return jsonify(response)

@api.route('/privatereviews', methods = ['POST'])
@token_required
def create_private_review(current_user_token):
    show = request.json['show']
    rating = request.json['rating']
    review = request.json['review']
    user_token = current_user_token.token

    review = PrivateReview(show, rating, review, user_token = user_token )

    db.session.add(review)
    db.session.commit()

    response = private_review_schema.dump(review)
    return jsonify(response)

@api.route('/privatereviews', methods = ['GET'])
@token_required
def get_private_review(current_user_token):
    a_user = current_user_token.token
    reviews = PrivateReview.query.filter_by(user_token = a_user).all()
    response = private_reviews_schema.dump(reviews)
    return jsonify(response)

@api.route('/privatereviews/<id>', methods = ['GET'])
@token_required
def get_single_private_review(current_user_token, id):
    review = PrivateReview.query.get(id)
    if review.user_token != current_user_token.token:
        print('Wrong user token')
        return
    response = private_review_schema.dump(review)
    return jsonify(response)

@api.route('/privatereviews/<id>', methods = ['POST','PUT'])
@token_required
def update_private_review(current_user_token, id):
    review = PrivateReview.query.get(id) 
    if review.user_token != current_user_token.token:
        print('Wrong user token')
        return
    review.show = request.json['show']
    review.rating = request.json['rating']
    review.review = request.json['review']
    

    db.session.commit()
    response = private_review_schema.dump(review)
    return jsonify(response)

@api.route('/privatereviews/<id>', methods = ['DELETE'])
@token_required
def delete_private_review(current_user_token, id):
    review = PrivateReview.query.get(id)
    if review.user_token != current_user_token.token:
        print('Wrong user token')
        return
    db.session.delete(review)
    db.session.commit()
    response = private_review_schema.dump(review)
    return jsonify(response)
