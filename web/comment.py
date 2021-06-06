# -*- coding: utf-8 -*-
#    Copyright (C) 2021  The Project TONA Authors
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
from flask import Blueprint, render_template, request, jsonify
from tona.utils import HTTPException, HTTPResponse
from tona.models.comment import Comment

comment_api_bp = Blueprint('comment_api_bp', __name__, url_prefix='/api/comment')

@comment_api_bp.route("", methods=['POST', 'GET'])
@comment_api_bp.route("/<int:id>", methods=['PUT', 'DELETE'])
def comment(id=0):
    res = HTTPResponse()
    try:
        if request.method == 'POST':
            data = request.json
            res.payload = Comment.add(**data).to_dict()
        elif request.method == 'PUT':
            data = request.json
            res.payload = Comment.edit(id, **data).to_dict()
        elif request.method == 'DELETE':
            Comment.remove(id)
        else:
            offset = int(request.args.get('offset', 1))
            limit = int(request.args.get('limit', 10))
            model = request.args.get('model', None)
            id = int(request.args.get('id', 0))
            if not model and not id:
                raise HTTPException(400, "Params required model & id ")

            rows = Comment.select().where(Comment.res_id ==id, Comment.res_model ==model).order_by(
                                            Comment.created_at.desc()).paginate(offset, limit)
            data = []
            for row in rows:
                data.append(row.to_dict())
            res.payload = data
        res.code = 200
        res.ok = True
    except HTTPException as e:
        res.code = e.code
        res.message = e.message
    except Exception as e:
        res.message  = str(e)
    return jsonify(res.to_dict()), res.code