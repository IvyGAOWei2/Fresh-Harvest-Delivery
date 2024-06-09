from app import app
from flask import render_template, request, session

# User-defined function
from dbFile.config import insertSQL, updateSQL, fetchAll
from common import roleRequired, saveImage


@app.route("/admin/post/news")
@roleRequired(['Local_Manager', 'National_Manager'])
def manageNews():
    if session['depot_id'] == 6:
        news = fetchAll("SELECT * FROM News WHERE is_deleted = False;", None, True)
    else:
        news = fetchAll("SELECT * FROM News WHERE depot_id = %s AND is_deleted = False;", (session['depot_id'],), True)
    return render_template('manage_news.html', news=news, depotList=app.depot_list,)

@app.route("/news/add", methods=['POST'])
@roleRequired(['Local_Manager', 'National_Manager'])
def addNews():
    try:
        data = dict(request.form)
        image_name = saveImage(app.config['UPLOAD_FOLDER'], request.files['image'])

        add_successful = insertSQL("INSERT INTO News (title, subtitle, content, date, image, depot_id) VALUES (%s,%s,%s,%s,%s,%s);", \
            (data['title'], data['subtitle'], data['content'], data['date'], image_name, data['depot_id']))
        return {"status": bool(add_successful)}, 200 if add_successful else 500
    except:
        return {"status": False}, 500

@app.route("/news/update", methods=['POST'])
@roleRequired(['Local_Manager', 'National_Manager'])
def updateNews():
    try:
        data = dict(request.form)

        news_id = data['news_id']
        data.pop('news_id')

        if data:
            updates,params = [], []
            for key, value in data.items():
                updates.append(f"{key} = %s")
                params.append(value)
            params.append(news_id)

        update_successful = updateSQL("UPDATE News SET " + ", ".join(updates) + " WHERE news_id = %s", params)

        image = request.files['image']
        if image.filename:
            image_name = saveImage(app.config['UPLOAD_FOLDER'], image)
            update_successful = updateSQL("UPDATE News SET image = %s WHERE news_id = %s", (image_name, news_id))

        return {"status": bool(update_successful)}, 200 if update_successful else 500
    except:
        return {"status": False}, 500

@app.route("/news/del", methods=['POST'])
@roleRequired(['Local_Manager', 'National_Manager'])
def deleteNews():
    data = request.get_json()
    update_successful = updateSQL("UPDATE News SET is_deleted = TRUE WHERE news_id = %s;", (data['news_id'],))

    if update_successful:
        return {"status": True}, 200
    else:
        return {"status": False}, 500