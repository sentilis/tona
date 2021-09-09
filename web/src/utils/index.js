

export const URLJoin = (base, endpoint) => {
    return new URL(endpoint, base).toString()
}

export const Clipboard = (text) =>{
    navigator.clipboard.writeText(text);
}