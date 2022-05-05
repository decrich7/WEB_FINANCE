from data.news import News
from data.users import User
from data import db_session
from flask import jsonify
from flask_restful import Resource
from stoks import Stock
import json
from file_portfel import csv_file
import datetime as dt
from flask_restful import reqparse
import os

parser = reqparse.RequestParser()
parser.add_argument('length_invest_horizon', required=True)
parser.add_argument('shorts', required=True)
parser.add_argument('tikets', required=True)
parser.add_argument('is_private', required=True)
parser.add_argument('name_portfel', required=True)
parser.add_argument('id_user', required=True, type=int)
parser.add_argument('budget', required=True, type=int)


class Briefcase(Resource):
    def get(self, id_user):
        db_sess = db_session.create_session()
        data = {}
        for i in db_sess.query(News).filter(News.id_file == id_user):
            data[i.id] = {
                'name_portfel': i.name_portfel,
                'created_date': i.created_date,
                'horiz': i.horiz,
                'short': i.short,
                'money': i.money,
                'tikets': i.tikets,
                'yield_persent': i.yield_persent
            }

        return jsonify(data)

    def post(self, id_user):
        args = parser.parse_args()
        data = {
            'length_invest_horizon': args['length_invest_horizon'],
            'budget': args['budget'],
            'shorts': args['shorts'],
            'name_portfel': args['name_portfel'],
            'tikets': args['tikets'],
            'is_private': args['is_private'],
            'id_user': args['id_user']
        }

        if int(data['length_invest_horizon']) == 1:
            mon_stoks = int(data['budget']) * 0.2

        elif int(data['length_invest_horizon']) == 3:
            mon_stoks = int(data['budget']) * 0.3

        elif int(data['length_invest_horizon']) == 5:
            mon_stoks = int(data['budget']) * 0.5

        stock = Stock(tickers=str(data['tikets']).split(), money=mon_stoks, shorts=bool(data['shorts']))
        sharp = stock.sharp()
        profit = stock.profit()

        volatility = stock.volatility()
        path_vol = stock.plot_equal_volatility(id_user)
        path_sharp = stock.plot_equal_sharp(id_user)
        path = stock.plot(id_user)


        db_sess = db_session.create_session()
        news = News()
        current_user = db_sess.query(User).filter(User.id == data['id_user']).first()
        news.name_portfel = data['name_portfel']
        news.tikets = data['tikets']
        news.is_private = True if data['is_private'] == 'True' else False
        news.horiz = int(str(data['length_invest_horizon']).split()[0])
        news.short = bool(data['shorts'])
        news.short = True if data['shorts'] == 'True' else False
        news.id_file = current_user.id
        news.yield_persent = profit
        news.money = data['budget']
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()

        dict_data = {
            'success': 'OK',
            'id': db_sess.query(News).filter(News.user_id == data['id_user'])[-1].id,
            'time': dt.datetime.now().strftime("%d-%m-%Y"),
            'stoks': {
                'volatility': {
                    'stoks_and_count': volatility[0],
                    'balance': volatility[1]
                },
                'sharp': {
                    'stoks_and_count': sharp[0],
                    'balance': sharp[1]
                }
            },
            'yield': profit,
            'path': path,
            'path_sharp': path_sharp,
            'path_vol': path_vol
        }

        with open(
                f"json_data/{current_user.id}_{db_sess.query(News).filter(News.user_id == data['id_user'])[-1].id}.json",
                'w') as cat_file:
            json.dump(dict_data, cat_file)
        csv_file(current_user.name, dict_data, db_sess.query(News).filter(News.user_id == data['id_user'])[-1].id)
        return jsonify(dict_data)

    def delete(self, id_user):
        db_sess = db_session.create_session()
        port = db_sess.query(News).filter(News.id == id_user).first()
        os.remove(f'json_data/{port.id_file}_{id_user}.json')
        if port:
            db_sess.delete(port)
            db_sess.commit()
        return jsonify({'resalt': f'port {id_user} deleted'})
