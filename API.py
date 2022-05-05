# -*- coding: utf-8 -*-
from resurses.briefcase import Briefcase
from resurses.test import Test
from data import db_session
from flask import Flask
from flask_restful import Api
from resurses.user import Users


app = Flask(__name__)
api = Api(app)
db_session.global_init("db/finanse.db")




def main():
    api.add_resource(Briefcase, '/api/v2/briefcase/<int:id_user>')
    api.add_resource(Test, '/api/v2/test/<int:id_img>')
    api.add_resource(Users, '/api/v2/user/<int:id_user>')
    # db_session.global_init("db/db_users.db")
    app.run()


if __name__ == '__main__':
    main()
