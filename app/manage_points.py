from datetime import datetime
from app import app
from flask import render_template, request, session

# User-defined function
from dbFile.config import insertSQL, updateSQL,fetchAll, fetchOne
from common import toDay, roleRequired


@app.route("/manage/points", methods=['GET', 'POST'])
@roleRequired(['Local_Manager', 'National_Manager'])
def managePoints():
    type = session['type']

    points_list = fetchAll("""WITH LatestPoints AS 
             (SELECT user_id, MAX(point_id) AS latest_point_id FROM ConsumerPoints GROUP BY user_id)
            SELECT u.given_name,u.family_name,u.depot_id,
                Depots.location,           
                p.*  
            FROM Consumer u JOIN LatestPoints lp ON u.user_id = lp.user_id
            JOIN ConsumerPoints p ON p.point_id = lp.latest_point_id
            JOIN Depots on Depots.depot_id = u.depot_id;""", val=None, withDescription=False)
        
    return render_template('manage_points.html', type=type, points_list=points_list)


@app.route("/manage/points/details", methods=['POST'])
@roleRequired(['Local_Manager', 'National_Manager'])
def managePointsDetails():
    type = session['type']
    user_id = request.form.get('user_id')

    points_list = fetchAll("""WITH LatestPoints AS 
             (SELECT user_id, MAX(point_id) AS latest_point_id FROM ConsumerPoints GROUP BY user_id)
            SELECT u.given_name,u.family_name,u.depot_id,
                Depots.location,           
                p.*  
            FROM Consumer u JOIN LatestPoints lp ON u.user_id = lp.user_id
            JOIN ConsumerPoints p ON p.point_id = lp.latest_point_id
            JOIN Depots on Depots.depot_id = u.depot_id;""", val=None, withDescription=False)
    
    
    user_details = fetchAll("SELECT * FROM ConsumerPoints WHERE user_id = %s", (user_id,), withDescription=False)
    
    return render_template('manage_points.html', type=type, user_details=user_details,show_modal=True, points_list=points_list)
    
   
@app.route("/manage/points/update", methods=['POST'])
@roleRequired(['Local_Manager', 'National_Manager'])
def manageupdate():
  
    user_id = request.form.get('user_id')
    point_balance = request.form.get('point_balance')
    print(user_id,point_balance)
    
    
    point_variation = float(request.form.get('point_variation'))
    new_points = float(point_balance) + point_variation
    current_date = datetime.now().date()
    update_successful = insertSQL("insert into ConsumerPoints(point_id, user_id,point_type,point_variation,point_balance,point_date) values(default,%s,'Placeholder1',%s,%s,%s)", (user_id,point_variation,new_points,current_date))
        
    if update_successful:
        return {"status": True}, 200
    else:
        return {"status": False}, 500


   
    