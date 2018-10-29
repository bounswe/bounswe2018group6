import Cookies from "universal-cookie";

const cookies = new Cookies();

export const TOKEN_COOKIE = "TOKEN_COOKIE";
export const LOGGEDIN_COOKIE = "LOGGEDIN_COOKIE";

export const setCookie = (key, value) => {
    return cookies.set(key, value, { path: "/" });
};

export const getCookie = key => {
    return cookies.get(key);
};

export const removeCookie = key => {
    return cookies.remove(key);
};

export const addCookieListener = func => {
    return cookies.addChangeListener(func);
};

export const removeCookieListener = func => {
    return cookies.removeChangeListener(func);
};