from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from collections import OrderedDict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:passwd@db_host_ip:db_port/schema'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Below is a db model for AUTOMATION_TEST_CASE table
class AUTOMATION_TEST_CASE(db.Model):
    __tablename__ = 'AUTOMATION_TEST_CASE'
    TEST_CASE_ID  = db.Column(db.Integer, primary_key=True)
    TEST_RUN_ID = db.Column(db.Integer, nullable=False)
    TEST_CASE_NAME = db.Column(db.String(50), nullable=False)
    PRODUCT = db.Column(db.String(30), nullable=False)
    EXECUTION_TIME = db.Column(db.DateTime, nullable=False)
    RESULT = db.Column(db.String(10), nullable=False)
    
# Create the database and tables
with app.app_context():
    db.create_all()
  
@app.route('/get_test/<case_id>', methods=['GET'])
def get_test(run_id):
    if request.method == 'GET':
        # The details of filtered run_id row is stored into a variable
        get_test_case_details = AUTOMATION_TEST_CASE.query.filter_by(TEST_CASE_ID=run_id).first()
        # If there is no rows for the selected get_test_case_details
        if get_test_case_details is None:
            # Return a 404 error if no test case is found with the given run_id
            return jsonify({'TEST_CASE_ID': f'{run_id} Not Found'}), 404
        get_test_case_id = OrderedDict({
            'TEST_CASE_ID': get_test_case_details.TEST_CASE_ID,
            'TEST_RUN_ID': get_test_case_details.TEST_RUN_ID,
            'PRODUCT': get_test_case_details.PRODUCT,
            'EXECUTION_TIME': get_test_case_details.EXECUTION_TIME,
            'RESULT': get_test_case_details.RESULT
        })
        
        # Return the response as JSON
        return jsonify(get_test_case_id)
    
@app.route('/get_run/<run_id>', methods=['GET'])
def get_run(run_id):
    if request.method == 'GET':
        # select all the testc cases rows with the given run_id and store it into get_test_case_details variable
        get_test_case_details = AUTOMATION_TEST_CASE.query.filter_by(TEST_RUN_ID=run_id).all()
        # print(get_test_case_details)
        if get_test_case_details == []:
            # Return a 404 error if no test case is found with the given run_id
            return jsonify({'TEST_RUN_ID': f'{run_id} Not Found'}), 404
        
        get_test_case_list = []
        for case in get_test_case_details:
            get_test_case_list.append({
                'TEST_CASE_ID': case.TEST_CASE_ID,
                'TEST_CASE_NAME': case.TEST_CASE_NAME,
                'PRODUCT': case.PRODUCT,
                'EXECUTION_TIME': case.EXECUTION_TIME,
                'RESULT': case.RESULT
            })
        get_test_case_list_response = OrderedDict({
            'TEST_RUN_ID': run_id,
            'TEST_CASE_DETAILS': get_test_case_list
        })
            
        return jsonify(get_test_case_list_response)
    
@app.route('/delete_test/<run_id>', methods=['DELETE'])
def delete_test(run_id):
    if request.method == 'DELETE':
        # Delete the row by filtering for the run_id of first selected row
        delete_test_case_details = AUTOMATION_TEST_CASE.query.filter_by(TEST_CASE_ID=run_id).first()
        # Validating if delete is null or non null, if non null delete the selected first row
        if delete_test_case_details is not None:
            db.session.delete(delete_test_case_details)
            db.session.commit()
            return jsonify({"message": "Test case Details deleted successfully."}), 200
        else:
            return jsonify({"message": "Test case not found."}), 404

@app.route('/post_test', methods=['POST'])
def post_test():
    if request.method == 'POST':
        json_data = request.get_json()

        if not(3<= len(str(json_data['TEST_RUN_ID'])) <=10):
            return jsonify({'TEST_RUN_ID' : 'Length should be between 3 to 10'}), 400
        if not(5<= len(json_data['TEST_CASE_NAME']) <=30):
            return jsonify({'TEST_CASE_NAME' : 'Length should be between 5 to 30'}), 400
        if not(4<= len(json_data['PRODUCT']) <=15):
            return jsonify({'PRODUCT' : 'Length should be between 4 to 15'}), 400
        if (json_data['RESULT'].upper() not in ['PASS', 'FAIL']):
            return jsonify({'RESULT' : 'Should be either pass or fail'}), 400
        post_test_case_details = AUTOMATION_TEST_CASE(
            TEST_RUN_ID=int(json_data['TEST_RUN_ID']),
            TEST_CASE_NAME=json_data['TEST_CASE_NAME'],
            PRODUCT=json_data['PRODUCT'],
            EXECUTION_TIME=datetime.strptime(json_data['EXECUTION_TIME'], "%d-%m-%Y %H:%M:%S"),
            RESULT=json_data['RESULT']
        )

        db.session.add(post_test_case_details)
        db.session.commit()

        return jsonify({'Message': 'The Test Details were added Successfully'}), 201
    
if __name__ == '__main__':
    app.run(debug=True, host='<host_ip_on_which_api_is_deployed>', port=8080)
    