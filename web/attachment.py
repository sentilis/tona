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
from flask import Blueprint, request, jsonify, send_from_directory, abort
from tona.utils import HTTPException, HTTPResponse
from tona.models.attachment import Attachment
from tona.web.app import app
from tona.utils import save_attachment, location_attachment, remove_attachment

attachment_api_bp = Blueprint('attachment_api_bp', __name__, url_prefix='/api/attachment')

@attachment_api_bp.route("", methods=['POST', 'GET'])
@attachment_api_bp.route("/<int:id>", methods=['DELETE'])
def attachment(id=0):
    res = HTTPResponse()
    try:
        if request.method == 'POST':
            data = request.json
            if data.get('content', None):
                attachment = Attachment.add(**data)
                try:
                    save_attachment(
                        app.config.get('STORAGE'),
                        attachment,
                        data.get('content'))
                except Exception as e:
                    Attachment.remove(attachment.id)
                    raise e
                res.payload = attachment.to_dict()
            else:
                raise HTTPException(404, "Attachment content not is base64")
        elif request.method == 'DELETE':
            attachment = Attachment.get(id)
            remove_attachment(app.config.get('STORAGE'), attachment)
            Attachment.remove(id)
        else:
            offset = int(request.args.get('offset', 1))
            limit = int(request.args.get('limit', 10))
            model = request.args.get('model', None)
            id = int(request.args.get('id', 0))
            if not model and not id:
                raise HTTPException(400, "Params required model & id ")
            rows = Attachment.select().where(Attachment.res_id ==id, Attachment.res_model ==model).order_by(
                                            Attachment.created_at.desc()).paginate(offset, limit)
            data = []
            for row in rows:
                data.append(row.to_dict())
            res.payload = data
        res.code = 200
        res.ok = True
    except HTTPException as e:
        res.code = e.code
        res.message = e.message
        app.logger.error(e)
    except Exception as e:
        res.message  = str(e)
        app.logger.error(e)
    return jsonify(res.to_dict()), res.code

@attachment_api_bp.route('/<action>/<int:id>')
def attachment_action(action, id):
    res = HTTPResponse()
    try:
        attachment = Attachment.get(id)
        fpath, fname = location_attachment(app.config.get('STORAGE'), attachment)
        as_attachment = False
        if action == 'download':
            as_attachment = True
        elif action == 'preview':
            pass
        else:
            raise HTTPException(405, "Only support action download & preview")
        return send_from_directory(fpath, fname, as_attachment=as_attachment)
    except FileNotFoundError as e:
        app.logger.error(e)
        abort(404)
    except HTTPException as e:
        res.code = e.code
        res.message = e.message
        app.logger.error(e)
    except Exception as e:
        res.message  = str(e)
        app.logger.error(e)
    return jsonify(res.to_dict()), res.code
