import React from "react";
// @material-ui/core components
import withStyles from "@material-ui/core/styles/withStyles";
import InputAdornment from "@material-ui/core/InputAdornment";
import Icon from "@material-ui/core/Icon";
// @material-ui/icons
import Email from "@material-ui/icons/Email";
import People from "@material-ui/icons/People";
import TextField from '@material-ui/core/TextField';

// core components
import Header from "components/Header/Header.jsx";
import HeaderLinks from "components/Header/HeaderLinks.jsx";
import Footer from "components/Footer/Footer.jsx";
import GridContainer from "components/Grid/GridContainer.jsx";
import GridItem from "components/Grid/GridItem.jsx";
import Button from "components/CustomButtons/Button.jsx";
import Card from "components/Card/Card.jsx";
import CardBody from "components/Card/CardBody.jsx";
import CardHeader from "components/Card/CardHeader.jsx";
import CardFooter from "components/Card/CardFooter.jsx";
import CustomInput from "components/CustomInput/CustomInput.jsx";

import loginPageStyle from "assets/jss/material-kit-react/views/loginPage.jsx";

import { tryRegister, registerReset } from "redux/auth/Actions.js";
import { connect } from "react-redux";

import image from "assets/img/login.jpg";

class SignUpPage extends React.Component {
  constructor(props) {
    super(props);
    // we use this to make the card to appear after the page has been rendered
    this.state = {
      cardAnimaton: "cardHidden",
      first_name: "",
      last_name: "",
      username: "",
      email: "",
      birth_date: "",
      password: "",
      is_corporate_user: false,
      corporate_profile: {
        description: null,
        url: null,
        location: null
      }
    };
  }

  handleSubmit(event) {
    const { cardAnimation, first_name, last_name, username, email, birth_date, password,
            is_corporate_user, corporate_profile } = this.state;
    this.props.tryRegister(first_name, last_name, username, email, birth_date, password,
      is_corporate_user, corporate_profile);
    event.preventDefault();
  }

  componentDidUpdate(prevProps, prevState) {
    const { history } = this.props;
    const { registerInProgress, registerHasError, registerCompleted } = this.props.auth;

    if (registerInProgress && !registerHasError && !registerCompleted) {
    } else if (!registerInProgress && !registerHasError && registerCompleted) {
      this.props.registerReset();
      history.push("/login");
    } else if (!registerInProgress && registerHasError && registerCompleted) {
      this.props.registerReset();
    }
  }

  componentDidMount() {
    setTimeout(
      function () {
        this.setState({ cardAnimaton: "" });
      }.bind(this),
      700
    );
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
              <GridItem xs={12} sm={12} md={6}>
                <Card className={classes[this.state.cardAnimaton]}>
                  <form className={classes.form}>
                    <CardBody>
                      <CustomInput
                        labelText="First Name"
                        id="firstname"
                        formControlProps={{
                          fullWidth: true
                        }}
                        inputProps={{
                          type: "text",
                          endAdornment: (
                            <InputAdornment position="end">
                              <People className={classes.inputIconsColor} />
                            </InputAdornment>
                          ),
                          onChange: e => this.setState({ first_name: e.target.value })
                        }}
                      />
                      <CustomInput
                        labelText="Last Name"
                        id="lastname"
                        formControlProps={{
                          fullWidth: true
                        }}
                        inputProps={{
                          type: "text",
                          endAdornment: (
                            <InputAdornment position="end">
                              <People className={classes.inputIconsColor} />
                            </InputAdornment>
                          ),
                          onChange: e => this.setState({ last_name: e.target.value })
                        }}
                      />
                      <CustomInput
                        labelText="Username"
                        id="username"
                        formControlProps={{
                          fullWidth: true
                        }}
                        inputProps={{
                          type: "text",
                          endAdornment: (
                            <Icon className={classes.inputIconsColor}>
                              account_circle
                              </Icon>
                          ),
                          onChange: e => this.setState({ username: e.target.value })
                        }}
                      />
                      <CustomInput
                        labelText="Email"
                        id="email"
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
                          onChange: event => this.setState({ email: event.target.value })
                        }}
                      />
                      <CustomInput
                        labelText="Birthdate"
                        id="birthday"
                        formControlProps={{
                          fullWidth: true,
                        }}
                        inputProps={{
                          type: "date",
                          defaultValue: "2018-04-11",
                          endAdornment: (
                            <InputAdornment position="end">
                              <Icon className={classes.inputIconsColor}>
                                child_care
                              </Icon>
                            </InputAdornment>
                          ),
                          onChange: e => this.setState({ birth_date: e.target.value })
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
                        Sign Up
                      </Button>
                    </CardFooter>
                  </form>
                  <Button href="/login" simple size="sm" type="button" color="danger">Login Instead?</Button>
                  <br/>
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
    tryRegister: (first_name, last_name, username, email, birth_date, password,
      is_corporate_user, corporate_profile) => dispatch(tryRegister(first_name,
        last_name, username, email, birth_date, password,
        is_corporate_user, corporate_profile)),
    registerReset: () => dispatch(registerReset())
  };
}

const mapStateToProps = state => ({
  auth: state.auth
});

export default connect(
  mapStateToProps,
  bindAction
)(withStyles(loginPageStyle)(SignUpPage));
