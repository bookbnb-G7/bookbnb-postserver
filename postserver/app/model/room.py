from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape

from app.db import Base


def get_coordinates_from_geom(geom: WKTElement):
    shply_geom = to_shape(geom)
    coordinates = {'lng': shply_geom.x, 'lat': shply_geom.y}
    return coordinates


class Room(Base):

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    type = Column(String(60), nullable=False)
    owner = Column(String(255), nullable=False)
    owner_id = Column(Integer, nullable=False)
    price_per_day = Column(Float, nullable=False)
    location = Column(Geometry(geometry_type='POINT', srid=4326))

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, type, owner, owner_id, price_per_day, lng, lat):
        self.type = type
        self.owner = owner
        self.owner_id = owner_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.price_per_day = price_per_day
        self.location = WKTElement(f'POINT({lng} {lat})', srid=4326)

    def serialize(self):
        coords = get_coordinates_from_geom(self.location)
        return {
            "id": self.id,
            "type": self.type,
            "owner": self.owner,
            "owner_id": self.owner_id,
            "price_per_day": self.price_per_day,
            "lng": float(coords['lng']),
            "lat": float(coords['lat']),
            "location": self.location,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
