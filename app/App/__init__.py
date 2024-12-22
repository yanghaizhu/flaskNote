# init to create flask application.
from  flask import Flask
# import views, also run views.
from .viewsHome import *

#from flask_restful import Resource,Api
#
#dataList = []
#class People(Resource):
#    def get(self):
#        for x in dataList:
#            if x['Name'] == name:
#                return x
#        return {'Name':None}
#        
#    def post(self, name):
#        tmp  = {'Name': name}
#        dataList.append(tmp)
#        return tmp
#        
#    def delete(self,data):
#   
#        for ind, x in enumerate(dataList):
#            if x == data:
#                tmp = dataList.pop(ind)
#            return {'Note': Deleted}

def create_app():
    app = Flask(__name__)
    
#    api = Api(app)
#    api.add_resource(People,'/Name/')


    app.register_blueprint(blueprint=homeBlueprint)
    return app
