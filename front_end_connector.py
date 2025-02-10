from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

class FrontEndConnector:
        def _init_(self):
            self.app = Flask(_name_)
            CORS(self.app)
            # Add routes
            self.app.add_url_rule('/', 'index', methods=['GET'])

        def index(self):
            return render_template('index.html')

        """def get_runs(self):
            response = jsonify({"runs": self.runs})
            return response

        def setRuns(self, runs):
            print("Runs:", len(runs))

            self.runs = runs"""