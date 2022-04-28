# -*- coding: utf-8 -*-
from data.news import News
from data.users import User
from data import db_session
from flask import Flask, make_response
from flask_restful import Api
from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse
from stoks import Stock
import json
from file_portfel import csv_file
import os
import datetime as dt

app = Flask(__name__)
api = Api(app)
db_session.global_init("db/finanse.db")

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
        # db_sess = db_session.create_session()
        # print(id_user)
        # news = db_sess.query(News).filter(News.user_id == int(id_user))
        # for i in news:
        # print(i.money)
        print(1)
        return 'ok'

    def post(self):
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
        #
        # db_sess = db_session.create_session()
        # news = News()
        # current_user = db_sess.query(User).filter(User.id == data['id_user']).first()
        # news.name_portfel = data['name_portfel']
        # news.tikets = data['tikets']
        # news.is_private = True if data['is_private'] == 'True' else False
        # news.horiz = int(str(data['length_invest_horizon']).split()[0])
        # news.short = bool(data['shorts'])
        # news.short = True if data['shorts'] == 'True' else False
        # news.id_file = current_user.id
        # news.money = data['budget']
        # current_user.news.append(news)
        # db_sess.merge(current_user)
        # db_sess.commit()

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
        }

        with open(
                f"json_data/{current_user.id}_{db_sess.query(News).filter(News.user_id == data['id_user'])[-1].id}.json",
                'w') as cat_file:
            json.dump(dict_data, cat_file)
        csv_file(current_user.name, dict_data, db_sess.query(News).filter(News.user_id == data['id_user'])[-1].id)
        return jsonify(dict_data)


class Test(Resource):

    def post(self, id_img):
        args = parser.parse_args()
        news = {
            'date': args['date'],
            'length_invest_horizon': args['length_invest_horizon'],
            'budget': args['budget'],
            'tg_id': args['tg_id'],
            'shorts': args['shorts']
        }
        if int(news['length_invest_horizon']) == 1:
            mon_stoks = int(news['budget']) * 0.2
            mon_bonds = int(news['budget']) * 0.8

        elif int(news['length_invest_horizon']) == 3:
            mon_stoks = int(news['budget']) * 0.3
            mon_bonds = int(news['budget']) * 0.7

        elif int(news['length_invest_horizon']) == 5:
            mon_stoks = int(news['budget']) * 0.5
            mon_bonds = int(news['budget']) * 0.5

        stock = Stock(money=mon_stoks, shorts=bool(news['shorts']))
        stock.sharp()
        stock.volatility()
        if id_img == 1:
            name_file = stock.plot()
        elif id_img == 2:
            name_file = stock.plot_equal_sharp()
        elif id_img == 3:
            name_file = stock.plot_equal_volatility()

        with open(name_file, 'rb') as file:
            image_binary = file.read(-1)
        response = make_response(image_binary)
        response.headers.set('Content-Type', 'image/png')
        response.headers.set(
            'Content-Disposition', 'attachment', filename=name_file)
        return response


def main():
    api.add_resource(Briefcase, '/api/v2/briefcase')
    api.add_resource(Test, '/api/v2/test/<int:id_img>')
    # db_session.global_init("db/db_users.db")
    app.run()


if __name__ == '__main__':
    main()
