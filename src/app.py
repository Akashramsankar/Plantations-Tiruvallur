from datetime import datetime
from datetime import timedelta
import pymongo
import os
import sys
import pandas as pd
import codecs
import gridfs
from bson import json_util
from bson.objectid import ObjectId
from flask import Flask, render_template, request, session, json, abort
from src.common.database import Database
from src.models.plantations import Plantation
from src.models.watering import Watering
from src.models.overseers import Overseer
from src.models.users import User
app = Flask(__name__)  # main
app.secret_key = "commercial"
@app.before_first_request
def initialize_database():
    Database.initialize()
@app.route('/')
def home():
    # remote_address = request.headers.getlist("X-Forwarded-For")[0]
    return render_template('home.html')
@app.route('/login')
def login_form():
    return render_template('login.html')
@app.route('/register')
def register_form():
    return render_template('register.html')
@app.route('/profile_landing')
def profile():
    email = session['email']
    user = User.get_by_email(email)
    if email:
        if user.designation == 'HQ Staff':
            return render_template('profile_HQ.html', user=user)
        else:
            return render_template('profile_blocks.html', user=user)
    else:
        return render_template('login_fail.html')
@app.route('/authorize/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    valid = User.valid_login(email, password)
    User.login(email)
    user = User.get_by_email(email)
    if valid:
        if user.designation == 'HQ Staff':
            return render_template('profile_HQ.html', user=user)
        else:
            return render_template('profile_blocks.html', user=user)
    else:
        return render_template('login_fail.html')
@app.route('/authorize/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    username = request.form['username']
    designation = request.form['designation']
    block = request.form['block']
    User.register(email, password, username, designation, block)
    user = User.get_by_email(email)
    if user.designation == 'HQ Staff':
        return render_template('profile_HQ.html', user=user)
    else:
        return render_template('profile_blocks.html', user=user)
@app.route('/loggedOut')
def log_out():
    email = session['email']
    user = User.get_by_email(email)
    if email is not None:
        user.logout()
        return render_template('logged_out.html', user=user.username)
    else:
        return render_template('login_fail.html')
@app.route('/add_plantation/<string:user_id>', methods=['POST', 'GET'])
def plantation_form(user_id):
    email = session['email']
    if email is not None:
        if request.method == 'GET':
            user = User.get_by_id(user_id)
            return render_template('add_plantation.html', user=user)
        else:
            user = User.get_by_id(user_id)
            typeOfPlantation = request.form['typeOfPlantation']
            typeOfCrop = request.form['typeOfCrop']
            block = request.form['Blocks']
            plotNo = request.form['plotNo']
            hectre = request.form['hectre']
            workName = request.form['workName']
            totalPits = request.form['totalPits']
            totalSanctionedPlants = request.form['totalSanctionedPlants']
            costOfCrops = request.form['costOfCrops']
            plantationDate = request.form['plantationDate']
            panchayat = request.form['panchayat']
            habitation = request.form['habitation']
            overseer = request.form['overseer']
            typeOfRoad = request.form['typeOfRoad']
            KM = request.form['KM']
            user_id = user_id
            user_name = user.username
            plantation = Plantation(typeOfPlantation=typeOfPlantation,typeOfCrop=typeOfCrop, hectre=hectre, typeOfRoad=typeOfRoad,
                                    workName=workName, totalPits=totalPits, block=block, plotNo=plotNo, KM=KM,
                                    costOfCrops=costOfCrops, plantationDate=plantationDate, totalSanctionedPlants=totalSanctionedPlants,
                                    user_id=user_id, user_name=user_name, panchayat=panchayat, habitation=habitation,overseer=overseer,plantationStatus="Open")
            plantation.save_to_mongo()
            if user.designation == 'HQ Staff':
                return render_template('application_added.html', plantation=plantation, user=user)
            else:
                return render_template('application_added_blocks.html', plantation=plantation, user=user)
    else:
            return render_template('login_fail.html')
@app.route('/ViewAllPlantations')
def view_all_plantations():
    plantation = []
    plantation_dict = Database.find("plantations", {})
    for tran in plantation_dict:
        plantation.append(tran)
    single_plantation = json.dumps(plantation, default=json_util.default)
    return single_plantation
@app.route('/ViewAllOverseers')
def view_all_overseers():
    plantation = []
    plantation_dict = Database.find("oseers", {})
    for tran in plantation_dict:
        plantation.append(tran)
    single_plantation = json.dumps(plantation, default=json_util.default)
    return single_plantation
@app.route('/ViewAllPlantations/<string:block>')
def view_all_plantation_blocks(block):
    plantation = []
    plantation_dict = Database.find("plantations",{"block": block})
    for tran in plantation_dict:
        plantation.append(tran)
    single_plantation = json.dumps(plantation, default=json_util.default)
    return single_plantation
@app.route('/view_plantation')
def view_plantation():
    email = session['email']
    user = User.get_by_email(email)
    if email is not None:
        if user.designation == 'HQ Staff':
              return render_template('view_plantation.html', user=user)
        else:
              block = user.block
              return render_template('view_plantation_blocks.html', user=user, block = block)
    else:
        return render_template('login_fail.html', user=user)
@app.route('/view_overseer')
def view_overseer():
    email = session['email']
    user = User.get_by_email(email)
    if email is not None:
              return render_template('view_overseer.html', user=user)
    else:
        return render_template('login_fail.html', user=user)
@app.route('/raw_plantation/<string:plantation_id>')
def raw_demands_by_plantation_id(plantation_id):
    plantation = []
    plantation_dict = Database.find("plantations", {"plantation_id": plantation_id})
    for tran in plantation_dict:
        plantation.append(tran)
    single_plantation = json.dumps(plantation, default=json_util.default)
    return single_plantation
@app.route('/updateplantation/<string:plantation_id>', methods=['POST', 'GET'])
def update_plantation(plantation_id):
    email = session['email']
    if email is not None:
        if request.method == 'GET':
            user = User.get_by_email(email)
            if user.designation == 'HQ Staff':
                 return render_template('update_plantation_form.html', user=user, plantation_id=plantation_id)
            else:
                 return render_template('update_plantation_form_blocks.html', user=user, plantation_id=plantation_id)
        else:
            user = User.get_by_email(email)
            typeOfPlantation = request.form['typeOfPlantation']
            typeOfCrop = request.form['typeOfCrop']
            block = request.form['Blocks']
            plotNo = request.form['plotNo']
            hectre = request.form['hectre']
            typeOfRoad = request.form['typeOfRoad']
            KM = request.form['KM']
            workName = request.form['workName']
            totalPits = request.form['totalPits']
            survivalRateOfCrops = request.form['survivalRateOfCrops']
            costOfCrops = request.form['costOfCrops']
            totalSanctionedPlants = request.form['totalSanctionedPlants']
            pitsTaken = request.form['pitsTaken']
            pitsToBeTaken = int(totalPits) - int(pitsTaken)
            plantationDate = request.form['plantationDate']
            panchayat = request.form['panchayat']
            habitation = request.form['habitation']
            overseer = request.form['overseer']
            plantationStatus = request.form['plantationStatus']
            user_id = user._id
            user_name = user.username
            plantationDate = datetime.combine(datetime.strptime(plantationDate, '%Y-%m-%d').date(),
                                          datetime.now().time())
            for file in request.files.getlist("Image_upload"):
             filename = file.filename
             # URI = "mongodb://127.0.0.1:27017"
             # client = pymongo.MongoClient(URI)
             # DATABASE = client['Tiruvallur']
             URI = os.environ['MONGODB_URI']
             client = pymongo.MongoClient(URI)
             DATABASE = client['heroku_vcrk1vkq']
             fs = gridfs.GridFS(DATABASE)
             fileid = fs.put(file, filename=filename)
             DATABASE['road_images'].insert_one({"Image_upload": filename, "fileid": fileid, "plantation_id": plantation_id})
        Plantation.update_plantation(typeOfPlantation=typeOfPlantation,typeOfCrop=typeOfCrop, plotNo=plotNo, hectre=hectre, typeOfRoad=typeOfRoad, KM=KM, workName=workName,totalPits=totalPits, survivalRateOfCrops=survivalRateOfCrops, block = block,
        costOfCrops=costOfCrops, plantationDate=plantationDate, plantationStatus=plantationStatus, user_id=user_id, totalSanctionedPlants=totalSanctionedPlants, pitsTaken=pitsTaken, pitsToBeTaken=pitsToBeTaken,
        user_name=user_name, plantation_id=plantation_id, panchayat=panchayat, habitation=habitation, overseer=overseer)
        if user.designation == 'HQ Staff':
            return render_template('application_added.html', user=user)
        else:
            return render_template('application_added_blocks.html', user=user)
    else:
        return render_template('login_fail.html')
@app.route('/viewimageplantation/<string:plantation_id>', methods=['POST', 'GET'])
def preview_image(plantation_id):
    email = session['email']
    user = User.get_by_email(email)
    URI = os.environ['MONGODB_URI']
    client = pymongo.MongoClient(Database.URI)
    DATABASE = client['heroku_vcrk1vkq']
    # URI = "mongodb://127.0.0.1:27017"
    # client = pymongo.MongoClient(URI)
    # DATABASE = client['Tiruvallur']
    fid = ""
    fs = gridfs.GridFS(DATABASE)
    for output_data1 in DATABASE['road_images'].find({'plantation_id': plantation_id}):
            fid = output_data1["fileid"]
    output_data = fs.get(fid).read()
    base64_data = codecs.encode(output_data, 'base64')
    image = base64_data.decode('utf-8')
    if user.designation == 'HQ Staff':
            return render_template('road_image_display.html', images=image, user=user)
    else:
            return render_template('road_image_display_blocks.html', images=image, user=user)
@app.route('/deleteplantation/<string:plantation_id>')
def deleteplantation(plantation_id):
    email = session['email']
    user = User.get_by_email(email)
    Plantation.deletefrom_mongo(plantation_id=plantation_id)
    if user.designation == 'HQ Staff':
        return render_template('deleted.html', user=user)
    else:
        return render_template('deleted_blocks.html', user=user)
@app.route('/Blocks/<string:block_value>')
def get_plantation_by_blocks(block_value):
    plantation = []
    plantation_dict = Database.find("plantations", {"block": block_value})
    for tran in plantation_dict:
        plantation.append(tran)
    single_plantation = json.dumps(plantation, default=json_util.default)
    return single_plantation
@app.route('/view_plantation_by_blocks')
def view_plantation_by_blocks():
    email = session['email']
    user = User.get_by_email(email)
    if email is not None:
              return render_template('view_plantation_by_blocks.html', user=user)
    else:
        return render_template('login_fail.html', user=user)
@app.route('/ViewAllCompletedPlantations')
def view_all_completed_plantation():
    plantation = []
    plantation_dict = Database.find("plantations", {"plantationStatus": "Close"})
    for tran in plantation_dict:
        plantation.append(tran)
    single_plantation = json.dumps(plantation, default=json_util.default)
    return single_plantation
@app.route('/ViewAllOngoingPlantations')
def view_all_ongoing_plantation():
    plantation = []
    plantation_dict = Database.find("plantations", {"plantationStatus": "Open"})
    for tran in plantation_dict:
        plantation.append(tran)
    single_plantation = json.dumps(plantation, default=json_util.default)
    return single_plantation
@app.route('/Completed<string:block_value>')
def get_plantation_by_completion(block_value):
    plantation = []
    plantation_dict = Database.find("plantations", {"$and": [{"block": block_value},
                                                          {"plantationStatus": "Close"}]})
    for tran in plantation_dict:
        plantation.append(tran)
    single_plantation = json.dumps(plantation, default=json_util.default)
    return single_plantation
@app.route('/Ongoing<string:block_value>')
def get_plantation_by_ongoing(block_value):
    plantation = []
    plantation_dict = Database.find("plantations", {"$and": [{"block": block_value},
                                                          {"plantationStatus": "Open"}]})
    for tran in plantation_dict:
        plantation.append(tran)
    single_plantation = json.dumps(plantation, default=json_util.default)
    return single_plantation
@app.route('/ViewAllCompletedPlantations/<string:block>')
def view_all_completed_plantation_blocks(block):
    plantation = []
    plantation_dict = Database.find("plantations", {"$and": [{"block": block},
                                                 {"plantationStatus": "Close"}]})
    for tran in plantation_dict:
        plantation.append(tran)
    single_plantation = json.dumps(plantation, default=json_util.default)
    return single_plantation
@app.route('/ViewAllOngoingPlantations/<string:block>')
def view_all_ongoing_plantation_blocks(block):
    plantation = []
    plantation_dict = Database.find("plantations", {"$and": [{"block": block},
                                                 {"plantationStatus": "Open"}]})
    for tran in plantation_dict:
        plantation.append(tran)
    single_plantation = json.dumps(plantation, default=json_util.default)
    return single_plantation
@app.route('/Completed_plantation')
def Completed_plantation():
    email = session['email']
    user = User.get_by_email(email)
    if email is not None:
        if user.designation == 'HQ Staff':
              return render_template('completed_plantation.html', user=user)
        else:
              block = user.block
              return render_template('completed_plantation_blocks.html', user=user, block = block)
    else:
        return render_template('login_fail.html', user=user)
@app.route('/Ongoing_plantation')
def Ongoing_plantation():
    email = session['email']
    user = User.get_by_email(email)
    if email is not None:
        if user.designation == 'HQ Staff':
              return render_template('ongoing_plantation.html', user=user)
        else:
              block = user.block
              return render_template('ongoing_plantation_blocks.html', user=user, block = block)
    else:
        return render_template('login_fail.html', user=user)
@app.route('/BlockReport/<string:start_date>/<string:end_date>/<string:block>')
def Block_report(start_date, end_date, block):
    all_plantations = []
    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),
                             datetime.now().time())
    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),
                           datetime.now().time())
    all_plantations_dict = Database.find("plantations", {"$and": [{"plantationDate": {"$gte": start, "$lt": end}},
                                                        {"block": block}]})
    for tran in all_plantations_dict:
        all_plantations.append(tran)
    all_p = json.dumps(all_plantations, default=json_util.default)
    return all_p
@app.route('/OverseerReport/<string:start_date>/<string:end_date>/<string:overseer>')
def Overseer_report(start_date, end_date, overseer):
    all_plantations = []
    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),
                             datetime.now().time())
    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),
                           datetime.now().time())
    all_plantations_dict = Database.find("plantations", {"$and": [{"plantationDate": {"$gte": start, "$lt": end}},
                                                        {"overseer": overseer}]})
    for tran in all_plantations_dict:
        all_plantations.append(tran)
    all_p = json.dumps(all_plantations, default=json_util.default)
    return all_p
@app.route('/BlockReportWatering/<string:start_date>/<string:end_date>/<string:block>')
def Block_report_watering(start_date, end_date, block):
    all_waterings = []
    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),
                             datetime.now().time())
    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),
                           datetime.now().time())
    all_waterings_dict = Database.find("waterings", {"$and": [{"asDate": {"$gte": start, "$lt": end}},
                                                        {"block": block}]})
    for tran in all_waterings_dict:
        all_waterings.append(tran)
    all_w = json.dumps(all_waterings, default=json_util.default)
    return all_w
@app.route('/OverallBlockReport/<string:start_date>/<string:end_date>')
def OverallBlockReport(start_date, end_date):
    all_waterings = []
    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),
                             datetime.now().time())
    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),
                           datetime.now().time())
    all_waterings_dict = Database.find("waterings",{"asDate": {"$gte": start, "$lt": end}})
    for tran in all_waterings_dict:
        all_waterings.append(tran)
    all_w = json.dumps(all_waterings, default=json_util.default)
    return all_w
@app.route('/OverallOverseerReport/<string:start_date>/<string:end_date>')
def OverallOverseerReport(start_date, end_date):
    all_waterings = []
    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),
                             datetime.now().time())
    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),
                           datetime.now().time())
    all_waterings_dict = Database.find("waterings",{"asDate": {"$gte": start, "$lt": end}})
    for tran in all_waterings_dict:
        all_waterings.append(tran)
    all_w = json.dumps(all_waterings, default=json_util.default)
    return all_w
@app.route('/OverseerReportWatering/<string:start_date>/<string:end_date>/<string:overseer>')
def Overseer_report_watering(start_date, end_date, overseer):
    all_waterings = []
    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),
                             datetime.now().time())
    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),
                           datetime.now().time())
    all_waterings_dict = Database.find("waterings", {"$and": [{"asDate": {"$gte": start, "$lt": end}},
                                                        {"overseer": overseer}]})
    for tran in all_waterings_dict:
        all_waterings.append(tran)
    all_w = json.dumps(all_waterings, default=json_util.default)
    return all_w
@app.route('/Block_summary', methods=['POST', 'GET'])
def Block_Summary():
    email = session['email']
    user = User.get_by_email(email)
    if email is not None:
        if request.method == 'GET':
            if user.designation == 'HQ Staff':
                   return render_template('between_dates_blockwise.html', user=user)
            else:
                return render_template('between_dates_blockwise_blocks.html', user=user)
        else:
            start_date = request.form['startdate']
            end_date = request.form['enddate']
            if user.designation == 'HQ Staff':
                 block = request.form['block']
                 return render_template('blockwise_summary_sheet.html', user=user, start_date=start_date,
                                        end_date=end_date, block=block)
            else:
                block=user.block
                return render_template('blockwise_summary_sheet_blocks.html', user=user, start_date=start_date,
                                       end_date=end_date, block=block)
    else:
        return render_template('login_fail.html', user=user)
@app.route('/Overall_block_summary', methods=['POST', 'GET'])
def Overall_Block_Summary():
    email = session['email']
    user = User.get_by_email(email)
    if email is not None:
        if request.method == 'GET':

                   return render_template('between_dates_overall_blockwise.html', user=user)
        else:
            start_date = request.form['startdate']
            end_date = request.form['enddate']
            return render_template('overall_blockwise_summary_sheet.html', user=user, start_date=start_date,
                                        end_date=end_date)
    else:
        return render_template('login_fail.html', user=user)
@app.route('/Overall_overseer_summary', methods=['POST', 'GET'])
def Overall_Overseer_Summary():
    email = session['email']
    user = User.get_by_email(email)
    if email is not None:
        if request.method == 'GET':

                   return render_template('between_dates_overall_overseerwise.html', user=user)
        else:
            start_date = request.form['startdate']
            end_date = request.form['enddate']
            return render_template('overall_overseerwise_summary_sheet.html', user=user, start_date=start_date,
                                        end_date=end_date)
    else:
        return render_template('login_fail.html', user=user)
@app.route('/Overseer_summary', methods=['POST', 'GET'])
def Overseer_Summary():
    email = session['email']
    user = User.get_by_email(email)
    if email is not None:
        if request.method == 'GET':
            return render_template('between_dates_overseerwise.html', user=user)
        else:
            start_date = request.form['startdate']
            end_date = request.form['enddate']
            overseer = request.form['overseer']

            return render_template('overseer_summary_sheet.html', user=user, start_date=start_date,
                                   end_date=end_date, overseer=overseer)
    else:
        return render_template('login_fail.html', user=user)
@app.route('/Block_summary_watering', methods=['POST', 'GET'])
def Block_Summary_Watering():
    email = session['email']
    user = User.get_by_email(email)
    if email is not None:
        if request.method == 'GET':
            if user.designation == 'HQ Staff':
                   return render_template('between_dates_watering_blockwise.html', user=user)
            else:
                return render_template('between_dates_watering_blockwise_blocks.html', user=user)
        else:
            start_date = request.form['startdate']
            end_date = request.form['enddate']
            if user.designation == 'HQ Staff':
                 block = request.form['block']
                 return render_template('blockwise_summary_sheet_watering.html', user=user, start_date=start_date,
                                        end_date=end_date, block=block)

            else:
                block=user.block
                return render_template('blockwise_summary_sheet_watering_blocks.html', user=user, start_date=start_date,
                                       end_date=end_date, block=block)
    else:
        return render_template('login_fail.html', user=user)
@app.route('/Overseer_summary_watering', methods=['POST', 'GET'])
def Overseer_Summary_Watering():
    email = session['email']
    user = User.get_by_email(email)
    if email is not None:
        if request.method == 'GET':
            return render_template('between_dates_watering_overseerwise.html', user=user)
        else:
            start_date = request.form['startdate']
            end_date = request.form['enddate']
            overseer = request.form['overseer']
            return render_template('overseer_summary_sheet_watering.html', user=user, start_date=start_date,
                                   end_date=end_date, overseer=overseer)
    else:
        return render_template('login_fail.html', user=user)
@app.route('/addwatering/<string:plantation_id>', methods=['POST', 'GET'])
def add_watering(plantation_id):
    email = session['email']
    if email is not None:
        if request.method == 'GET':
            user = User.get_by_email(email)
            if user.designation == 'HQ Staff':
                  return render_template('add_watering.html', user=user, plantation_id= plantation_id)
            else:
                  return render_template('add_watering_blocks.html', user=user, plantation_id= plantation_id)
        else:

            user = User.get_by_email(email)
            originalCountOfCrops = request.form['originalCountOfCrops']
            currentCountOfCrops = request.form['currentCountOfCrops']
            asDate = request.form['asDate']
            numberOfManDays = request.form['numberOfManDays']
            numberOfPeople = request.form['numberOfPeople']
            numberOfReplacedCrops = int(originalCountOfCrops) - int(currentCountOfCrops)
            user_id = user._id
            user_name = user.username
            plantation_id = plantation_id
            application = Database.find("plantations", {"plantation_id": plantation_id})
            typeOfCrop = None
            plotNo = None
            totalSanctionedPlants = None
            block = None
            overseer = None
            for result_object in application[0:1]:
                typeOfCrop = result_object['typeOfCrop']
                plotNo = result_object['plotNo']
                totalSanctionedPlants = result_object['totalSanctionedPlants']
                estimateCostOfWatering = 2.45*int(totalSanctionedPlants)
                block = result_object['block']
                overseer = result_object['overseer']
                panchayat = result_object['panchayat']
                costOfCrops = result_object['costOfCrops']
            watering = Watering(originalCountOfCrops=originalCountOfCrops, totalSanctionedPlants=totalSanctionedPlants,
                                costOfCrops=costOfCrops,currentCountOfCrops=currentCountOfCrops,numberOfManDays=numberOfManDays,
                                asDate=asDate, typeOfCrop=typeOfCrop, plotNo=plotNo, panchayat=panchayat, estimateCostOfWatering=estimateCostOfWatering,numberOfPeople=numberOfPeople,
                                user_name=user_name, user_id=user_id, numberOfReplacedCrops=numberOfReplacedCrops, plantation_id=plantation_id, block=block, overseer=overseer)
            watering.save_to_mongo()
            if user.designation == 'HQ Staff':
                return render_template('application_added.html', application=application, user=user)
            else:
                return render_template('application_added_blocks.html', application=application, user=user)
    else:
            return render_template('login_fail.html')

@app.route('/Wateringsbyplantation/<string:plantation_id>')
def waterings_by_plantation(plantation_id):
    watering = []
    watering_dict = Database.find("waterings", {"plantation_id": plantation_id})
    for tran in watering_dict:
        watering.append(tran)
    single_watering = json.dumps(watering, default=json_util.default)
    return single_watering
@app.route('/viewwatering/<string:plantation_id>')
def view_watering(plantation_id):
    email = session['email']
    user = User.get_by_email(email)
    if email is not None:
        if user.designation == 'HQ Staff':
                return render_template('view_watering.html', user=user, plantation_id=plantation_id)
        else:
                return render_template('view_watering_blocks.html', user=user, plantation_id=plantation_id)
    else:
        return render_template('login_fail.html', user=user)
@app.route('/deletewatering/<string:_id>')
def deletewatering(_id):
    email = session['email']
    user = User.get_by_email(email)
    Watering.deletefrom_mongo(_id= _id)
    return render_template('deleted.html', user=user)
@app.route('/raw_watering/<string:_id>')
def raw_watering(_id):
    watering = []
    watering_dict = Database.find("waterings", {"_id": _id})
    for tran in watering_dict:
        watering.append(tran)
    single_watering = json.dumps(watering, default=json_util.default)
    return single_watering
@app.route('/updatewatering/<string:_id>', methods=['POST', 'GET'])
def update_watering(_id):
    email = session['email']
    if email is not None:
        if request.method == 'GET':
            user = User.get_by_email(email)
            if user.designation == 'HQ Staff':
                return render_template('update_watering_form.html', user=user, _id=_id)
            else:
                return render_template('update_watering_form_blocks.html', user=user, _id=_id)
        else:
            user = User.get_by_email(email)
            user_id = user._id
            user_name = user.username
            asDate = request.form['asDate']
            originalCountOfCrops = request.form['originalCountOfCrops']
            currentCountOfCrops = request.form['currentCountOfCrops']
            numberOfManDays = request.form['numberOfManDays']
            numberOfPeople = request.form['numberOfPeople']
            numberOfReplacedCrops = int(originalCountOfCrops) - int(currentCountOfCrops)
            application = Database.find("waterings", {"_id": _id})
            plantation_id = None
            typeOfCrop = None
            plotNo = None
            estimateCostOfWatering = None
            block = None
            overseer = None
            panchayat = None
            totalSanctionedPlants = None
            costOfCrops = None
            for result_object in application[0:1]:
                plantation_id = result_object['plantation_id']
                typeOfCrop = result_object['typeOfCrop']
                plotNo = result_object['plotNo']
                estimateCostOfWatering = result_object['estimateCostOfWatering']
                block = result_object['block']
                overseer = result_object['overseer']
                panchayat = result_object['panchayat']
                totalSanctionedPlants = result_object['totalSanctionedPlants']
                costOfCrops = result_object['costOfCrops']
            Watering.update_watering(_id=_id,asDate=asDate,estimateCostOfWatering=estimateCostOfWatering,block=block,
                                     numberOfPeople=numberOfPeople,numberOfManDays=numberOfManDays, overseer=overseer,
                                     plantation_id=plantation_id,typeOfCrop=typeOfCrop,plotNo=plotNo, panchayat=panchayat,
                                     originalCountOfCrops=originalCountOfCrops,numberOfReplacedCrops=numberOfReplacedCrops,
                                     currentCountOfCrops=currentCountOfCrops, user_id=user_id, user_name=user_name,
                                     totalSanctionedPlants=totalSanctionedPlants, costOfCrops=costOfCrops)
            return render_template('application_added.html', user=user)
    else:
        return render_template('login_fail.html')
@app.route('/panchayats/<string:block>')
def get_panchayat_name(block):
    district_intents_array = []
    district_intents = Database.find("panchayats", {"Block": block})
    for intent in district_intents:
        district_intents_array.append(intent)
    completed_intents = json.dumps(district_intents_array, default=json_util.default)
    return completed_intents
@app.route('/habitations/<string:block>')
def get_habitations_name(block):
    district_intents_array = []
    district_intents = Database.find("habitations", {"Block Name": block})
    for intent in district_intents:
        district_intents_array.append(intent)
    completed_intents = json.dumps(district_intents_array, default=json_util.default)
    return completed_intents
@app.route('/overseers/<string:block>')
def get_overseers_name(block):
    district_intents_array = []
    district_intents = Database.find("oseers", {"block": block})
    for intent in district_intents:
        district_intents_array.append(intent)
    completed_intents = json.dumps(district_intents_array, default=json_util.default)
    return completed_intents
@app.route('/add_overseer/<string:user_id>', methods=['POST', 'GET'])
def overseer_form(user_id):
    email = session['email']
    if email is not None:
        if request.method == 'GET':
            user = User.get_by_id(user_id)
            return render_template('add_overseer.html', user=user)
        else:
            user = User.get_by_id(user_id)
            block = request.form['Blocks']
            overseer = request.form['overseer']
            oseer = Overseer(block=block, overseer=overseer)
            oseer.save_to_mongo()
            if user.designation == 'HQ Staff':
                return render_template('application_added.html', oseer=oseer, user=user)
            else:
                return render_template('application_added_blocks.html', oseer=oseer, user=user)
    else:
            return render_template('login_fail.html')
@app.route('/delete_overseer/<string:_id>')
def delete_overseer(_id):
    email = session['email']
    user = User.get_by_email(email)
    Overseer.delete_from_mongo(_id= _id)
    return render_template('deleted.html', user=user)
@app.route('/raw_overseer/<string:_id>')
def raw_demands_by_overseer_id(_id):
    overseer = []
    overseer_dict = Database.find("oseers", {"_id": _id})
    for tran in overseer_dict:
        overseer.append(tran)
    single_overseer= json.dumps(overseer, default=json_util.default)
    return single_overseer
@app.route('/updateoverseer/<string:_id>', methods=['POST', 'GET'])
def update_overseer(_id):
    email = session['email']
    if email is not None:
        if request.method == 'GET':
            user = User.get_by_email(email)
            return render_template('update_overseer_form.html', user=user, _id=_id)
        else:
            user = User.get_by_email(email)
            block = request.form['Blocks']
            overseer = request.form['overseer']
            Overseer.update_overseer(block= block, overseer=overseer, _id=_id)
            return render_template('application_added.html', user=user)
    else:
        return render_template('login_fail.html')
if __name__ == '__main__':
    app.run(port=4025, debug=True)



