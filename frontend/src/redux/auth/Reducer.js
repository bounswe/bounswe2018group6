import {
    LOGIN_REQUEST,
    LOGIN_SUCCESS,
    LOGIN_FAILURE,
    LOGIN_RESET,
    LOGOUT_REQUEST,
    REGISTER_REQUEST,
    REGISTER_SUCCESS,
    REGISTER_FAILURE,
    REGISTER_RESET,
    AUTO_LOGIN
} from "./actionTypes";

const initialState = {
    api_token: "",

    loggedIn: false,

    loginInProgress: false,
    loginHasError: false,
    loginCompleted: false,
    loginError: "",

    registerInProgress: false,
    registerHasError: false,
    registerCompleted: false,
    registerError: "",
    loggedOut: false,
};

export default function(state = initialState, action) {
    const { payload } = action;
    if (action.type === LOGIN_REQUEST) {
        return {
            ...state,
            loginInProgress: true,
            loginHasError: false,
            loginCompleted: false
        };
    } else if (action.type === LOGIN_SUCCESS) {
        return {
            ...state,
            token: payload.token,
            loggedIn: true,
            loginInProgress: false,
            loginHasError: false,
            loginCompleted: true
        };
    } else if (action.type === LOGIN_FAILURE) {
        return {
            ...state,
            loginInProgress: false,
            loginHasError: true,
            loginCompleted: true,
            loginError: payload.detail[0]
        };
    } else if (action.type === LOGIN_RESET) {
        return {
            ...state,
            loginInProgress: false,
            loginHasError: false,
            loginCompleted: false
        };
    }
    if (action.type === REGISTER_REQUEST) {
        return {
            ...state,
            registerInProgress: true,
            registerHasError: false,
            registerCompleted: false
        };
    } else if (action.type === REGISTER_SUCCESS) {
        return {
            ...state,
            user: payload.user,
            token: payload.auth_token,
            loggedIn: true,
            registerInProgress: false,
            registerHasError: false,
            registerCompleted: true
        };
    } else if (action.type === REGISTER_FAILURE) {
        return {
            ...state,
            registerInProgress: false,
            registerHasError: true,
            registerCompleted: true,
            registerError: payload.detail[0]
        };
    } else if (action.type === REGISTER_RESET) {
        return {
            ...state,
            registerInProgress: false,
            registerHasError: false,
            registerCompleted: false
        };
    } else if (action.type === AUTO_LOGIN) {
        const { user, token } = payload;
        return {
            ...state,
            user,
            token,
            loggedIn: true
        };
    } else if (action.type === LOGOUT_REQUEST) {
        return {
            ...state,
            user: {},
            token: "",

            loggedIn: false,

            loginInProgress: false,
            loginHasError: false,
            loginCompleted: false,
            loginError: "",
            loggedOut: true,
        };
    }

    return state;
}
