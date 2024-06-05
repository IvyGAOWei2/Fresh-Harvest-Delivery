from app import app
from flask import render_template, request
from dbFile.config import fetchAll, updateSQL

# User-defined function
from dbFile.config import updateSQL, insertSQL
from common import roleRequired, validateProductProfile

@app.route("/giftcards/list", methods = ["GET"])
@roleRequired(['National_Manager'])
def manageGiftcard():
    sql_giftcards = """
        SELECT 
            GiftCards.product_id, 
            GiftCards.gift_card_id, 
            GiftCards.code, 
            GiftCards.balance, 
            Orders.order_date,
            Orders.user_id,
            Products.description,
            CONCAT(Consumer.given_name, ' ', Consumer.family_name) AS full_name 
        FROM 
            GiftCards
        JOIN 
            Orders ON GiftCards.order_id = Orders.order_id
        JOIN 
            Products ON GiftCards.product_id = Products.product_id
        JOIN
            Consumer ON Orders.user_id = Consumer.user_id;
    """
    gift_cards = fetchAll(sql_giftcards, None, True)
    return render_template('manage-giftcards.html', giftcards=gift_cards)


