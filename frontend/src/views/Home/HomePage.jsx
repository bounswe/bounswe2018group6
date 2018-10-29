import React from "react";
// nodejs library that concatenates classes
import classNames from "classnames";
// react components for routing our app without refresh
import { Link } from "react-router-dom";
// @material-ui/core components
import withStyles from "@material-ui/core/styles/withStyles";
// @material-ui/icons
// core components
import Header from "components/Header/Header.jsx";
import Footer from "components/Footer/Footer.jsx";
import GridContainer from "components/Grid/GridContainer.jsx";
import GridItem from "components/Grid/GridItem.jsx";
import Button from "components/CustomButtons/Button.jsx";
import Parallax from "components/Parallax/Parallax.jsx";
// sections for this page
import HeaderLinksLogout from "components/Header/HeaderLinksLogout.jsx";
import SectionCarousel from "./Sections/SectionCarousel.jsx";
import { connect } from "react-redux";
import componentsStyle from "assets/jss/material-kit-react/views/components.jsx";
import { getCookie, LOGGEDIN_COOKIE, TOKEN_COOKIE } from "services/cookies.js";



class HomePage extends React.Component {
  constructor(props) {
    super(props);
  }


  componentDidMount() {
    const { history } = this.props;
    const loggedIn = getCookie(LOGGEDIN_COOKIE);
    if (!loggedIn) return history.push("/");
  }


  render() {
    const { classes, ...rest } = this.props;
    return (
      <div>
        <Header
          brand="Cultidate"
          rightLinks={<HeaderLinksLogout />}
          fixed
          color="transparent"
          changeColorOnScroll={{
            height: 400,
            color: "white"
          }}
          {...rest}
        />
        <Parallax image={require("assets/img/home-background.png")}>
          <div className={classes.container}>
            <GridContainer>
              <GridItem>
                <div className={classes.brand}>
                  <h2 className={classes.title}>Recommended Events</h2>
                  <h3 className={classes.subtitle}>
                    Don't miss events any more.
                    </h3>
                </div>
              </GridItem>
            </GridContainer>
          </div>
        </Parallax>

        <div className={classNames(classes.main, classes.mainRaised)}>

          <SectionCarousel />

        </div>
        <Footer />
      </div>
    );
  }
}

const mapStateToProps = state => ({
  auth: state.auth
});

export default connect(mapStateToProps)(withStyles(componentsStyle)(HomePage));
