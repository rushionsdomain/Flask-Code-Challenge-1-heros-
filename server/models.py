from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Models
class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    # Relationship: Hero has many HeroPowers
    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade="all, delete-orphan")

    # Association proxy to access powers through HeroPower
    powers = association_proxy('hero_powers', 'power')

    # Serialization: Only serialize specific fields
    serialize_rules = ('-hero_powers.hero', '-powers.hero_powers')

    def __repr__(self):
        return f'<Hero {self.name} (Super: {self.super_name})>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    # Relationship: Power has many HeroPowers
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade="all, delete-orphan")

    # Association proxy to access heroes through HeroPower
    heroes = association_proxy('hero_powers', 'hero')

    # Serialization: Only serialize specific fields
    serialize_rules = ('-hero_powers.power', '-heroes.hero_powers')

    # Validation: Description should be meaningful
    @validates('description')
    def validate_description(self, key, value):
        if len(value) < 10:
            raise ValueError("Power description must be at least 10 characters long")
        return value

    def __repr__(self):
        return f'<Power {self.name}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    # Relationships
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    # Serialization: Avoid recursive serialization of relationships
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    # Validation: Ensure strength is valid
    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Average', 'Weak']:
            raise ValueError("Strength must be 'Strong', 'Average', or 'Weak'")
        return value

    def __repr__(self):
        return f'<HeroPower {self.hero.name} -> {self.power.name} (Strength: {self.strength})>'