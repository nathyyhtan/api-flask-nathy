from flask_restful import Resource
from models.store import StoreModel

NAME_ALREADY_EXISTS = "Uma loja com o nome '{}' já existe!"
ERROR_INSERTING = "Ocorreu um erro ao inserir a loja!"
STORE_NOT_FOUND = "Loja não encontrada!"
STORE_DELETED = "Loja excluída!"


class Store(Resource):
    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {"message": STORE_NOT_FOUND}, 404

    @classmethod
    def post(cls, name: str):
        if StoreModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return store.json(), 201

    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": STORE_DELETED}, 200

        return {"message": STORE_NOT_FOUND}, 404


class StoreList(Resource):
    @classmethod
    def get(cls):
        return {"stores": [store.json() for store in StoreModel.find_all()]}, 200
