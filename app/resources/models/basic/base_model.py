from ...data import system_db

class BaseModel(system_db.Model):
    """
        This class represent the base element on the database, with the base attributes.

        Attributes:
        ------------
        id : int
            The element unique id.
    """
    __abstract__ = True

    id = system_db.Column(system_db.Integer, primary_key=True)
