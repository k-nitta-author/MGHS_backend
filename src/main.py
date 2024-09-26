from os import environ

from user import UserResource
from activity import ActivityResource
from task import TaskResource
from team import TeamResource

from tables import app

user_resource = UserResource()
team_resource = TeamResource()
activity_resource = ActivityResource()
task_resource = TaskResource()

if __name__ == '__main__':

    # CREATE A COMMA SEPARATED LIST OF MGHS EMAILS WHICH SHOULD RECIEVE NOTIFICATIONS OF NEW JOB APPLICATIONS
    environ['JOB_APPLICANT_EMAIL_ADDRESS_LIST'] = "k.nitta.it@gmail.com"

    # CREATE A COMMA SEPARATED LIST OF MGHS EMAILS WHICH SHOULD RECIEVE NOTIFICATIONS OF INQUIRIES
    environ['INQUIRY_EMAIL_ADDRESS_LIST'] = "joshuapicato2016@gmail.com"

    # SET UP ENVIRONMENT VARIABLES FOR THE GMAIL ACCOUNT
    environ['OPTIFLOW_ACCOUNTNAME'] = "optiflow.mghs@gmail.com"
    environ['OPTIFLOW_PASSWORD'] = "mhzz opbh fpdf kxgh"

    app.run(debug=True, host='0.0.0.0')