/*eslint-disable*/
import React from "react";
// react components for routing our app without refresh
import { Link } from "react-router-dom";

// @material-ui/core components
import withStyles from "@material-ui/core/styles/withStyles";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import Tooltip from "@material-ui/core/Tooltip";

// @material-ui/icons
import { Apps, Close, CloudDownload } from "@material-ui/icons";
import { logout, loginReset } from "redux/auth/Actions.js";
import { setCookie, getCookie, LOGGEDIN_COOKIE, TOKEN_COOKIE, removeCookie, } from "services/cookies.js";
import { connect } from "react-redux";


// core components
import CustomDropdown from "components/CustomDropdown/CustomDropdown.jsx";
import Button from "components/CustomButtons/Button.jsx";

import headerLinksStyle from "assets/jss/material-kit-react/components/headerLinksStyle.jsx";

class HeaderLinksLogout extends React.Component {
  constructor(props) {
    super(props);
  }

  handleSubmit(event) {    
    removeCookie(TOKEN_COOKIE);
    removeCookie(LOGGEDIN_COOKIE);
    this.props.loginReset();
  }


  // componentDidMount() {
  //   const loggedIn = getCookie(LOGGEDIN_COOKIE);
  //   const { history } = this.props;
  //   if (!loggedIn) {
  //     removeCookie(TOKEN_COOKIE);
  //     removeCookie(LOGGEDIN_COOKIE);
  //     return history.push("/");
  //   }
  // }

  // componentDidUpdate(prevProps, prevState) {
  //   const { history } = this.props;
  //   const loggedIn = getCookie(LOGGEDIN_COOKIE);
  //   if (!loggedIn) {
  //     removeCookie(TOKEN_COOKIE);
  //     removeCookie(LOGGEDIN_COOKIE);
  //     return history.push("/");
  //   }
  // }


  render() {
    const { classes } = this.props;
    return (
      <List className={classes.list}>
        <ListItem className={classes.listItem}>
          <CustomDropdown
            noLiPadding
            buttonText="EVENTS"
            buttonProps={{
              className: classes.navLink,
              color: "transparent"
            }}
            buttonIcon={Apps}
            dropdownList={[
              <Link to="/" className={classes.dropdownLink}>
                Other Events
            </Link>,
              <a
                href=""
                target="_blank"
                className={classes.dropdownLink}
              >
                Some Events
            </a>
            ]}
          />
        </ListItem>
        <ListItem className={classes.listItem}>
          <Button
            href="/"
            color="transparent"
            target="_blank"
            className={classes.navLink}
          >
            <CloudDownload className={classes.icons} /> Download App
        </Button>
        </ListItem>
        <ListItem className={classes.listItem}>
          <Tooltip
            id="instagram-twitter"
            title="Follow us on twitter"
            placement={window.innerWidth > 959 ? "top" : "left"}
            classes={{ tooltip: classes.tooltip }}
          >
            <Button
              href="https://twitter.com/"
              target="_blank"
              color="transparent"
              className={classes.navLink}
            >
              <i className={classes.socialIcons + " fab fa-twitter"} />
            </Button>
          </Tooltip>
        </ListItem>
        <ListItem className={classes.listItem}>
          <Tooltip
            id="instagram-facebook"
            title="Follow us on facebook"
            placement={window.innerWidth > 959 ? "top" : "left"}
            classes={{ tooltip: classes.tooltip }}
          >
            <Button
              color="transparent"
              href="https://www.facebook.com/"
              target="_blank"
              className={classes.navLink}
            >
              <i className={classes.socialIcons + " fab fa-facebook"} />
            </Button>
          </Tooltip>
        </ListItem>
        <ListItem className={classes.listItem}>
          <Tooltip
            id="instagram-tooltip"
            title="Follow us on instagram"
            placement={window.innerWidth > 959 ? "top" : "left"}
            classes={{ tooltip: classes.tooltip }}
          >
            <Button
              color="transparent"
              href="https://www.instagram.com/"
              target="_blank"
              className={classes.navLink}
            >
              <i className={classes.socialIcons + " fab fa-instagram"} />
            </Button>
          </Tooltip>
          <Button
            color="transparent"
            href="/"
            onClick={e => this.handleSubmit(e)}
            className={classes.navLink}
          >
            <Close className={classes.icons} /> Logout
        </Button>
        </ListItem>
      </List>
    );
  }

}

function bindAction(dispatch) {
  return {
    logout: () => dispatch(logout()),
    loginReset: () => dispatch(loginReset())
  };
}

const mapStateToProps = state => ({
  auth: state.auth
});


export default connect(
  mapStateToProps,
  bindAction
)(withStyles(headerLinksStyle)(HeaderLinksLogout));
