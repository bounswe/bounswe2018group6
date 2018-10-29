import { createStore, combineReducers, applyMiddleware, compose } from "redux";
import { connectRouter, routerMiddleware } from "connected-react-router";
import createBrowserHistory from "history/createBrowserHistory";

import createSagaMiddleware from "redux-saga";

import authReducer from "./auth/Reducer";

import saga from "./sagas/saga";

export const history = createBrowserHistory();

const reducers = combineReducers({
    auth: authReducer,
});

const sagaMiddleware = createSagaMiddleware();

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

export const store = createStore(
    connectRouter(history)(reducers),
    composeEnhancers(
        applyMiddleware(
            routerMiddleware(history), // for dispatching history actions
            sagaMiddleware
        )
    )
);

sagaMiddleware.run(saga);
