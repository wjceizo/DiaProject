from . import auth_api, Resource
from ..models import User
from flask_restful import reqparse
from flask import current_app
import json

parser = reqparse.RequestParser()
parser.add_argument('page', type=int, required=True, location='json', help='第几页不能为空')
parser.add_argument('per_page', required=True, type=int, location='json', help='每页数量不能为空')
parser.add_argument('order', type=str, location='json', default='id', required=False)
parser.add_argument('order_by', type=str, location='json', default='ASC', required=False)


class UserView(Resource):

    def get(self):
        args = parser.parse_args()
        get_item = {}
        user_item = []
        current_app.logger.info(args['order'])
        current_app.logger.info(args['order_by'])
        if args['order'] == 'id' and args['order_by'] == 'ASC':
            pagination = User.query.order_by(User.id).paginate(page=args['page'],
                                                               per_page=args['per_page'],
                                                               error_out=False)

        elif args['order'] == 'username' and args['order_by'] == 'DESC':
            pagination = User.query.order_by(User.username.desc()).paginate(page=args['page'],
                                                                            per_page=args['per_page'],
                                                                            error_out=False)

        elif args['order'] == 'username' and args['order_by'] == 'ASC':
            pagination = User.query.order_by(User.username).paginate(page=args['page'],
                                                                     per_page=args['per_page'],
                                                                     error_out=False)

        elif args['order'] == 'id' and args['order_by'] == 'DESC':
            pagination = User.query.order_by(User.id.desc()).paginate(page=args['page'],
                                                                      per_page=args['per_page'],
                                                                      error_out=False)

        else:
            return {'status': 403, 'message': 'order or order_by wrong'}, 403

        count = User.query.count()
        order = args['order']
        order_by = args['order_by']
        users = pagination.items
        has_next = pagination.has_next
        has_prev = pagination.has_prev
        page = pagination.page
        pages = pagination.pages
        per_page = pagination.per_page
        current_page = len(users)
        current_app.logger.info(has_next)
        get_item.update({'total': count,
                         'page': page,
                         'perPage': per_page,
                         'currentPage': current_page,
                         'totalPages': pages,
                         'order': order,
                         'orderBy': order_by,
                         'hasNext': has_next,
                         'hasPrev': has_prev,
                         })
        for user in users:
            user_dict = {}
            user_dict.update({'user_id': user.id,
                              'username': user.username,
                              'email': user.email,
                              'role': 'User' if user.id == 2 else 'Admin',
                              'name': user.name,
                              'location': user.location,
                              'lang': user.lang})
            user_item.append(user_dict)
        get_item.update({'users': user_item})
        json_item = json.dumps(get_item)
        return get_item, 200


auth_api.add_resource(UserView, '/users')
