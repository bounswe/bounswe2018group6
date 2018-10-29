import React from "react";
import ReactDOM from "react-dom";
import { createBrowserHistory } from "history";
import { Router, Route, Switch } from "react-router-dom";
import { Provider } from "react-redux";
import { store, history } from "redux/configureStore.js";
import { ConnectedRouter } from "connected-react-router";


import indexRoutes from "routes/index.jsx";

import "assets/scss/material-kit-react.css";

var hist = createBrowserHistory();

class Main extends React.Component {
  render() {
    return (
      <Router history={hist}>
        <Switch>
          {indexRoutes.map((prop, key) => {
            return <Route exact path={prop.path} key={key} component={prop.component} />;
          })}
        </Switch>
      </Router>
    );
  }
}

ReactDOM.render(
  <Provider store={store}>
        <ConnectedRouter history={history}>
            <Main />
        </ConnectedRouter>
    </Provider>,
  document.getElementById("root")
);
