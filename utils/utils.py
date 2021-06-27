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
import os
import base64
from flask import jsonify
import csv
import subprocess

class HTTPException(BaseException):

    def __init__(self, code, message, *args: object) -> None:
        self.code = code
        self.message = message
        super().__init__(*args)


class HTTPResponse:
    ok = False
    message = None
    payload = {}
    erros = []
    code = 500

    def to_dict(self):
        data = {
            "ok": self.ok,
            "code": self.code
        }
        if self.message:
            data.update(dict(message=self.message))
        if self.payload:
            data.update(dict(payload=self.payload))
        if len(self.erros):
            data.update(dict(erros=self.erros))
        return data

    def jsonify(self):
        return jsonify(self.to_dict()), self.code

def api_response(ok=False, message=None, payload=None):
    return {
        "ok": ok,
        "message": message,
        "payload": payload
    }

def str2int(val: str):
    try:
        val = int("".join([n for n in val if n.isdigit()]))
        return val
    except Exception as e:
        pass
    return 0

def is_base64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        return False

def is_binary_base64(s):
    bs = base64.b64decode(s)
    textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    return bool(bs.translate(None, textchars))

def location_attachment(storage, attachment) -> tuple:
    res_model = str(attachment.res_model).replace('_', '/')
    fname = f"{attachment.id}-{attachment.name}"
    fpath = os.path.join(storage, res_model, str(attachment.res_id))
    return fpath, fname

def save_attachment(storage, attachment, content) -> bool:
    fpath, fname = location_attachment(storage, attachment)
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    decoded = base64.b64decode(content)
    output_file = open(os.path.join(fpath, fname), 'wb')
    output_file.write(decoded)
    output_file.close()
    return True

def remove_attachment(storage, attachment) -> bool:
    fpath, fname = location_attachment(storage, attachment)
    ffile = os.path.join(fpath, fname)
    if os.path.exists(ffile):
        os.remove(ffile)
    return True

def build_csv(storage, file_name, data, is_tmp=False, is_base64=False):
    fpath = storage
    if is_tmp:
        fpath = os.path.join(fpath, "tmp")
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    fpath = os.path.join(fpath, file_name)
    with open(fpath, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    if is_base64:
        with open(fpath, 'rb') as csvfile:
            return base64.b64encode(csvfile.read())
    return fpath

def build_pdf(storage, file_name, header, body, footer, is_tmp=False, is_base64=False):
    fpath = storage
    if is_tmp:
        fpath = os.path.join(fpath, "tmp")
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    fheader = header
    fbody = body
    ffooter = footer
    contents = {'header': header, 'body': body, 'footer': footer}
    for content in contents:
        if not os.path.exists(contents.get(content)):
            ptmp = os.path.join(fpath, f"pdf_{content}.html")
            with open(ptmp, "w", encoding='utf-8') as f:
                f.write(contents.get(content))
                f.close()
            if content == 'header':
                fheader = ptmp
            elif content == 'body':
                fbody = ptmp
            elif content == 'footer':
                ffooter = ptmp
    fpath = os.path.join(fpath, file_name)
    args = [
        "wkhtmltopdf", fbody,
        "--footer-html", ffooter,
        "--header-html", fheader,
        fpath
    ]
    subprocess.run(args)
    if is_base64:
        with open(fpath, 'rb') as csvfile:
            return base64.b64encode(csvfile.read())
    return fpath
