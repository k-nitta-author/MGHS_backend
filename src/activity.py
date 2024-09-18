from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from tables import db, app, Activity as model, ActivitySubscription as subscription
from datetime import datetime

class ActivityResource:

    def __init__(self) -> None:
        
        self.register_routes()

    def register_routes(self) -> None:


        @app.route('/activity', methods=['GET'])
        def get_all_activities():

            activities = model().query.all()
            output=[]

            activity_data = []

            for activity in activities:

                activity : model = activity

                input = {
                    "activity_id":activity.id,
                    "description":activity.description,
                    "name":activity.name,
                    "status":activity.status,
                    "task_id":activity.task_id,
                }

                output.append(input)


            return jsonify({"activity": output})

        @app.route('/activity/<id>', methods=['GET'])
        def get_one_activity(id):

            activity = model().query.filter_by(id=id).first()

            if not activity:
                return jsonify({'message': 'No activity found'})

            activity_data = {
                    "activity_id":activity.id,
                    "description":activity.description,
                    "name":activity.name,
                    "status":activity.status,
                    "task_id":activity.task_id,
            }

            return jsonify({'activity': activity_data})

        @app.route('/activity', methods=['POST'])
        def create_activity():

            data = request.get_json()


            activity = model()

            activity.description = data["description"]
            activity.name= data["name"]
            activity.status=data["status"]
            activity.task_id=data["task_id"]
            
            db.session.add(activity)
            db.session.commit()

            return jsonify({'message': 'new activity created'})

        @app.route('/activity/<id>', methods=['DELETE'])
        def delete_activity(id):

            activity = model().query.filter_by(id=id).first()

            if not activity:
                return jsonify({'message': 'No activity found'})
    

            db.session.delete(activity)
            db.session.commit()

            return jsonify({'message': 'activity has been deleted'})
        
        @app.route('/activity/<id>', methods=['PUT'])
        def update_activity(id):
            data = request.get_json()


            activity = model().query.filter_by(id=id).first()

            activity.description = data["description"]
            activity.name= data["name"]
            activity.status=data["status"]
            activity.task_id=data["task_id"]

            db.session.add(activity)
            db.session.commit()

            return jsonify({'message': 'new activity created'})
        

        @app.route('/activity/<id>/subscriptions', methods=['GET'])
        def get_activity_subscriptions(id):

            subs = subscription().query.filter_by(activity_id=id).all()

            output = []

            for sub in subs:

                input_data = {

                    "activity_id":sub.activity_id,
                    "intern_id":sub.intern_id,
                    "begin_date": sub.begin_date,
                    "end_date": sub.end_date,
                    "is_complete": sub.is_complete,
                    "reflection": sub.reflection

                }

                output.append(input_data)
            
            return jsonify({'output': output})
        
        @app.route('/activity/<id>/subscribe', methods=['POST'])
        def subscribe_to_activity(id):

            data = request.get_json()

            activity = model().query.filter_by(id=id).first()

            sub = subscription()

            sub.activity_id = id
            sub.intern_id = data["intern_id"]
            sub.begin_date = datetime.now()
            sub.end_date = None
            sub.is_complete = False
            sub.reflection = ""

            db.session.add(sub)
            db.session.commit()
            
            return jsonify({'message': 'subscribed to activity'})
        

        @app.route('/activity/<id>/complete', methods=['PUT'])
        def complete_activity(id):

            data = request.get_json()

            intern_id = data["intern_id"]

            sub = subscription().query.filter_by(activity_id=id, intern_id=intern_id).first()

            sub.end_date = datetime.now()
            sub.is_complete = True
            sub.reflection = data["reflection"]
            
            db.session.commit()

            return jsonify({'message': 'completed activity'})