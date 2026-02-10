from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorite_table = Table(
    "favorites",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True)
)

location_table = Table(
    "user_location",
    db.Model.metadata,
    Column("user.id", ForeignKey("user.id"), primary_key=True),
    Column("location.id", ForeignKey("location.id"), primary_key=True)
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(120))

    favorites: Mapped[list["Character"]] = relationship(
        "Character",
        secondary=favorite_table,
        # sincroniza ambos modelos, es un vinculo bidireccional.
        back_populates="favorited_by"
    )

    user_location: Mapped[list["Location"]] = relationship(#aqui tenia list["User"] antes...
        "Location", #model db name CLASS
        secondary=location_table,
        back_populates="located_at"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": self.favorites
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    quote: Mapped[str] = mapped_column(String(120), nullable=False)
    image: Mapped[str] = mapped_column(String(120), nullable=True)
    
    favorited_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=favorite_table,
        # sincroniza ambos modelos, es un vinculo bidireccional.
        back_populates="favorites"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "quote": self.quote,
            "image": self.image
        }
    # After creating the new model, go to admin file and add a VIEW


class Location(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    image: Mapped[str] = mapped_column(String(120), nullable=True)
    town: Mapped[str] = mapped_column(String(120), nullable=False)
    use: Mapped[str] = mapped_column(String(120), nullable=False)

    located_at: Mapped[list["User"]] = relationship(
        "User",
        secondary=location_table,
        back_populates="user_location"
    )

    def serialize(self):
       return{
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "town":self.town,
            "use": self.use
       }
