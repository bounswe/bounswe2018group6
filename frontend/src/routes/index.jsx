import LandingPage from "views/Home/LandingPage.jsx";
import LoginPage from "views/LoginPage/LoginPage.jsx";
import SignUpPage from "views/LoginPage/SignUpPage.jsx";
import HomePage from "views/Home/HomePage.jsx"
var indexRoutes = [
  { path: "/login", name: "LoginPage", component: LoginPage },
  { path: "/sign-up", name: "SignUpPage", component: SignUpPage },
  { path: "/", name: "LandingPage", component: LandingPage },
  { path: "/home", name: "HomePage", component: HomePage }
];

export default indexRoutes;
