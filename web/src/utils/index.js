import moment from 'moment-timezone';

export const URLJoin = (base, endpoint) => {
    return new URL(endpoint, base).toString()
}

export const Clipboard = (text) => {
    navigator.clipboard.writeText(text);
}

export const DateToUTC = (date) => {

    function pad(number) {
        var r = String(number);
        if (r.length === 1) {
            r = '0' + r;
        }
        return r;
    }
    return date.getUTCFullYear()
        + '-' + pad(date.getUTCMonth() + 1)
        + '-' + pad(date.getUTCDate())
        + 'T' + pad(date.getUTCHours())
        + ':' + pad(date.getUTCMinutes())
        + ':' + pad(date.getUTCSeconds())
        + '.' + String((date.getUTCMilliseconds() / 1000).toFixed(3)).slice(2, 5)
        + 'Z';
}

export const getBrowseTimeZone = () => {
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
}

export const getHTML5DateTime = (dt) => {
    let local = moment(dt).tz(getBrowseTimeZone()).format(moment.DATETIME_LOCAL_MS)
    return local.substring(0, 19)
};