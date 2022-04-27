from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, RadioField, SelectField, IntegerField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    name_portfel = StringField('Имя портфеля', validators=[DataRequired()])
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')
    goriz = RadioField('Укажите длину инвестиционного горизонта', choices=['1 год', '3 года', '5 лет'])
    short = RadioField('Учитывать короткие позиции по ценным бумагам при анализе?', choices=['Да', 'Нет'])
    money = IntegerField('Введите ваш бюджет (в валюте)')
    tikets = StringField('Введите тикеты акций')
