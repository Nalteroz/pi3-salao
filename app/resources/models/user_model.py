from ..data import system_db
from .basic import BaseModel, UserRoleEnum

class UserModel(BaseModel):
    """
        This class summarizes the user, with all its attributes.

        Attributes:
        ------------
        All the attributes are inherited from BaseModel.
        name : str
            The user's name.
        email : str
            The user's email.
        password : str
            The user's password.
        role : int
            The user's role.
    """
    __tablename__ = 'user'
    __table_args__ = {"schema": "security"}

    name = system_db.Column(system_db.String(255), nullable=False)
    role = system_db.Column(system_db.Enum(UserRoleEnum), nullable=False)
    email = system_db.Column(system_db.String(255), nullable=False, unique=True)
    password = system_db.Column(system_db.LargeBinary(), nullable=False)

    def GetColumnsNames():
        return {
            "name": "nome",
            "role": "cargo",
            "email": "e-mail",
            "password": "senha"
        }