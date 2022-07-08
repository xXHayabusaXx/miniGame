
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

        id=InteractBDD.getID(username)
        if id==None:
            InteractBDD.createUser(username)
            id=InteractBDD.getID(username)
        self._id= User.id




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
        return str(self._id)


    def checkPassword(self, username, password):
        if Utils.sanitization([username, password]):
            password=Utils.hashPassword(password)
            if InteractBDD.existInDB(username):
                if InteractBDD.checkPassword(username, password):
                    self._is_authenticated = True # known user with good password
                    self._joueur = Joueur(username)
                    self._menu = Menu()
            # new user 
            self._is_authenticated = True
            self._is_anonymous=False
            joueur = Joueur(username, password)
            self._menu = Menu()
            self._menu.joueur = joueur



class Anonymous(AnonymousUserMixin):

    def __init__(self):
        self._is_authenticated=False
        self._is_active=True # on y touche pas
        self._is_anonymous=True 
        self._menu= None
        self._id= None

    def checkPassword(self, username, password):
        if Utils.sanitization([username, password]):
            password=Utils.hashPassword(password)
            if InteractBDD.existInDB(username):
                if InteractBDD.checkPassword(username, password):
                    self._is_authenticated = True # known user with good password
                    self._joueur = Joueur(username)
                    self._menu = Menu()
            # new user 
            self._is_authenticated = True
            self._is_anonymous=False
            joueur = Joueur(username, password)
            self._menu = Menu()
            self._menu.joueur = joueur

