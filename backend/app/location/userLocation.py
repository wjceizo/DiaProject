from . import MethodView,abort, location
from ..models import Province,County,City,Town
from flask import current_app
from .. import db

@location.route("/provinces")
class ProvinceView(MethodView):
    def get(self):
        provinces = Province.query.all()
        province_list =[province.to_dict() for province in provinces]
        return {'data': province_list}
    
@location.route("/province/<province_id>/cities")
class CityView(MethodView):
    def get(self, province_id):
        cities = City.query.filter_by(province_id=province_id).all()
        city_list =[city.to_dict() for city in cities]
        return {'data': city_list}
    
@location.route("/city/<city_id>/counties")
class CountyView(MethodView):
    def get(self, city_id):
        counties = County.query.filter_by(city_id=city_id).all()
        county_list =[county.to_dict() for county in counties]
        return {'data': county_list}
    
@location.route("/county/<county_id>/towns")
class TownView(MethodView):
    def get(self,county_id):
        towns = Town.query.filter_by(county_id=county_id).all()
        town_list =[town.to_dict() for town in towns]
        return {'data': town_list}