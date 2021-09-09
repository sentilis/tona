# -*- coding: utf-8 -*-
#   Copyright (C) The TONA Authors
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

from logging import log
import os
import difflib
import re
import magic
from tona.utils import md5sum, logger
from tona.apps.drive.models.drive_file import DriveFile
from tona.apps.drive.models.drive_folder import DriveFolder
import peewee

# sudo apt-get install libmagic1
# python-magic
# https://askubuntu.com/questions/421712/comparing-the-contents-of-two-directories
# https://gist.github.com/amakukha/f489cbde2afd32817f8e866cf4abe779


FILE_LOCK = 'drive.lock'
FILE_TMP = 'drive.tmp'

class LocalSync:

    def __init__(self, path):
        self.path = path
        self.path_lock = os.path.join(self.path, FILE_LOCK)
        self.path_tmp = os.path.join(self.path, FILE_TMP)

    def filestat(self, filename):
        if not os.path.exists(self.path) or not os.path.isdir(self.path):
            os.makedirs(self.path)
        if os.path.isfile(filename) and filename == self.path_lock:
            return self.path_lock
        content = ""
        for root, dirs, files in os.walk(self.path):
            for f in files:
                pathfile = os.path.join(root, f)
                content += f"{md5sum(pathfile)}\t{pathfile}\n"
        with open(filename, "w") as f:
            f.write(content)
            f.close()
        return filename

    def diff(self):
        drivelock = self.filestat(self.path_lock)
        drivetmp = self.filestat(self.path_tmp)
        diff = {}
        with open(drivelock) as f1:
            with open(drivetmp) as f2:
                lines = difflib.unified_diff(f1.readlines(), f2.readlines(), fromfile=FILE_LOCK, tofile=FILE_TMP, n=0)
                for line in lines:
                    for prefix in ('---', '+++', '@@'):
                        if line.startswith(prefix):
                            break
                    else:
                        fname = line.split("\t")[-1]
                        fstate = None
                        if re.search("^-", line):
                            fstate = "del"
                        elif re.search("^\\+", line):
                            fstate = "add"
                        if fstate:
                            if fname in diff.keys():
                                diff[fname][fstate] = True
                            else:
                                diff.update({fname: {fstate: True}})
        fdel = []
        fadd = []
        for fname in diff.keys():
            fstate = diff.get(fname)
            if fstate.get("del", False) and fstate.get('add', False):
                continue
            elif fstate.get('del', False) and not fstate.get('add', False):
                fdel.append(fname)
            elif not fstate.get('del', False) and fstate.get('add', False):
                fadd.append(fname)
        return fdel, fadd

    @property
    def firsttime(self):
        return not os.path.exists(self.path_lock) and not os.path.isfile(self.path_lock)

    def sync(self):
        if self.firsttime:
            with open(self.path_lock, "w") as f:
                f.write("")
                f.close()
            files_deleted, files_added = self.diff()
        else:
            files_deleted, files_added = self.diff()

        logger.info("Start Local Sync")
        logger.info(f"Files deleted: {len(files_deleted)}")
        logger.info(f"Files added: {len(files_added)}")

        paths = {}
        files_added_success = 0
        for f in files_added:
            filename = os.path.basename(f.replace("\n", ""))
            filepath = f.replace("\n", "")
            logger.info("+ %s", filepath)
            mimetype = magic.Magic(mime=True).from_file(filepath)
            filepath = filepath.replace(self.path, "")
            filehash = md5sum(os.path.join(filepath, filename))

            path = ""
            parent_path = ""
            for dir in filepath.split(os.sep):
                if dir != filename:
                    parent_path = path
                    path = os.path.join(path, dir)
                    path_hash = md5sum(path)
                    parent_hash = md5sum(parent_path)
                    if path == parent_path:
                        continue
                    if path not in paths.keys():
                        try:
                            row = DriveFolder.select(DriveFolder.id).where(
                                DriveFolder.path_hash == path_hash).limit(1).get()
                        except peewee.DoesNotExist:
                            data_folder = {"name": dir, "path_hash": path_hash}
                            try:
                                parent_row = DriveFolder.select(DriveFolder.id).where(
                                    DriveFolder.path_hash == parent_hash).limit(1).get()
                                data_folder.update({"parent_id": parent_row.id})
                            except peewee.DoesNotExist:
                                pass
                            row = DriveFolder.create(**data_folder)
                        paths.update({ path: { "id": row.id, "parent_id":  paths.get(parent_path, "") }})

            data_file = { "name": filename, "mimetype": mimetype, "file_hash": filehash,
                          "file": filepath}
            if parent_path != "":
                parent_path = filepath.replace(filename, "")[1:-1]
                data_file.update({"drive_folder_id": paths.get(parent_path)["id"]})
            try:
                parent_row = DriveFile.select(DriveFile.id).where(
                    DriveFile.file_hash == filehash).limit(1).get()
                files_added_success += 1
            except peewee.DoesNotExist:
                DriveFile.create(**data_file)

        files_deleted_success = 0
        for f in files_deleted:
            filename = os.path.basename(f.replace("\n", ""))
            filepath = f.replace("\n", "")
            filepath = filepath.replace(self.path, "")
            filehash = md5sum(os.path.join(filepath, filename))
            try:
                DriveFile.select(DriveFile.id).where(
                    DriveFile.file_hash == filehash).limit(1).get()
                if DriveFile.delete().where(DriveFile.file_hash == filehash).execute():
                    files_deleted_success += 1
                    logger.info("Deleted: %s%s%s", filepath, os.sep, filename)
            except peewee.DoesNotExist:
                files_deleted_success += 1
        if files_added_success == len(files_added) and files_deleted_success == len(files_deleted):
           with open(self.path_tmp, 'r') as tmp:
               with open(self.path_lock, "w") as lock:
                   lock.write(tmp.read())
                   lock.close()
               tmp.close()

