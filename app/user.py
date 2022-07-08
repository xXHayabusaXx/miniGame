
from interactBDD import InteractBDD
from joueur import Joueur
from menu import Menu
from utils import Utils
from flask_login import UserMixin, AnonymousUserMixin

class User(UserMixin):

    def __init__(self, username):
        self._is_authenticated=False
        self._is_active=True # on y touche pas
        self._is_anonymous=True 
        self._menu= None
        self._id= None




    @property
    def is_authenticated(self):
        return self._is_authenticated

    @property
    def is_active(self):
        return self._is_active

    @property
    def is_anonymous(self):
        return self._is_anonymous

    @property
    def menu(self):
        return self._menu


    @is_authenticated.setter
    def is_authenticated(self, bool):
        self._is_authenticated=bool

    @is_active.setter
    def is_active(self, bool):
        self._is_active=bool

    @is_anonymous.setter
    def is_anonymous(self, bool):
        self._is_anonymous=bool

    @menu.setter
    def menu(self, menu):
        self._menu=menu




    def get_id(self):
        if self._id==None:
            self._id = InteractBDD.getID(self._menu.username)
        return str(self._id)





class Anonymous(AnonymousUserMixin):

    def __init__(self):
        self._is_authenticated=False

    @property
    def is_authenticated(self):
        return self._is_authenticated

    def checkPassword(self, username, password):
        if Utils.sanitization([username, password]):
            password=Utils.hashPassword(password)
            if InteractBDD.existInDB(username):
                if InteractBDD.checkPassword(username, password):
                    self.__class__ = User
                    self._menu= Menu()
                    self._menu.joueur = Joueur(username)
                    self._is_authenticated = True # known user with good password
                    self._is_anonymous= False
                    return None
                return None
                    
            # new user 
            self.__class__ = User
            self._menu= Menu()
            self._menu.joueur = Joueur(username, password)
            self._is_authenticated = True # known user with good password
            self._is_anonymous= False
            return None
        
