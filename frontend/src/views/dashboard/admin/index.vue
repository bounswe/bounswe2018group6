<template>
  <div class="dashboard-editor-container">
    <github-corner style="position: absolute; top: 0px; border: 0; right: 0;"/>
    <panel-group @handleSetLineChartData="handleSetLineChartData"/>
    <el-row :gutter="32">
      <el-col :xs="{span: 24}" :sm="{span: 12}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}" style="margin-bottom:30px;">
        <todo-list/>
      </el-col>
      <el-col :span="8">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span style="font-weight:bold; color: #4b7ad3;">Following events</span>
            </div>
            <div v-for="event in following_events" :key="event.title" class="text item">
              <router-link :to="'events/show-event/' + event.event.id"><mallki :text="event.event.title" class-name="mallki-text"/></router-link>
              <span style="float: right; color: #77450d; font-weight:bold;">{{ beautifyDate(event.event.date) }}</span>
            </div>
          </el-card>
          <el-card class="box-card" style="margin-top: 30px;">
            <div slot="header" class="clearfix">
              <span style="font-weight:bold; color: #4b7ad3;">Owned events</span>
            </div>
            <div v-for="event in owned_events" :key="event.title" class="text item">
              <router-link :to="'events/show-event/' + event.id"><mallki :text="event.title" class-name="mallki-text"/></router-link>
              <span style="float: right; color: #77450d; font-weight:bold;">{{ beautifyDate(event.date) }}</span>
            </div>
          </el-card>
      </el-col>
      <el-col :span="8" style="margin-left: 57px;">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span style="font-weight:bold; color: #4b7ad3;">Notifications</span>
            <el-button style="float: right; padding: 3px 0" type="text" @click.prevent.native="markNotificationsRead">Mark notifications read</el-button>
          </div>
          <div v-for="notification in notifications" :key="notification.id" class="text item">
            <mallki :text="notification.data" class-name="mallki-text"/>
            <span style="float: right; color: #77450d; font-weight:bold;">{{ beautifyDate(notification.timestamp) }}</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import GithubCorner from '@/components/GithubCorner'
import PanelGroup from './components/PanelGroup'
import TodoList from './components/TodoList'
import BoxCard from './components/BoxCard'
import Mallki from '@/components/TextHoverEffect/Mallki'
import { getUserInfo, getAllNotifications, getUnreadNotifications, makeNotificationsRead } from '@/api/user'
export default {
  name: 'DashboardAdmin',
  components: {
    GithubCorner,
    PanelGroup,
    TodoList,
    BoxCard,
    Mallki
  },
  data() {
    return {
      following_events: null,
      owned_events: null,
      notifications: null
    }
  },
  created() {
    this.userDetails(this.$store.state.user.user_id)
    this.interval = setInterval(() => {
      this.getAllNotification()()
    }, 3000)
  },
  methods: {
    userDetails(user_id) {
      getUserInfo(user_id).then(response => {
        this.following_events = response.data.followings.events
        this.owned_events = response.data.owned_events
      })
    },
    beautifyDate(date) {
      var d = new Date(date)
      date = (d.getDate()<10?'0':'') + d.getDate() + "/" + ((d.getMonth() + 1)<10?'0':'') + (d.getMonth() + 1) + "/" +
               d.getFullYear() + " - " + (d.getHours()<10?'0':'')+  d.getHours() + ":" + (d.getMinutes()<10?'0':'') + d.getMinutes()
      return date
    },
    getAllNotification() {
      getUnreadNotifications().then(response => {
        this.notifications = response.data.notifications
      })
    },
    markNotificationsRead() {
      makeNotificationsRead().then(response => {
        this.getAllNotification()
      })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}
.text {
  font-size: 14px;
}
.item {
  margin-bottom: 18px;
}
.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both
}
.box-card {
  width: 480px;
}
.mallki-text {
  font-size: 15px;
  color: black;
}
</style>