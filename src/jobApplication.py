from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

class JobApplicationResource:

    def __init__(self, app: Flask, db: SQLAlchemy, model: object) -> None:
        
        self.register_routes(app, db)
        self.model = model
        self.db = db

    def register_routes(self, app: Flask, db: SQLAlchemy) -> None:


        @app.route('/job_application', methods=['GET'])
        def get_all_job_application():

            job_applications = self.model().query.all()
            output=[]

            application_data = []

            for job_application in job_applications:
                job_application_data = {

                "user_id":job_application.user_id,
                "job_id":job_application.job_id,
                "interview_date":job_application.interview_date,
                "application_date":job_application.application_date,
                "application_source":job_application.application_source

                }


                output.append(job_application_data)


            return jsonify({"job_applications": output})
        

        @app.route('/job_application/<user_id>', methods=['GET'])
        def get_by_user_job_application(user_id):

            job_applications = self.model().query.filter_by(user_id=user_id).all()

            if not job_applications:
                return jsonify({'message': 'No job_application found'})
            
            output=[]
            
            for job_application in job_applications: 

                job_application_data = {
                    "user_id":job_application.user_id,
                    "job_id":job_application.job_id,
                    "interview_date":job_application.interview_date,
                    "application_date":job_application.application_date,
                    "application_source":job_application.application_source

                }

                output.append(job_application_data)

            return jsonify({'job applications': output})
        
        @app.route('/job_application/job/<job_id>', methods=['GET'])
        def get_by_job_job_application(job_id):

            job_applications = self.model().query.filter_by(job_id=job_id).all()

            if not job_applications:
                return jsonify({'message': 'No job_application found'})
            
            output=[]
            
            for job_application in job_applications: 

                job_application_data = {
                    "user_id":job_application.user_id,
                    "job_id":job_application.job_id,
                    "interview_date":job_application.interview_date,
                    "application_date":job_application.application_date,
                    "application_source":job_application.application_source

                }

                output.append(job_application_data)

            return jsonify({'job applications': output})

        @app.route('/job_application/<user_id>/<job_id>', methods=['GET'])
        def get_one_job_application(user_id, job_id):

            job_application = self.model().query.get((user_id,job_id))

            if not job_application:
                return jsonify({'message': 'No job_application found'})

            job_application_data = {
                "user_id":job_application.user_id,
                "job_id":job_application.job_id,
                "interview_date":job_application.interview_date,
                "application_date":job_application.application_date,
                "application_source":job_application.application_source

            }

            return jsonify({'job': job_application_data})

        @app.route('/job_application', methods=['POST'])
        def create_job_application():

            data = request.get_json()


            job_application = self.model(

                    user_id =data['user_id'],
                    job_id =data['job_id'],
                    interview_date = data['interview_date'],
                    application_date=data['application_date'],
                    application_source=data['application_source']

                    )
            
            self.db.session.add(job_application)
            self.db.session.commit()

            return jsonify({'message': 'new job_application created'})
        

        # TODO: COMPLETE THIS FUNCTION
        @app.route('/job_application/<user_id>/<job_id>', methods=['PUT'])
        def update_job_application(user_id, job_id):


            data: dict = request.get_json()


            job_application = self.model(

                    user_id =data['user_id'],
                    job_id =data['job_id'],
                    interview_date = data['interview_date'],
                    application_date=data['application_date'],
                    application_source=data['application_source']

                    )
            
            self.db.session.add(job_application)
            self.db.session.commit()

            return jsonify({'message': 'new job_application created'})

        @app.route('/job_application/<user_id>/<job_id>', methods=['DELETE'])
        def delete_job_application(user_id, job_id):

            job_application = self.model().query.get((user_id, job_id))

            if not job_application:
                return jsonify({'message': 'No user found'})
    

            self.db.session.delete(job_application)
            self.db.session.commit()

            return jsonify({'message': 'job has been deleted'})