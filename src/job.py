from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

class JobResource:

    def __init__(self, app: Flask, db: SQLAlchemy, model: object) -> None:
        
        self.register_routes(app, db)
        self.model = model
        self.db = db

    def register_routes(self, app: Flask, db: SQLAlchemy) -> None:


        @app.route('/job', methods=['GET'])
        def get_all_jobs():

            jobs = self.model().query.all()
            output=[]



            job_data = []

            for job in jobs:
                service_data = {
                "id": job.id,
                "jobTitle": job.jobTitle,
                "jobRequest": job.jobRequest,
                "jobRequirements": job.jobRequirements
                }


                output.append(service_data)


            return jsonify({"jobs": output})

        @app.route('/job/<id>', methods=['GET'])
        def get_one_job(id):

            job = self.model().query.filter_by(id=id).first()

            if not job:
                return jsonify({'message': 'No job found'})



            job_data = {
                "id": job.id,
                "jobTitle": job.jobTitle,
                "jobRequest": job.jobRequest,
                "jobRequirements": job.jobRequirements
            }

            return jsonify({'job': job_data})

        @app.route('/job', methods=['POST'])
        def create_job():

            data = request.get_json()


            job = self.model(

                    jobTitle=data['jobTitle'],
                    jobRequest=data['jobRequest'],
                    jobRequirements=data['jobRequirements']

                    )
            
            self.db.session.add(job)
            self.db.session.commit()

            return jsonify({'message': 'new job created'})

        @app.route('/job/<id>', methods=['DELETE'])
        def delete_job(id):

            job = self.model().query.filter_by(id=id).first()

            if not job:
                return jsonify({'message': 'No job found'})
    

            self.db.session.delete(job)
            self.db.session.commit()

            return jsonify({'message': 'job has been deleted'})