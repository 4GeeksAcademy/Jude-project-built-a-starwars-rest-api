import os
from flask_admin import Admin
from models import db, User, Character, Planet, Vehicle, Starship, CharacterFavorite, PlanetFavorite, VehicleFavorite, StarshipFavorite
from flask_admin.contrib.sqla import ModelView


class UserModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'email', 'password', 'is_active', 'favorites',
                   'favorites_planet', 'favorite_vehicle', 'favorite_starship']


class CharacterModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'name', 'height', 'gender',
                   'eyes_color', 'birth_day', 'mass', 'favorites_by']


class PlanetModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'name', 'climate',
                   'diametre', 'population', 'favorite_by']


class VehicleModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'name', 'model', 'passengers', 'favorite_by']


class StarshipModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'name', 'model',
                   'passengers', 'length', 'favorite_by']


class CharacterFavoriteModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'users', 'character_id', 'character']


class PlanetFavoriteModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'users', 'planet_id', 'planetas']


class VehicleFavoriteModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'users', 'vehicle_id', 'vehiculo']


class StarshipFavoriteModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'users', 'starship_id', 'starship']


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CharacterModelView(Character, db.session))
    admin.add_view(PlanetModelView(Planet, db.session))
    admin.add_view(VehicleModelView(Vehicle, db.session))
    admin.add_view(StarshipModelView(Starship, db.session))
    admin.add_view(CharacterFavoriteModelView(CharacterFavorite, db.session))
    admin.add_view(PlanetFavoriteModelView(PlanetFavorite, db.session))
    admin.add_view(VehicleFavoriteModelView(VehicleFavorite, db.session))
    admin.add_view(StarshipFavoriteModelView(StarshipFavorite, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
