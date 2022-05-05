

# Õ≈ »—œŒÀ‹«”≈“—ﬂ


from flask import make_response
from flask_restful import Resource
from stoks import Stock
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('length_invest_horizon', required=True)
parser.add_argument('shorts', required=True)
parser.add_argument('tikets', required=True)
parser.add_argument('is_private', required=True)
parser.add_argument('name_portfel', required=True)
parser.add_argument('id_user', required=True, type=int)
parser.add_argument('budget', required=True, type=int)


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
