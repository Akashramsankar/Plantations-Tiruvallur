import uuid
from src.common.database import Database
class Overseer(object):
    def __init__(self, block, overseer, _id=None):
        self.block = block
        self.overseer = overseer
        self._id = uuid.uuid4().hex if _id is None else _id
    def save_to_mongo(self):
        Database.insert(collection='oseers', data=self.json())
    @classmethod
    def update_overseer(cls, _id, block, overseer):
        Database.update_overseer(collection='oseers', query={'_id': _id}, block=block,
                              overseer=overseer)
    def json(self):
        return {
            'block': self.block,
            'overseer': self.overseer,
            '_id': self._id,
        }
    @classmethod
    def delete_from_mongo(cls, _id):
        Database.delete_from_mongo(collection='oseers', query={'_id': _id})
