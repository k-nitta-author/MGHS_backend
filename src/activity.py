from flask import jsonify, request
from tables import db, app, User, Activity as model, ActivitySubscription as subscription, Task
from datetime import datetime

class ActivityResource:

    def __init__(self) -> None:
        self.register_routes()

    def register_routes(self) -> None:
        # Route to get all activities
        @app.route('/activity', methods=['GET'])
        def get_all_activities():
            #TODO: test this query
            # result = model().query.join(Task, model.task_id==Task.id).all()
            activities = model().query.join(Task, model.task_id == Task.id).all()
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
                    #"task_name": activity.task.name,  # Added task name
                    "number_of_subscriptions": 0 # PLACEHOLDER VALUE
                }
                output.append(input)
            return jsonify({"activity": output})

        # Route to get statistics for activities
        @app.route('/activity/stats', methods=['GET'])
        def get_activity_statistics():
            # get the number of rows composing the activities table
            activity_row_count = db.session.query(model).count()

            # get the number of activities with status: Complete
            complete_activities = model.query.filter_by(status="Complete").count()
            
            # get the number of activities with status: Incomplete
            incomplete_activities = model.query.filter_by(status="Incomplete").count()
            
            # get the number of activity subscriptions 
            subscriptions_count = subscription.query.count()
            
            # get the number of complete subscriptions
            complete_subs_count = subscription.query.filter_by(is_complete=True).count()
            
            # get the number of incomplete subscriptions
            incomplete_subs = subscription.query.filter_by(is_complete=False).count()
            
            # most complete activity
            #most_complete_activity = db.session.query(
            #subscription.activity_id, db.func.count().label('count')
            #).filter_by(is_complete=True).group_by(subscription.activity_id).order_by(db.desc('count')).first()
            
            # least complete activity
            #least_complete_activity = db.session.query(
            #subscription.activity_id, db.func.count().label('count')
            #).filter_by(is_complete=True).group_by(subscription.activity_id).order_by('count').first()
            
            # TODO: get the average time to completion for activity subscription
            # avg time to completion for activity subscription
            output = {
            "activity_row_count": activity_row_count,
            "complete_activities": complete_activities,
            "incomplete_activities": incomplete_activities,
            "subscriptions_count": subscriptions_count,
            "complete_subs_count": complete_subs_count,
            "incomplete_subs": incomplete_subs,
            #"most_complete_activity": {"id": most_complete_activity.activity_id, "name": most_complete_activity.name} if most_complete_activity else None,
            #"least_complete_activity": {"id": least_complete_activity.activity_id, "name": least_complete_activity.name} if least_complete_activity else None
            #"avg_time_to_completion": avg_time_to_completion
            }
            return jsonify(output)

        # Route to get a single activity by ID
        @app.route('/activity/<id>', methods=['GET'])
        def get_one_activity(id):
            activity: model = model().query.filter_by(id=id).first()
            if not activity:
                return jsonify({'message': 'No activity found'})
            activity_data = {
                    "activity_id":activity.id,
                    "description":activity.description,
                    "name":activity.name,
                    "status":activity.status,
                    "task_id":activity.task_id,
                    #"task_name": activity.task.name  # Added task name
            }
            return jsonify({'activity': activity_data})

        # Route to create a new activity
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

        # Route to delete an activity by ID
        @app.route('/activity/<id>', methods=['DELETE'])
        def delete_activity(id):
            activity = model().query.join().filter_by(id=id).first()
            if not activity:
                return jsonify({'message': 'No activity found'})
            db.session.delete(activity)
            db.session.commit()
            return jsonify({'message': 'activity has been deleted'})
        
        # Route to update an activity by ID
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

        # Route to set the status of an activity by ID
        @app.route('/activity/<id>/status', methods=['PUT'])
        def set_activity_status(id):
            data = request.get_json()
            activity = model().query.filter_by(id=id).first()
            activity.status=data["status"] # status can go from complete and incomplete
            db.session.add(activity)
            db.session.commit()
            return jsonify({'message': 'new activity created'})

        # Route to get all activity subscriptions
        @app.route('/activity/sub', methods=['GET'])
        def get_all_activity_subscriptions():
            subs = subscription.query.all()
            output = []
            for sub in subs:

                u: User = User().query.filter_by(id=sub.intern_id).first()
                if u == None: return jsonify({'message': 'no intern by that id'})

                input_data = {
                    "activity_id":sub.activity_id,
                    "intern_id":sub.intern_id,
                    "intern_name": u.givenname + " " + u.surname,  # Added intern name
                    "begin_date": sub.begin_date,
                    "end_date": sub.end_date,
                    "is_complete": sub.is_complete,
                    "reflection": sub.reflection
                }
                output.append(input_data)
            return jsonify({'output': output})

        # Route to get subscriptions for a specific activity by ID
        @app.route('/activity/<id>/sub', methods=['GET'])
        def get_activity_subscriptions(id):
            subs = subscription().query.filter_by(activity_id=id).all()


            output = []
            for sub in subs:

                u: User = User().query.filter_by(id=sub.intern_id).first()
                if u == None: return jsonify({'message': 'no intern by that id'})

                input_data = {
                    "activity_id":sub.activity_id,
                    "intern_id":sub.intern_id,
                    "intern_name": u.givenname + " " + u.surname,  # Added intern name
                    "begin_date": sub.begin_date,
                    "end_date": sub.end_date,
                    "is_complete": sub.is_complete,
                    "reflection": sub.reflection
                }
                output.append(input_data)
            return jsonify({'output': output})

        # Route to get a specific activity subscription by activity ID and user ID
        @app.route('/activity/<id>/sub/<u_id>', methods=['GET'])
        def get_one_activity_subscription(id, u_id):
            u: User = User().query.filter_by(public_id=u_id).first()
            if u == None: return jsonify({'message': 'no intern by that id'})
            sub: subscription = subscription().query.filter_by(activity_id=id, intern_id=u.id).first()
            input_data = {
                    "activity_id":sub.activity_id,
                    "intern_id":sub.intern_id,
                    "intern_name": u.givenname + " " + u.surname,  # Added intern name
                    "begin_date": sub.begin_date,
                    "end_date": sub.end_date,
                    "is_complete": sub.is_complete,
                    "reflection": sub.reflection
            } if sub else None
            db.session.commit()
            return jsonify({'message': input_data})

        # Route to subscribe to an activity by ID
        @app.route('/activity/<id>/subscribe', methods=['POST'])
        def subscribe_to_activity(id):
            data = request.get_json()
            activity = model().query.filter_by(id=id).first()
            sub = subscription()
            u = User().query.filter_by(public_id=data["intern_id"]).first()
            if u == None: return jsonify({'message': 'no intern by that id'})
            sub.activity_id = id
            sub.intern_id = u.id
            sub.begin_date = datetime.now()
            sub.end_date = None
            sub.is_complete = False
            sub.reflection = ""
            db.session.add(sub)
            db.session.commit()
            return jsonify({'message': 'subscribed to activity'})
    
        # Route to unsubscribe from an activity by ID
        @app.route('/activity/<id>/unsubscribe', methods=['PUT'])
        def unsubscribe_to_activity(id):
            data = request.get_json()
            activity = model().query.filter_by(id=id).first()
            
            u: User = User().query.filter_by(public_id=data["intern_id"]).first()
            sub = subscription().query.filter_by(activity_id=id, intern_id=u.id).first()

            if u == None: return jsonify({'message': 'no intern by that id'})
            db.session.delete(sub)
            db.session.commit()
            return jsonify({'message': 'subscribed to activity'})
        
        # Route to update the reflection for an activity subscription by activity ID
        @app.route('/activity/<id>/sub/reflection', methods=['PUT'])
        def update_reflection_activity(id):
            data = request.get_json()
            intern_id = data["intern_id"]

            u : User = User().query.filter_by(public_id=intern_id).first()
            if u == None: return jsonify({'message': 'no intern by that id'})

            sub: subscription = subscription().query.filter_by(activity_id=id, intern_id=u.id).first()
            sub.reflection = data["reflection"]
            db.session.commit()
            return jsonify({'message': 'completed activity'})

        # Route to get all activity subscriptions for a user by public ID
        @app.route('/activity/sub/<public_id>', methods=['GET'])
        def get_user_activity_subscription(public_id):
            result = db.session.query(model, subscription, User)\
            .join(subscription, model.id==subscription.activity_id)\
            .join(User, User.id == subscription.intern_id)\
            .filter(User.public_id == public_id)\
            .all()
            if not result:
                return jsonify({'message': 'no matching record found'}), 404
            response = []
            for activities, subs, user in result:
                response.append({
                    "activity_name":  activities.name,
                    "activity_description": activities.description,
                    "activity_status": activities.status,
                    'subscription_begin_date': subs.begin_date,
                    'subscription_end_date': subs.end_date,
                    'subscription_is_complete': subs.is_complete,
                    'subscription_reflection': subs.reflection,
                    'user_givenname': user.givenname,
                    'user_surname': user.surname,
                    "activity_id": activities.id,
                    #"task_name": activities.task.name  # Added task name
                })

            summary = {
                "no_complete_activities": len([x for x in response if x['subscription_is_complete'] == True]),
                "no_of_subscriptions": len(response),
            }


            return jsonify({'message': response, 'summary': summary})
        
        # Route to mark an activity subscription as complete by activity ID
        @app.route('/activity/<id>/complete', methods=['PUT'])
        def complete_activity_subscription(id):
            data = request.get_json()
            intern_id = data["intern_id"]
            u: User = User().query.filter_by(public_id=intern_id).first()
            if u == None: return jsonify({'message': 'no intern by that id'})
            sub = subscription().query.filter_by(activity_id=id, intern_id=u.id).first()
            sub.end_date = datetime.now()
            sub.is_complete = True
            sub.reflection = data["reflection"]
            db.session.commit()
            return jsonify({'message': 'completed activity'})