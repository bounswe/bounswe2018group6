import React from "react";
// @material-ui/core components
import withStyles from "@material-ui/core/styles/withStyles";
import InputAdornment from "@material-ui/core/InputAdornment";
import Icon from "@material-ui/core/Icon";
// @material-ui/icons
import Email from "@material-ui/icons/Email";
import People from "@material-ui/icons/People";
// core components
import Header from "components/Header/Header.jsx";
import HeaderLinks from "components/Header/HeaderLinks.jsx";
import Footer from "components/Footer/Footer.jsx";
import GridContainer from "components/Grid/GridContainer.jsx";
import GridItem from "components/Grid/GridItem.jsx";
import Button from "components/CustomButtons/Button.jsx";
import Card from "components/Card/Card.jsx";
import CardBody from "components/Card/CardBody.jsx";
//import CardHeader from "components/Card/CardHeader.jsx";
import CardFooter from "components/Card/CardFooter.jsx";
import CustomInput from "components/CustomInput/CustomInput.jsx";
import Typography from '@material-ui/core/Typography';

import loginPageStyle from "assets/jss/material-kit-react/views/loginPage.jsx";
import { tryLogin, loginReset } from "redux/auth/Actions.js";
import { connect } from "react-redux";

import { setCookie, getCookie, LOGGEDIN_COOKIE, TOKEN_COOKIE } from "services/cookies.js";

import image from "assets/img/login.jpg";

class LoginPage extends React.Component {
  constructor(props) {
    super(props);
    // we use this to make the card to appear after the page has been rendered
    this.state = {
      cardAnimaton: "cardHidden",
      username: "",
      password: "",
    };
  }

  handleSubmit(event) {
    const { username, password } = this.state;
    this.props.tryLogin(username, password);
    event.preventDefault();
  }

  componentDidMount() {
    const { history } = this.props;
    const loggedIn = getCookie(LOGGEDIN_COOKIE);
    if (loggedIn) return history.push("/home");

    setTimeout(
      function () {
        this.setState({ cardAnimaton: "" });
      }.bind(this),
      700
    );
  }

  componentDidUpdate(prevProps, prevState) {
    const { history } = this.props;
    const { loginInProgress, loginHasError, loginCompleted, api_token, loggedIn } = this.props.auth;

    if (loginInProgress && !loginHasError && !loginCompleted) {
    } else if (!loginInProgress && !loginHasError && loginCompleted) {
      setCookie(TOKEN_COOKIE, api_token, { path: "/" });
      setCookie(LOGGEDIN_COOKIE, loggedIn, { path: "/" });
      this.props.loginReset();
      history.push("/home");
    } else if (!loginInProgress && loginHasError && loginCompleted) {
      this.props.loginReset();
    }
  }


  render() {
    const { classes, ...rest } = this.props;
    return (
      <div>
        <Header
          absolute
          color="transparent"
          brand="Cultidate"
          rightLinks={<HeaderLinks />}
          {...rest}
        />
        <div
          className={classes.pageHeader}
          style={{
            backgroundImage: "url(" + image + ")",
            backgroundSize: "cover",
            backgroundPosition: "top center"
          }}
        >
          <div className={classes.container}>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={4}>
                <Card className={classes[this.state.cardAnimaton]}>
                  <form className={classes.form}>
                    <CardBody>
                      <CustomInput
                        labelText="Username"
                        id="username"
                        formControlProps={{
                          fullWidth: true
                        }}
                        inputProps={{
                          type: "email",
                          endAdornment: (
                            <InputAdornment position="end">
                              <Email className={classes.inputIconsColor} />
                            </InputAdornment>
                          ),
                          onChange: e => this.setState({ username: e.target.value })
                        }}
                      />
                      <CustomInput
                        labelText="Password"
                        id="pass"
                        formControlProps={{
                          fullWidth: true
                        }}
                        inputProps={{
                          type: "password",
                          endAdornment: (
                            <InputAdornment position="end">
                              <Icon className={classes.inputIconsColor}>
                                lock_outline
                              </Icon>
                            </InputAdornment>
                          ),
                          onChange: e => this.setState({ password: e.target.value })
                        }}
                      />
                    </CardBody>
                    <CardFooter className={classes.cardFooter}>
                      <Button color="danger" size="lg" onClick={e => this.handleSubmit(e)}>
                        Login
                      </Button>
                    </CardFooter>
                  </form>
                  <Button href="/sign-up" simple type="button" color="danger">Sign Up Instead?</Button>
                </Card>
              </GridItem>
            </GridContainer>
          </div>
          <Footer whiteFont />
        </div>
      </div>
    );
  }
}

function bindAction(dispatch) {
  return {
    tryLogin: (username, password) => dispatch(tryLogin(username, password)),
    loginReset: () => dispatch(loginReset())
  };
}

const mapStateToProps = state => ({
  auth: state.auth
});

export default connect(
  mapStateToProps,
  bindAction
)(withStyles(loginPageStyle)(LoginPage));
