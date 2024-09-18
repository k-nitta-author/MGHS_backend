from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from tables import db, app, Task as model

class TaskResource:

    def __init__(self) -> None:
        
        self.register_routes()

    def register_routes(self) -> None:


        @app.route('/task', methods=['GET'])
        def get_all_tasks():

            tasks = model().query.all()
            output=[]

            task_data = []

            for task in tasks:

                task : model = task

                input = {

                    "task.id":task.id,
                    "name":task.name,
                    "description":task.description,
                    "team_id":task.team_id

                }


                output.append(input)


            return jsonify({"task": output})

        @app.route('/task/<id>', methods=['GET'])
        def get_one_task(id):

            task = model().query.filter_by(id=id).first()

            if not task:
                return jsonify({'message': 'No task found'})

            task_data = {
                    "task.id":task.id,
                    "name":task.name,
                    "description":task.description,
                    "team_id":task.team_id
            }

            return jsonify({'task': task_data})

        @app.route('/task', methods=['POST'])
        def create_task():

            data = request.get_json()


            task = model()

            task.name= data["name"]
            task.description= data["description"]
            task.team_id= data["team_id"]


            
            db.session.add(task)
            db.session.commit()

            return jsonify({'message': 'new task created'})

        @app.route('/task/<id>', methods=['DELETE'])
        def delete_task(id):

            task = model().query.filter_by(id=id).first()

            if not task:
                return jsonify({'message': 'No task found'})
    

            db.session.delete(task)
            db.session.commit()

            return jsonify({'message': 'task has been deleted'})
        
        @app.route('/task/<id>', methods=['PUT'])
        def update_task(id):
            data = request.get_json()


            task = model().query.filter_by(id=id).first()

            task.name= data["name"]
            task.description= data["description"]
            task.team_id= data["team_id"]

            db.session.add(task)
            db.session.commit()

            return jsonify({'message': 'new task created'})