import { URLJoin } from "../../utils";
import { API_URL } from "../../constants";

export const runLocalSync = async (self) => {
    return self.fetch(URLJoin(API_URL, `/api/v1/drive/localsync`));
}

export const getContentFolder = async (id) => {
    let files = [];
    let folders = [];
    if (id === parseInt(id, 10)) {
        try {
            folders = await fetch(
                URLJoin(API_URL, `/api/v1/drive/folders?parent_id=${id}`)
            ).then((r) => r.json());
        } catch (error) { }
        try {
            files = await fetch(
                URLJoin(
                    API_URL,
                    `/api/v1/drive/files?drive_folder_id=${id}`
                )
            ).then((r) => r.json());
        } catch (error) { }
    } else {
        try {
            folders = await id
                .fetch(URLJoin(API_URL, `/api/v1/drive/folders`))
                .then((r) => r.json());
        } catch (error) { }
        try {
            files = await id
                .fetch(URLJoin(API_URL, `/api/v1/drive/files`))
                .then((r) => r.json());
        } catch (error) { }
    }
    return {
        folders: folders,
        files: files,
    };
}


export const routeBreadcrumbs = (items, id, name) => {
    let found = items.findIndex((item) => item.id == id);
    if (found >= 0) {
        items = [...items.slice(0, found + 1)];
    } else {
        items = [...items, { id: id, name: name }];
    }
    return items
}