from app import app
from flask import render_template, session, request
from dbFile.config import fetchOne, fetchAll
from emailMethod.method import sendFhdContact
from common import fakeReview

@app.route("/")
def index():
    print(session)
    sql = "SELECT description, discount_rate FROM Discounts WHERE status = 1 ORDER BY start_date DESC LIMIT 1"
    discount = fetchOne(sql, [])

    # Ensure discount is not None and extract the description and discount rate
    discount_description = discount[0] if discount else 'New discounts available soon.'
    discount_rate = discount[1]if discount else '10'
    discount = {'description': discount_description, 'rate': f'{discount_rate}% OFF'}

    if 'depot_id' not in session or session['depot_id'] == 6:
        depot_id = 1
    else:
        depot_id = session['depot_id']

    news = fetchAll("SELECT * FROM News WHERE depot_id = %s AND is_deleted = False;", (depot_id,), True)

    sql = """
        SELECT 
            p.*, 
            pi.image
        FROM 
            Products p
        INNER JOIN 
            ProductImages pi ON p.product_id = pi.product_id
        WHERE 
            p.category_id = %s 
            AND p.depot_id = %s 
        ORDER BY 
            RAND() 
        LIMIT 2;
    """
    tablist1 = fetchAll(sql,(app.category_list[0]['category_id'], depot_id),True)
    tablist2 = fetchAll(sql,(app.category_list[1]['category_id'], depot_id),True)
    tablist3 = fetchAll(sql,(app.category_list[2]['category_id'], depot_id),True)
    tablist4 = fetchAll(sql,(app.category_list[3]['category_id'], depot_id),True)
    combined_list = tablist1 + tablist2 + tablist3 + tablist4

    best_seller = fetchAll("SELECT p.name, p.price,p.product_id, pi.image FROM Products p \
        INNER JOIN ProductImages pi ON p.product_id = pi.product_id \
        WHERE category_id = 1 AND p.depot_id = %s ORDER BY RAND() LIMIT 6;", (depot_id,), True)

    return render_template('index.html', discount=discount, news=news, shipping=app.shipping, \
        categoryList=app.category_list,unitList=app.unit_list, reviews=fakeReview(), best_seller=best_seller,
        tablist1=tablist1,tablist2=tablist2,tablist3=tablist3,tablist4=tablist4, combined_list=combined_list)

@app.route("/404")
def notFound():
    return render_template('404.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact", methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        data = request.form.to_dict()

        if app.send_email:
            sendFhdContact(data['name'], data['email'], data['type'], data['msg'])
        return {"status": True}, 200
    return render_template('contact.html')

@app.route("/exmaples")
def exmaples():
    return render_template('exmaples.html')