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
            gc.balance,
            p.description,
            p.name,
            p.product_id,
            pi.image
        FROM 
            GiftCards gc
        JOIN 
            Products p ON gc.product_id = p.product_id
        JOIN
            ProductImages pi ON p.product_id = pi.product_id
        WHERE 
            pi.is_primary = TRUE
        GROUP BY 
            gc.balance, p.description, p.name, p.product_id, pi.image;
    """
    gift_cards = fetchAll(sql_giftcards, None, True)
    print(gift_cards)

    sql_giftcards_redeem = """
        SELECT 
            GiftCards.product_id, 
            GiftCards.gift_card_id, 
            GiftCards.code, 
            GiftCards.balance, 
            Orders.order_date,
            Orders.user_id,
            CONCAT(Consumer.given_name, ' ', Consumer.family_name) AS full_name 
        FROM 
            GiftCards
        JOIN 
            Orders ON GiftCards.order_id = Orders.order_id
        JOIN
            Consumer ON Orders.user_id = Consumer.user_id;
    """
    print(gift_cards)
    gift_cards_redeem = fetchAll(sql_giftcards_redeem, None, True)
    return render_template('manage-giftcards.html',giftcards=gift_cards,  giftcardsRedeem=gift_cards_redeem)


