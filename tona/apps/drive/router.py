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

from typing import Optional
from typing import List
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from .models.drive_folder import DriveFolder
from .models.drive_file import DriveFile
from .services.localsync import LocalSync
from peewee import DoesNotExist
import os
from tona.utils import logger
v1 = APIRouter()

@v1.get('/folders', response_model=List[DriveFolder.Pydantic])
async def get_folders(skip: Optional[int] = 0, limit: Optional[int] = 100, parent_id: Optional[int] = 0):
    rows = DriveFolder.select()
    if parent_id:
        rows = rows.where(DriveFolder.parent_id == parent_id)
    else:
        rows = rows.where(DriveFolder.parent_id == None)
    return list(rows.offset(skip).limit(limit))

# @v1.post('/folders', response_model=DriveFolder.Pydantic)
# async def post_folders(dir: DriveFolder.Pydantic):
#    return DriveFolder.create(**dir.dict(exclude={'id': ...}, exclude_unset=True))

@v1.get('/files', response_model=List[DriveFile.Pydantic])
async def get_files(skip: int = 0, limit: int = 100, drive_folder_id: Optional[int] = 0):
    rows = DriveFile.select()
    if drive_folder_id:
        rows = rows.where(DriveFile.drive_folder_id == drive_folder_id)
    else:
        rows = rows.where(DriveFile.drive_folder_id == None)
    return list(rows.offset(skip).limit(limit))

@v1.get('/files/{file_id}/{action}')
async def get_files_by_action(file_id: int, action: str):
    try:
        row = DriveFile.get_by_id(file_id)
        if action == 'download':
            return FileResponse(os.path.join("data/drive", row.file[1:]), 200, media_type="application/octet-stream", filename=row.name)
        elif action == 'preview':
            return FileResponse(os.path.join("data/drive", row.file[1:]), 200, media_type=row.mimetype)
        raise HTTPException(400, detail="Action only support download & preview")
    except DoesNotExist as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)
   


@v1.get("/localsync")
async def get_localsync(background_tasks: BackgroundTasks):
    def localsync():
        LocalSync("data/drive").sync()
    background_tasks.add_task(localsync)
    return {"message": "LocalSync sent in the background"}
