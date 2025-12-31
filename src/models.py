from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'usuario'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites: Mapped[list['CharacterFavorite']
                      ] = relationship(back_populates='users')
    favorites_planet: Mapped[list['PlanetFavorite']
                             ] = relationship(back_populates='users')
    favorite_vehicle: Mapped[list['VehicleFavorite']
                             ] = relationship(back_populates='users')
    favorite_starship: Mapped[list['StarshipFavorite']
                              ] = relationship(back_populates='users')

    def __repr__(self):
        return f'Usuario {self.email}'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    __tablename__ = 'people'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    height: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String, nullable=False)
    eyes_color: Mapped[str] = mapped_column(String(50))
    birth_day: Mapped[str] = mapped_column(String(20))
    mass: Mapped[int] = mapped_column(nullable=True)
    favorites_by: Mapped[list['CharacterFavorite']
                         ] = relationship(back_populates='character', cascade ='all, delete-orphan')
    
    def __repr__(self):
        return f'Personaje {self.name}'
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height,
            'gender': self.eyes_color,
            'eyes_color': self.eyes_color,
            'birth_day': self.birth_day,
            'mass': self.mass
        }

class Planet(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=True)
    diametre: Mapped[int] = mapped_column(nullable=True)
    population: Mapped[int] = mapped_column(nullable=True)
    favorite_by: Mapped[list['PlanetFavorite']
                        ] = relationship(back_populates='planetas', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'Planet {self.name}'
    
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'climate': self.climate,
            'diametre': self.diametre,
            'population': self.population
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    model: Mapped[str] = mapped_column(String(120))
    passengers: Mapped[int] = mapped_column(nullable=False)
    favorite_by: Mapped[list['VehicleFavorite']
                        ] = relationship(back_populates='vehiculo', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'{self.name}'
    
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'passengers': self.passengers
        }

class Starship(db.Model):
    __tablename__ = 'starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    model: Mapped[str] = mapped_column(String(120))
    passengers: Mapped[int] = mapped_column(nullable=False)
    length: Mapped[int] = mapped_column(nullable=False)
    favorite_by: Mapped[list['StarshipFavorite']
                        ] = relationship(back_populates='starship', cascade = 'all, delete-orphan')

    def __repr__(self):
        return f'{self.name}'
    
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'passengers': self.passengers,
            'length': self.length
        }

class CharacterFavorite(db.Model):
    __tablename__ = 'character_favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('usuario.id'))
    users: Mapped['User'] = relationship(back_populates='favorites')

    character_id: Mapped[int] = mapped_column(ForeignKey('people.id', ondelete='CASCADE'), nullable = False)
    character: Mapped['Character'] = relationship(
        back_populates='favorites_by')

    def __repr__(self):
        return f'le gusta el id # {self.id}'
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'character_id': self.character_id
        }

class PlanetFavorite(db.Model):
    __tablename__ = 'planet_favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('usuario.id'))
    users: Mapped['User'] = relationship(back_populates='favorites_planet')

    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id', ondelete = 'CASCADE'), nullable = False)
    planetas: Mapped['Planet'] = relationship(back_populates='favorite_by')

    def __repr__(self):
        return f'le gusta {self.users}'
    
    def serialize(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'planetas': self.planetas
        }

class VehicleFavorite(db.Model):
    __tablename__ = 'vehicle_favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('usuario.id'))
    users: Mapped['User'] = relationship(back_populates='favorite_vehicle')

    vehicle_id: Mapped[int] = mapped_column(ForeignKey('vehicles.id', ondelete = 'CASCADE'))
    vehiculo: Mapped['Vehicle'] = relationship(back_populates='favorite_by')
    
    def __repr__(self):
        return f'le gusta {self.users}'
    
    def serialize(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'vehicle_id': self.vehicle_id
        }

class StarshipFavorite(db.Model):
    __tablename__ = 'starship_favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('usuario.id'))
    users: Mapped['User'] = relationship(back_populates='favorite_starship')

    starship_id: Mapped[int] = mapped_column(ForeignKey('starships.id', ondelete = 'CASCADE'))
    starship: Mapped['Starship'] = relationship(back_populates='favorite_by')

    def __repr__(self):
        return f'le gusta el usuario con el id # {self.user_id}'
    
    def serialize(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'starship_id': self.starship_id
        }