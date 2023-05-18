from . import auth, MethodView, abort
from ..models import User
from ..schemas import AuthSchema
from flask import current_app
from flask_jwt_extended import jwt_required
import json


@auth.route("/userinfo")
class UserView(MethodView):

    @jwt_required()
    @auth.arguments(AuthSchema)
    def get(self, page_data):
        get_item = {}
        user_item = []
        current_app.logger.info(page_data['order'])
        current_app.logger.info(page_data['order_by'])
        if page_data['order'] == 'id' and page_data['order_by'] == 'ASC':
            pagination = User.query.order_by(User.id).paginate(page=page_data['page'],
                                                               per_page=page_data['per_page'],
                                                               error_out=False)

        elif page_data['order'] == 'username' and page_data['order_by'] == 'DESC':
            pagination = User.query.order_by(User.username.desc()).paginate(page=page_data['page'],
                                                                            per_page=page_data['per_page'],
                                                                            error_out=False)

        elif page_data['order'] == 'username' and page_data['order_by'] == 'ASC':
            pagination = User.query.order_by(User.username).paginate(page=page_data['page'],
                                                                     per_page=page_data['per_page'],
                                                                     error_out=False)

        elif page_data['order'] == 'id' and page_data['order_by'] == 'DESC':
            pagination = User.query.order_by(User.id.desc()).paginate(page=page_data['page'],
                                                                      per_page=page_data['per_page'],
                                                                      error_out=False)

        else:
            abort(403, message='order or order_by wrong')

        count = User.query.count()
        order = page_data['order']
        order_by = page_data['order_by']
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
                              'role': 'Admin' if user.role_id == 1 else 'Member' if user.role_id == 2 else 'User' if user.role_id == 3 else None,
                              'name': user.name,
                              'location': user.location,
                              'lang': user.lang})
            user_item.append(user_dict)
        get_item.update({'users': user_item})
        return get_item, 200
