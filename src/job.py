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
                "jobRequirements": job.jobRequirements,
                "available": job.available,
                "max_salary": job.max_salary,
                "min_salary": job.min_salary
                }




                output.append(service_data)


            return jsonify({"jobs": output})
        

        @app.route('/job/open', methods=['GET'])
        def get_open_jobs():
            
            available_jobs = self.model().query.filter_by(available=True)

            job_data = []

            for job in available_jobs:
                service_data = {
                "id": job.id,
                "jobTitle": job.jobTitle,
                "jobRequirements": job.jobRequirements,
                "available": job.available,
                "max_salary": job.max_salary,
                "min_salary": job.min_salary
                }


                job_data.append(service_data)


            return jsonify({"jobs": job_data})
        
        @app.route('/job/closed', methods=['GET'])
        def get_closed_jobs():
            
            available_jobs = self.model().query.filter_by(available=False)

            job_data = []

            for job in available_jobs:
                service_data = {
                "id": job.id,
                "jobTitle": job.jobTitle,
                "jobRequirements": job.jobRequirements,
                "available": job.available,
                "max_salary": job.max_salary,
                "min_salary": job.min_salary
                }


                job_data.append(service_data)


            return jsonify({"jobs": job_data})


        @app.route('/job/<id>', methods=['GET'])
        def get_one_job(id):

            job = self.model().query.filter_by(id=id).first()

            if not job:
                return jsonify({'message': 'No job found'})



            job_data = {
                "id": job.id,
                "jobTitle": job.jobTitle,
                "jobRequirements": job.jobRequirements,
                "available": job.available,
                "max_salary": job.max_salary,
                "min_salary": job.min_salary
            }

            return jsonify({'job': job_data})

        @app.route('/job', methods=['POST'])
        def create_job():

            data = request.get_json()


            job = self.model(

                    jobTitle=data['jobTitle'],
                    jobRequirements=data['jobRequirements'],
                    available=data['available'],
                    description=data['description'],
                    max_salary=data['max_salary'],
                    min_salary=data['min_salary']

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
        

        @app.route('/job/<id>/close', methods=['PUT'])
        def close_job(id):

            job = self.model().query.filter_by(id=id).first()

            if not job:
                return jsonify({'message': 'No job found'})
            
            job.available=False


            self.db.session.commit()

            return jsonify({'message': 'job has been closed out'})
        
        @app.route('/job/<id>/open', methods=['PUT'])
        def open_job(id):

            job = self.model().query.filter_by(id=id).first()

            if not job:
                return jsonify({'message': 'No job found'})
            
            job.available=True


            self.db.session.commit()

            return jsonify({'message': 'job is now open'})