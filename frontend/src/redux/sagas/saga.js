import { call, put, takeLatest } from "redux-saga/effects";

import { LOGIN_REQUEST, REGISTER_REQUEST } from "../auth/actionTypes";
import { loginSuccess, loginFailure, registerFailure, registerSuccess } from "../auth/Actions";

import api from "./api";

const tryLoginSaga = function*(action) {
    const { username, password } = action.payload;

    try {
        const loginResponse = yield call(api.doLogin, username, password);
        if (loginResponse) {
            console.log("​loginResponse", loginResponse);

            if (loginResponse.status === 200) {
                yield put(loginSuccess(loginResponse.responseBody));
            } else if (loginResponse.status === 400) {
                console.log("Something wrong! Got a status 400", loginResponse.responseBody);
                yield put(loginFailure(loginResponse.responseBody));
            } else {
                console.log("Something wrong! Got an unknown status.", loginResponse);
                yield put(loginFailure({ detail: ["Unknown status. Check console!"] }));
            }
        } else {
            console.log("Login failed by api. No response !");
            yield put(loginFailure({ detail: ["No response fetched. Please contact the API team!"] }));
        }
    } catch (err) {
        console.log("Login failed by api. Error => ", err);
        yield put(loginFailure({ detail: [err.detail] }));
    }
};

const tryRegisterSaga = function*(action) {
    const { first_name, last_name,  username, email, birth_date, password, 
        is_corporate_user, corporate_profile} = action.payload;
    try {
        const registerResponse = yield call(api.doRegister, first_name, last_name, 
                                            username, email, birth_date, password, 
                                            is_corporate_user, corporate_profile);

        if (registerResponse) {
            console.log("registerResponse", registerResponse);

            if (registerResponse.status === 201 || registerResponse.status === 201) {
                yield put(registerSuccess(registerResponse.responseBody));
            } else if (registerResponse.status === 400) {
                console.log("Something wrong! Got a status 400", registerResponse.responseBody);
                yield put(registerFailure(registerResponse.responseBody));
            } else {
                console.log("Something wrong! Got an unknown status.", registerResponse);
                yield put(registerFailure({ detail: ["Unknown status. Check console!"] }));
            }
        } else {
            console.log("Register failed by api. No response !");
            yield put(registerFailure({ detail: ["No response fetched. Please contact the API team!"] }));
        }
    } catch (err) {
        console.log("Register failed by api. Error => ", err);
        yield put(registerFailure({ detail: [err.detail] }));
    }
};


const saga = function*() {
    //AUTH
    yield takeLatest(LOGIN_REQUEST, tryLoginSaga);
    yield takeLatest(REGISTER_REQUEST, tryRegisterSaga);
};

export default saga;
