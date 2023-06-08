from flask import Flask, render_template, request, flash, redirect, url_for
import mysql.connector


# MYSQL CONNECTOR
table = "VIDEOGAME"

mydb = mysql.connector.connect(
  host="localhost",
  user="giocas1",
  password="qwerty",
  database="GameStart"
)
mycursor = mydb.cursor()
table_names = ['BOOKS', 'VIDEOGAME', 'CONSOLE', 'TOYS_AND_FIGURES', 'CONTROLLER']
loc_products = ['LOC_VIG', 'LOC_CNS', 'LOC_CNT', 'LOC_BOK', 'LOC_TYF']

# Queries for Home Page
for name in table_names:
    mycursor.execute(f"select * from {name}")
    data = mycursor.fetchall()

VIDEOGAMES_data = data[1]
CONSOLE_data = data[2]
TOYS_FIGS_data = data[3]
CONTROLLER_data = data[4]


# FLASK
app = Flask(__name__)
app.secret_key = 'kj34t2hj76iuy544t'


@app.route('/', methods=['GET'])
def index():
    data = []

    for name1 in table_names:
        mycursor.execute(f"select * from {name1}")
        data.extend(mycursor.fetchall())

    return render_template('index.html', data=data)


@app.route('/search_category', methods=['GET'])
def search_category():
    category = request.args.get('category')
    mycursor.execute(f"select * from {category}")
    category_data = mycursor.fetchall()

    return render_template('search_category.html', queries=category_data, category=category)


@app.route('/product', methods=['GET'])
def product():
        ISBN = request.args.get('isbn')
        product_data = []
        location_data = []

        for name2 in table_names:
            mycursor.execute(f"select * from {name2} where ISBN = '{ISBN}';")
            product_data.extend(mycursor.fetchall())

        for row in loc_products:
            mycursor.execute(f"select * from {row} where ISBN = '{ISBN}';")
            location_data.extend(mycursor.fetchall())

        return render_template('product.html', products=product_data, isbn=ISBN, locations=location_data)


@app.route('/search_item', methods=['GET', 'POST'])
def search_item():
    if request.method == 'POST':
        item = request.form['item']
        data = []

        for name3 in table_names:
            mycursor.execute(f"select * from {name3} where title like '%%{item}%%';")
            data.extend(mycursor.fetchall())

        if data:
            return render_template('search_category.html', queries=data, item=item)
        else:
            return render_template('404.html')

    return render_template('search_item.html')


@app.route('/cancel_pre_order', methods=['GET', 'POST'])
def cancel_pre_order():
    if request.method == 'POST':
        order_input = request.form['order_input']

        mycursor.execute(f"select order_id from PREORDERS where order_id = '{order_input}';")
        order_id = mycursor.fetchone()

        if order_id is not None and order_input == order_id[0]:
            mycursor.execute(f"delete from PREORDERS where order_id = '{order_input}';")
            flash(f'Pre order for cancelled successfully!', 'success')
            return redirect(url_for('cancel_pre_order'))
        else:
            flash(f'Pre order not found. Please try again', 'error')
            return redirect(url_for('cancel_pre_order'))

    return render_template('cancel_pre_order.html')


@app.route('/location')
def location():
    mycursor.execute(f"select * from STORE")
    locations = mycursor.fetchall()

    return render_template('location.html', locations=locations)


@app.route('/error')
def error():
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)

