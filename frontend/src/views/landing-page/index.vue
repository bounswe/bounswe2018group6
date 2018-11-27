<template>
    <video-bg :sources="['src/assets/video/timelapse.mp4']" img="src/assets/video/bg.jpg">
    <github-corner style="position: absolute; top: 0px; border: 0; right: 0;"/>
    <div class=center-item>
        <h1 align="center">Cultidate</h1>
        <h3>Cultidate is a social platform for cultural activities. You can create events,
             join other events, interact with the others, get event recommendations, create 
             your own profile, add other users as friends and message them privately.</h3>
        <el-row class="center-button">
            <router-link to="/signup"><el-button round class="button-margin">Sign up</el-button></router-link>
            <router-link to="/login?redirect=%2Fdashboard"><el-button round class="button-margin">Login</el-button></router-link>
        </el-row>
        </div>
    </video-bg>
</template>

<script>
import VideoBg from 'vue-videobg'
import GithubCorner from '@/components/GithubCorner'


export default {
  name: 'LandingPage',
  components: {
    GithubCorner,
    VideoBg
  },
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.VideoBg {
  min-height: 640px;
}
.center-button{
    display: flex;
    justify-content: center;
}
.button-margin{
    margin: 20px;
}
.center-item{
  position: absolute;
    top: 50%;
    left: 50%;

    -moz-transform: translateX(-50%) translateY(-50%);
    -webkit-transform: translateX(-50%) translateY(-50%);
    transform: translateX(-50%) translateY(-50%);
}
.VideoBg__content {
  text-align: center;
  display: flex;
  justify-content: center;
  background-color: rgba(52, 72, 92, 0.7);
}

img {
  width: 200px;
  margin-top: 120px;
}
h1 {
  margin: 40px 0;
  font-family: 'Dosis', 'Source Sans Pro', 'Helvetica Neue', sans-serif;
  font-weight: 300;
  font-size: 4em;
  color: #ebebeb;
  text-shadow: 1px 1px rgb(184, 183, 180);

}

h3, a {
  font-family: 'Source Sans Pro', 'Helvetica Neue', sans-serif;
  font-weight: 400;
  text-shadow: 1px 1px rgb(184, 183, 180);

//   font-size: 15px;
  color: #ebebeb;
}
</style>
