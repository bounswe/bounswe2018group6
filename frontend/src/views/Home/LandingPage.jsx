import React from "react";
// nodejs library that concatenates classes
import classNames from "classnames";
import { Link } from "react-router-dom";


// @material-ui/core components
import withStyles from "@material-ui/core/styles/withStyles";
import { Favorite, Star } from "@material-ui/icons";

// @material-ui/icons

// core components
import Header from "components/Header/Header.jsx";
import Footer from "components/Footer/Footer.jsx";
import GridContainer from "components/Grid/GridContainer.jsx";
import GridItem from "components/Grid/GridItem.jsx";
import Button from "components/CustomButtons/Button.jsx";
import HeaderLinks from "components/Header/HeaderLinks.jsx";
import Parallax from "components/Parallax/Parallax.jsx";

import landingPageStyle from "assets/jss/material-kit-react/views/landingPage.jsx";

// Sections for this page
const dashboardRoutes = [];

class LandingPage extends React.Component {
  render() {
    const { classes, ...rest } = this.props;
    return (
      <div>
        <Header
          color="dark"
          routes={dashboardRoutes}
          brand="Cultidate"
          rightLinks={<HeaderLinks />}
          fixed
          changeColorOnScroll={{
            height: 400,
            color: "white"
          }}
          {...rest}
        />
        <Parallax filter image={require("assets/img/land.jpg")}>
          <div className={classes.container}>
            <GridContainer>
              <GridItem xs={12} sm={12} md={6}>
                <h1 className={classes.title}>Cultidate</h1>
                <h4>
                  Cultidate is a social platform for cultural activities. You can create events, join other events, interact with the others, get event recommendations, create your own profile, add other users as friends and message them privately.
</h4>
                <br />

                <Button
                  color="danger"
                  round
                  size="lg"
                  href="/sign-up"
                  rel="noopener noreferrer"
                >
                  <i className="fas" /><Favorite />Sign Up
                </Button>
                <Button
                  color="danger"
                  round
                  size="lg"
                  href="/login"
                  rel="noopener noreferrer"
                >
                  <i className="fas" /><Star />Login
                </Button>
              </GridItem>
            </GridContainer>
          </div>
        </Parallax>
        <Footer />
      </div>
    );
  }
}

export default withStyles(landingPageStyle)(LandingPage);
