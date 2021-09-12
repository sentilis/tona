import { DateToUTC, getBrowseTimeZone, URLJoin } from "../../utils";
import { API_URL } from "../../constants";
import moment from "moment-timezone";


export const getLastEntries = async (self) => {
    let lastEntries = [];
    try {
        let res = await self.fetch(URLJoin(API_URL, `/api/v1/time-tracking/entries?skip=0&limit=30&sort_by=-created_at`));
        if (res.status == 200) {
            let data = await res.json();
            lastEntries = data["payload"];
        }
    } catch (error) {

    }

    return lastEntries;
}

export const formatDuration = (seconds, format = "clock") => {
    function pad(number) {
        var r = String(number);
        if (r.length === 1) {
            r = "0" + r;
        }
        return r;
    }
    var minutes = parseInt(seconds / 60);
    var hours = parseInt(minutes / 60);
    seconds = parseInt(seconds - minutes * 60);
    minutes = parseInt(minutes - hours * 60);
    var d = pad(hours) + ":" + pad(minutes) + ":" + pad(seconds);
    if (format == "human") {
        d = pad(hours) + "H" + pad(minutes) + "M" + pad(seconds) + "S";
    }
    return d;
};


export const entryEdit = (field, entry) => {
    let data = {};
    if (field == 'name' && entry.name.length) {
        data[field] = entry.name;
    }
    if (field == 'start' && entry.start.length) {
        data[field] = DateToUTC(new Date(moment.tz(entry.start, getBrowseTimeZone()).valueOf()))
    }
    if (field == 'stop' && entry.stop.length) {
        data[field] = DateToUTC(new Date(moment.tz(entry.stop, getBrowseTimeZone()).valueOf()))
    }

    if (Object.keys(data).length == 0) {
        return;
    }

    fetch(URLJoin(API_URL, `/api/v1/time-tracking/entries/${entry.id}`), {
        method: "put",
        body: JSON.stringify(data),
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    }).then((res) => {
        //console.log(res)
    }).catch(err => {
        console.log(err)
    });
};


export const entryDelete = (entry) => {
    fetch(URLJoin(API_URL, `/api/v1/time-tracking/entries/${entry.id}`), {
        method: "delete"
    }).then((res) => {
        //console.log(res)
    }).catch(err => {
        console.err(err)
    });
}