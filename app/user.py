
try:
    from joueur import Joueur
    from menu import Menu
    from interactBDD import InteractBDD
except:
    pass
from flask_login import UserMixin, AnonymousUserMixin

class User(UserMixin):

    def __init__(self, username):
        self._is_authenticated=True
        self._is_active=True # on y touche pas
        self._is_anonymous=False 
        self._menu= Menu()
        self._username=username

        joueur = Joueur(username)
        self._menu.joueur = joueur
        self._id= None

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


  
    def get_id(self):
        if self._id==None:
            self._id = InteractBDD.getID(self._username)
        return str(self._id)








class Anonymous(AnonymousUserMixin):

    def __init__(self):
        self._is_authenticated=False
        self._is_active=True # on y touche pas
        self._is_anonymous=True

    @property
    def is_authenticated(self):
        return self._is_authenticated

