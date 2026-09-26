

from geoalchemy2 import Geography, WKBElement
from src.models.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column


class Place(Base): 
    __tablename__ = "places"

    name : Mapped[str]
    # Mot diem, bao gom kinh do va vi do 
    location : Mapped[WKBElement] = mapped_column(

        Geography(geometry_type="POINT" , srid = 4326), nullable=False
        #srid: He quy chieu toa do WGS 84 ma google map dien thoai va hau het ban do API su dung, no quy 
        #dinh hai so trong POINT duoc hieu theo chuan nao
    )