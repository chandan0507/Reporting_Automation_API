# This Flask app creates a table in mysql database and updates the test cases result into the created table using CRUD API

<br>

Author : Chandan.D
<br>
Date of release : 09-09-2024

<br>

using flask_sqlalchemy db model table is created for the updation of results

<br>

Make sure python3.* version is installed in the local system
<br>
Install below python libraries using pip

<br>
pip install Flask
<br>
pip install Flask-SQLAlchemy

<br>

There are 2 GET methods used in the code
<br>
1 is we can results of 1 test case in json using /get_test/<case_id>, NOTE <case_id> is replaced with actual value in db for TEST_CASE_ID Column
<br>
1 is we can results of 1 test run(which includes multiple test cases) in json using /get_run/<run_id>, NOTE <run_id> is replaced with actualy value in db for TEST_RUN_ID Column
<br>

Delete /delete_test/<run_id> is used to DELETE the any entry using the test_run_id, which is given in url itself

<br>


Post /post_test is used to create a entry for test_case result with body as below

<br>
{
    "TEST_RUN_ID": 8293,
    "TEST_CASE_NAME": "First_Case_string",
    "PRODUCT": "Some_Product_string",
    "EXECUTION_TIME": "24-08-2024 23:12:00",
    "RESULT": "pass or fail any one"
}
<br>

Important : In Deployment server Don't run as debug=True