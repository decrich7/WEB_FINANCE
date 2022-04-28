import flask_login
from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from requests import get, post
from forms.news import NewsForm
from forms.user import RegisterForm, LoginForm
from data.news import News
from data.users import User
from data import db_session
import json
from info_main.course_val import get_course
from info_main.brokers import get_brokers
from info_main.up_down import get_liders
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/finanse.db")
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    app.run(port=80, host='127.0.0.1')



@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():

        r = post('http://127.0.0.1:5000/api/v2/briefcase', json={
                    'length_invest_horizon': int(str(form.goriz.data).split()[0]),
                    'budget': form.money.data,
                    'shorts': True if form.short.data == 'Да' else False,
                    'name_portfel': form.name_portfel.data,
                    'tikets': form.tikets.data,
                    'is_private': form.is_private.data,
                    'id_user': flask_login.current_user.id
                }).json()
        # db_sess = db_session.create_session()
        # news = News()
        # news.name_portfel = form.name_portfel.data
        # # news.content = form.content.data
        # news.tikets = form.tikets.data
        # news.is_private = form.is_private.data
        # news.horiz = int(str(form.goriz.data).split()[0])
        # news.short = True if form.short.data == 'Да' else False
        # news.money = form.money.data
        # current_user.news.append(news)
        # db_sess.merge(current_user)
        # db_sess.commit()
        return redirect(f'/info/{r["id"]}')
    return render_template('news.html', title='Добавление новости', form=form)




@app.route('/info/<int:id>', methods=['GET', 'POST'])
@login_required
def info(id):
    # db_sess = db_session.create_session()
    # news = db_sess.query(News).filter((News.user == current_user) | (News.is_private != True))
    # print(current_user)
    # import requests
    # print(get(f'http://127.0.0.1:5000/api/v2/briefcase/{flask_login.current_user.id}'))
    # return render_template('news.html', title='Добавление новости')
    # print(flask_login.current_user.id)

    with open(f'json_data/{flask_login.current_user.id}_{id}.json') as cat_file:
        data = json.load(cat_file)
        price = list()
        price_vol = list()
        stoks = data["stoks"]
        for i, k in stoks.get('sharp').get('stoks_and_count').items():
            s = [i, k]
            price.append(s)

        for v, k in stoks.get('volatility').get('stoks_and_count').items():
            s = [v, k]
            price_vol.append(s)

        # msg = f"📈 Формирование портфеля по максимальному коэфициенту Шарпа:" + \
        #       f'\n{"".join(price)}\n' + \
        #       f"\n💵 Остаток средств(по Шарпу)  - {stoks.get('sharp').get('balance')}\n" + \
        #       f'\n📌 Формирование портфеля по минимальной волатильности:' + \
        #       f'\n{"".join(price_vol)}\n' + \
        #       f'\n💵 Остаток средств(Волантильность) - {stoks.get("volatility").get("balance")}\n' + \
        #       f'\n📅 Дата формирования портфелей: {data["time"]}\n' + \
        #       f'\n💰 Годовой доход: {data["yield"]}'
    return render_template('Site2/index.html', list_sharp=price, list_vol=price_vol, path_csv=f'/static/csv_port/portfolio_stoks_{flask_login.current_user.name}_{id}.csv')



@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/main_page')


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    # form = NewsForm()
    # if request.method == "GET":
    #     db_sess = db_session.create_session()
    #     news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
    #     if news:
    #         form.name_portfel.data = news.name_portfel
    #         form.is_private.data = news.is_private
    #     else:
    #         abort(404)
    # if form.validate_on_submit():
    #     db_sess = db_session.create_session()
    #     news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
    #     if news:
    #         news.name_portfel = form.name_portfel.data
    #         news.is_private = form.is_private.data
    #         db_sess.commit()
    #         return redirect('/')
    #     else:
    #         abort(404)

    with open(f'json_data/{flask_login.current_user.id}_{id}.json') as cat_file:
        data = json.load(cat_file)
        price = list()
        price_vol = list()
        stoks = data["stoks"]
        for i, k in stoks.get('sharp').get('stoks_and_count').items():
            s = [i, k]
            price.append(s)

        for v, k in stoks.get('volatility').get('stoks_and_count').items():
            s = [v, k]
            price_vol.append(s)
    return render_template('Site2/index.html', list_sharp=price, list_vol=price_vol, path_csv=f'/static/csv_port/portfolio_stoks_{flask_login.current_user.name}_{id}.csv')


    # return render_template('news.html', title='Редактирование новости', form=form)


@app.route("/")
def index():
    # db_session.global_init("db/blogs.db")
    # db_sess = db_session.create_session()
    # if current_user.is_authenticated:
    #     news = db_sess.query(News).filter((News.user == current_user) | (News.is_private != True))
    # else:
    #     news = db_sess.query(News).filter(News.is_private != True)
    return render_template("Главная/index.html")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        print(form.name.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/main_page')
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/main_page', methods=['GET', 'POST'])
@login_required
def main_page():
    list_course = get_course()
    # list_brokers = get_brokers()
    # print(len(list_brokers))
    kort_up_down = get_liders()
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter((News.user == current_user))
    return render_template("index.html", news=news, list_course=list_course, list_up=kort_up_down[-1], list_down=kort_up_down[0])



if __name__ == '__main__':
    main()
