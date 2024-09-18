from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from tables import db, app, Team as model

class TeamResource:

    def __init__(self) -> None:
        
        self.register_routes()

    def create_public_id() -> str:

        return ""

    def register_routes(self) -> None:


        @app.route('/team', methods=['GET'])
        def get_all_teams():

            teams = model().query.all()
            output=[]

            team_data = []

            for team in teams:

                team : model = team

                input = {
                    "name": team.name,
                    "description":team.description,
                    "team_id":team.id,                    

                }


                output.append(input)


            return jsonify({"team": output})

        @app.route('/team/<id>', methods=['GET'])
        def get_one_team(id):

            team = model().query.filter_by(id=id).first()

            if not team:
                return jsonify({'message': 'No team found'})

            team_data = {
                    "name": team.name,
                    "description":team.description,
                    "team_id":team.id,   
            }

            return jsonify({'team': team_data})

        @app.route('/team', methods=['POST'])
        def create_team():

            data = request.get_json()


            team = model()

            team.description = data["description"]
            team.name = data["name"]
            
            db.session.add(team)
            db.session.commit()

            return jsonify({'message': 'new team created'})

        @app.route('/team/<id>', methods=['DELETE'])
        def delete_team(id):

            team = model().query.filter_by(id=id).first()

            if not team:
                return jsonify({'message': 'No team found'})
    

            db.session.delete(team)
            db.session.commit()

            return jsonify({'message': 'team has been deleted'})
        
        @app.route('/team/<id>', methods=['PUT'])
        def update_team(id):
            data = request.get_json()


            team = model().query.filter_by(id=id).first()

            team.description = data["description"]
            team.name = data["name"]
            
            db.session.add(team)
            db.session.commit()

            return jsonify({'message': 'new team created'})