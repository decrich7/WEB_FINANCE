from data.news import News
from data.users import User
from data import db_session
from flask import jsonify
from flask_restful import Resource
from stoks import Stock
from flask import jsonify

import json
from file_portfel import csv_file
import datetime as dt
from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)



class Users(Resource):
    def get(self, id_user):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id_user).first()
        return jsonify({
            'id': user.id,
            'email': user.email,
            'data_create': user.created_date
        })

    def post(self, id_user):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        user = User(
            name=args['name'],
            email=args['email'],
            hashed_password=args['password']
        )
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'status': f"user {id_user} created"})


    def delete(self, id_user):
        db_sess = db_session.create_session()
        db_sess.query(User).filter(User.id == id_user).delete()
        db_sess.commit()
        return jsonify({'status': f"user {id_user} deleted"})
