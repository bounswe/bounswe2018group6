import LandingPage from "views/Home/LandingPage.jsx";
import ProfilePage from "views/ProfilePage/ProfilePage.jsx";
import LoginPage from "views/LoginPage/LoginPage.jsx";
import SignUpPage from "views/LoginPage/SignUpPage.jsx";

var indexRoutes = [
  { path: "/profile-page", name: "ProfilePage", component: ProfilePage },
  { path: "/login", name: "LoginPage", component: LoginPage },
  { path: "/sign-up", name: "SignUpPage", component: SignUpPage },
  { path: "/", name: "LandingPage", component: LandingPage }
];

export default indexRoutes;
