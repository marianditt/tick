from typing import Tuple, List


class DatabaseError(Exception):
    pass


class DatabaseClient(object):
    def find_one(self, query: str, **kwargs) -> Tuple:
        raise NotImplementedError()

    def find_many(self, query: str, **kwargs) -> List[Tuple]:
        raise NotImplementedError()

    def mutate(self, query: str, **kwargs):
        raise NotImplementedError()
