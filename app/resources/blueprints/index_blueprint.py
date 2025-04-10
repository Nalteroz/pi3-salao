from flask import render_template, redirect
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from ..models import UserModel #, TruckModel, StorageHistoryModel, ClientModel, CollaboratorModel, MaterialModel, MaterialCollectSiteModel, MaterialCollectionModel, MaterialTriageModel, TransactionModel

IndexBlueprint = Blueprint('index', 'index', url_prefix='/', template_folder='app/resources/templates')

class Utils:
    def GetElementName(element_name):
        name_dict = {
            'user': 'usuário',
        }

        return name_dict.get(element_name, None)
    
    def GetColumnNames(element_name):
        if element_name == 'user':
            return UserModel.GetColumnsNames()
        else:
            return None

@IndexBlueprint.route('/')
class Index(MethodView):
    @jwt_required()
    def get(self):
       return ElementView.get(self, 'user')

@IndexBlueprint.route('/element/<string:element>')
class ElementView(MethodView):
    @jwt_required()
    def get(self, element):
        element_name = Utils.GetElementName(element)
        if not element_name:
            abort(404, message='Element not found.')
        columns = Utils.GetColumnNames(element)
        if not columns:
            abort(404, message='Element columns not found.')
        context = {
            'element': element,
            'element_name': element_name,
            'data_path': '/api/' + element,
            'columns_names': columns
        }
        return render_template('element_content.html', **context)
    
@IndexBlueprint.route('/element/create/<string:element>')
class CreateElementView(MethodView):
    @jwt_required()
    def get(self, element):
        element_name = Utils.GetElementName(element)
        if not element_name:
            abort(404, message='Element not found.')
        columns = Utils.GetColumnNames(element)
        if not columns:
            abort(404, message='Element columns not found.')
        context = {
            'element': element,
            'element_name': element_name,
            'data_path': '/api/' + element,
            'columns_names': columns
        }
        return render_template('add_element.html', **context)
    
@IndexBlueprint.route('/element/update/<string:element>')
class UpdateElementView(MethodView):
    @jwt_required()
    def get(self, element):
        element_name = Utils.GetElementName(element)
        if not element_name:
            abort(404, message='Element not found.')
        columns = Utils.GetColumnNames(element)
        if not columns:
            abort(404, message='Element columns not found.')
        context = {
            'element': element,
            'element_name': element_name,
            'data_path': '/api/' + element,
            'columns_names': columns
        }
        return render_template('update_element.html', **context)
    
@IndexBlueprint.route('/element/delete/<string:element>')
class DeleteElementView(MethodView):
    @jwt_required()
    def get(self, element):
        element_name = Utils.GetElementName(element)
        if not element_name:
            abort(404, message='Element not found.')
        columns = Utils.GetColumnNames(element)
        if not columns:
            abort(404, message='Element columns not found.')
        context = {
            'element': element,
            'element_name': element_name,
            'data_path': '/api/' + element,
            'columns_names': columns
        }
        return render_template('delete_element.html', **context)

@IndexBlueprint.route('/login')
class Login(MethodView):
    def get(self):
        return render_template('login.html')
