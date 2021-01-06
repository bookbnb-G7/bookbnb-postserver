from app.db import Base
from datetime import datetime
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKTElement
from sqlalchemy import Column, DateTime, Float, Integer, String


def _get_coordinates_from_geom(geom: WKTElement):
    shapely_geom = to_shape(geom)

    coordinates = {
        'lng': float(shapely_geom.x),
        'lat': float(shapely_geom.y)
    }

    return coordinates


class Room(Base):

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, autoincrement=False)
    type = Column(String(60), nullable=False)
    capacity = Column(Integer, nullable=False)
    owner = Column(String(255), nullable=False)
    owner_uuid = Column(Integer, nullable=False)
    price_per_day = Column(Integer, nullable=False)
    location = Column(String(255), nullable=False)
    coordinates = Column(Geometry(geometry_type='POINT', srid=4326))

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, id, type, owner, owner_uuid, price_per_day, latitude, longitude, capacity, location):
        self.id = id
        self.type = type
        self.owner = owner
        self.capacity = capacity
        self.location = location
        self.owner_uuid = owner_uuid
        self.price_per_day = price_per_day
        self.coordinates = WKTElement(f'POINT({longitude} {latitude})', srid=4326)

        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def serialize(self):
        coordinates = _get_coordinates_from_geom(self.coordinates)

        return {
            "id": self.id,
            "type": self.type,
            "owner": self.owner,
            "latitude": coordinates['lat'],
            "longitude": coordinates['lng'],
            "owner_uuid": self.owner_uuid,
            "price_per_day": self.price_per_day,
            "capacity": self.capacity,
            "location": self.location,

            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
