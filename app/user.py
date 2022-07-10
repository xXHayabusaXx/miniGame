
from interactBDD import InteractBDD
from joueur import Joueur
from menu import Menu
from utils import Utils
from flask_login import UserMixin, AnonymousUserMixin

class User(AnonymousUserMixin, UserMixin):

    def __init__(self, username=None):
        self._is_authenticated=False
        self._is_active=True # on y touche pas
        self._is_anonymous=True 
        self._menu= Menu()
        self._username=username
        self._id= None
        self._id= self.get_id()

    @property
    def username(self):
        return self._username


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

    @username.setter
    def username(self, username):
        self._username=username

    #def isinstance(self):
    #    return "User"


    def get_id(self):
        if self._id==None:
            self._id = InteractBDD.getID(self._menu.username)
        return str(self._id)


    def checkPassword(self, username, password):
        if Utils.sanitization([username, password]):
            password=Utils.hashPassword(password)
            if InteractBDD.existInDB(username):
                if not InteractBDD.checkPassword(username, password):
                    return None
                self._menu.joueur = Joueur(username)
            else:
                self._menu.joueur = Joueur(username, password)   
            self._is_authenticated = True 
            self._is_anonymous= False
            return None
    '''
    def checkPassword(self, username, password):
        # user is already authentificated
        self.__class__= Anonymous
        self.checkPassword(username, password) # it recasts back to User (if the given password is correct)
        return None'''



'''
class Anonymous(AnonymousUserMixin):

    def __init__(self):
        self._is_authenticated=False

    @property
    def is_authenticated(self):
        return self._is_authenticated

    def isinstance(self):
        return "Anonymous"
    '''



        
