<template>
  <div class="components-container">
    <el-row>
      <el-col :span="14"><div class="grid-content bg-purple-light">
        <center style="font-size: 25px; font-weight:bold;font-family: 'Helvetica', 'Arial', sans-serif; color: #38A1F3;"> {{ eventDetails.title }} </center>
        <p style="font-size: 20px; margin-left: 20px;">by {{ eventDetails.owner.username }} </p>
        <el-button size="large" style="float: right; margin-right: 20px;" type="success" @click.native.prevent="rateUpEvent" icon="el-icon-arrow-up" circle></el-button>
        <p style="font-size: 20px; margin-left: 20px; font-weight:bold;">Date and Time</p>
        <span style="font-size: 20px; margin-left: 20px;"> {{ beautifyDate(eventDetails.date) }}</span>
        <span style="font-size: 20px; float: right; margin-right: 34px;">{{ eventDetails.vote_count }}</span>
        <div></div>
        <el-button size="large" style="float: right; margin-right: 20px;" type="danger" @click.native.prevent="rateDownEvent" icon="el-icon-arrow-down" circle></el-button>
        <div style="font-size: 20px; margin-left: 20px; margin-top: 130px;"> <span>Price: {{ eventDetails.price }} ₺ </span>
        <el-select v-model="attend" placeholder="Tell Us Your Status" style="margin-right: 20px; float: right;" @change="attendanceEvent">
        <p style="font-size: 20px; margin-left: 20px;">{{ eventDetails.date }}</p>
        <div style="font-size: 20px; margin-left: 20px; margin-top: 130px;"> <span>Price: {{ eventDetails.price }} ₺ </span>
          <el-select v-model="attend" placeholder="Tell Us Your Status" style="margin-right: 20px; float: right;" @change="attendanceEvent">
            <el-option v-for="item in options" :key="item.attend" :label="item.label" :value="item.attend"/>
          </el-select>
          <span style="margin-right: 20px; float: right;"> Attendance Status </span>
        </div>
      </div>
      </el-col>
      <el-carousel trigger="click" height="350px">
        <el-carousel-item>
          <img :src="eventDetails.featured_image" class="imgs">
        </el-carousel-item>
        <el-carousel-item v-for="media in eventDetails.medias" :key="media.id">
          <img :src="media.file" class="imgs">
        </el-carousel-item>
      </el-carousel>
    </el-row>
<el-row :gutter="32">
  <el-col :xs="24" :sm="24" :md="16" :lg="16">
    <div style="margin-top: 20px">
      <span style="font-size: 20px; font-weight:bold;">Description</span>
      <el-card class="box-card">
        <div class="text item">
          {{ eventDetails.description }}
        </div>
      </el-card>
    </div>
  </el-col>

  <el-col :xs="24" :sm="24" :md="8" :lg="8">
    <div style="margin-top: 30 px" >
      <p/>
      <el-tag v-for="tag in eventDetails.tags" :key="tag" size="medium">
        {{ tag.name }}
      </el-tag>
      <el-button style="float: right;" type="primary" plain size="medium" @click.native.prevent="followEvent">{{ following }}</el-button>
      <router-link v-if="is_owner" :to="'/events/edit-event/' + event_id">
        <el-button >Edit Event</el-button>
      </router-link>
    </div>
    <div style="margin-top: 20px">
      <span style="font-size: 20px; font-weight:bold;">Description</span>
      <el-button v-if="is_owner" size="medium" style="float: right;" type="danger" @click="deleteEvent">Delete Event</el-button>
      <p>{{ eventDetails.description }} </p>
    </div>
    <googlemaps-geocoder
    :request="{
      location: { lat: 41.017822, lng: 28.954770 },
    }">
      <template slot-scope="props">
        <div class="name">{{ props.results[1].address_components[4].long_name }}</div>
        <div class="name">{{ props.results[1].address_components[5].long_name }}</div>
        <div class="address">{{ props.results[0].address_components.administrative_area_level_1 }}</div>
      </template>
    </googlemaps-geocoder>
  
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>Comments</span>
        <el-popover placement="left" width="400" trigger="click">
          <el-input type="textarea" autosize placeholder="Please comment..." v-model="comment"></el-input>
          <el-button style="float: left; margin-top: 5px;" type="primary" @click.native.prevent="addComment">Submit</el-button>
          <el-button style="float: right; padding: 3px 0" type="text" slot="reference">Add Comment</el-button>
        </el-popover>
      </div>
      <div v-for="com in eventDetails.comments" :key="com.content" class="text item">
         <span> {{ com.content }} </span>
         <span style="font-weight: bold; margin-left: 5px"> {{ 'by ' + com.owner.username }} </span>
         <el-button v-if="com.owner.username === owner_username" size="mini" style="float: right;" type="danger" @click.native.prevent="deleteComment(com.id)">Delete</el-button>
      </div>
    </el-card>
    <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :md="24" :lg="24">
        <googlemaps-map
          ref="map"
          :center.sync="mapCenter"
          :zoom.sync="zoom"
          style="height: 350px; max-width: 50%; margin-left: 50%;"
          class="map">
          <googlemaps-marker
            :position="{ lat: 41.017822, lng: 28.954770 }"
            title="Baran Et Mangal"
            label="Baran Et Mangal" />
        </googlemaps-map>
      </el-col>
    </el-row>

  </div>
</template>

<script>

import { getEventDetail, follow, unfollow, attendance, rate, delEvent, createComment, delComment } from '@/api/event'
import { getUserInfo } from '@/api/user'
import { getToken } from '@/utils/auth' // getToken from cookie

export default {
  name: 'ShowEvent',
  components: {},
  data() {
    return {
      apiAddress: 'https://cultidate.herokuapp.com/api/medias/',
      headers : {
        // 'Content-Type': 'multipart/form-data',
        'Authorization': 'Token ' + getToken(),
      },
      additionalBody: {
        event: null
      },
      keyName: 'file',
      mediaLimit : 5,
      options: [{
        attend: 'Attend',
        label: 'Attend'
      }, {
        attend: 'Won\'t attend',
        label: 'Won\'t attend'
      }, {
        attend: 'Maybe',
        label: 'Maybe'
      }, {
        attend: 'Block',
        label: 'Block'
      }
      ],
      attend: '',
      mapCenter: {lat: 41.017822, lng: 28.954770},
      zoom: 11,
      radio4: 'Attend',
      rate: null,
      eventDetails: null,
      date: null,
      following: null,
      event_id: null,
      follow_event_id: null,
      is_owner: false,
      comment: null
    }
  },
  created() {
    this.getUser()
    this.event_id = this.$route.params.id
    this.additionalBody.event = this.event_id
    this.fetchData(this.event_id)
  },
  methods: {
    fetchData(event_id) {
      let attends
      attends = {
        'Y': 'Attend',
        'N': "Won't attend",
        'M': 'Maybe',
        'B': 'Block'
      }
      getEventDetail(event_id).then(response => {
        this.eventDetails = response.data
        if (response.data.own_follow_status != null) {
          this.follow_event_id = response.data.own_follow_status.id
        }
        if (response.data.own_attendance_status != null) {
          this.attend = attends[response.data.own_attendance_status.status]
        }
        if (response.data.own_follow_status == null) {
          this.following = 'follow'
        } else {
          this.following = 'unfollow'
        }

        this.is_owner = (this.eventDetails.owner.id === this.$store.state.user.user_id) ? true : false
      })
    },
    followEvent() {
      if (this.following == 'follow') {
        follow(parseInt(this.event_id)).then(response => {
          this.following = 'unfollow'
          this.follow_event_id = response.data.id
        })
      } else {
        unfollow(this.follow_event_id).then(response => {
          this.following = 'follow'
          this.follow_event_id = null
        })
      }
    },
    attendanceEvent() {
      let attends
      attends = {
        'Y': 'Attend',
        'N': "Won't attend",
        'M': 'Maybe',
        'B': 'Block'
      }
      attendance(this.event_id, this.attend).then(response => {
        this.attend = attends[response.data.status]
      })
    },

    rateUpEvent() {
      rate(this.event_id, 'U').then(response => {
        if(response) {
          this.$message({
            message: 'You upvoted event succesfully.',
            type: 'success'
          })
          getEventDetail(this.event_id).then(response => {
            this.eventDetails.vote_count = response.data.vote_count
          })
        }
        else {
          this.$message({
            message: 'Please vote again!',
            type: 'error'
          })
        }
      })
    },
    rateDownEvent() {
      rate(this.event_id, 'D').then(response => {
        if(response) {
          this.$message({
            message: 'You downvoted event succesfully.',
            type: 'success'
          })
          getEventDetail(this.event_id).then(response => {
            this.eventDetails.vote_count = response.data.vote_count
          })
        }
        else {
          this.$message({
            message: 'Please vote again!',
            type: 'error'
          })
        }
      })
    },
    addComment() {
      createComment(this.event_id, this.comment).then(response => {
        if(response) {
          this.$message({
            message: 'You created comment succesfully.',
            type: 'success'
          })
          getEventDetail(this.event_id).then(response => {
              this.eventDetails.comments = response.data.comments
          })
          this.comment = ''
        } else {
          this.$message({
            message: 'Please comment again!',
            type: 'error'
          })
        }
      })
    },
    deleteComment(comment_id) {
      delComment(comment_id).then(response => {
        if(response) {
          this.$message({
            message: 'You deleted event succesfully.',
            type: 'success'
          })
          getEventDetail(this.event_id).then(response => {
              this.eventDetails.comments = response.data.comments
          })
          this.comment = ''
        } else {
          this.$message({
            message: 'Please delete comment again!',
            type: 'error'
          })
        }
      })
    },
    beautifyDate(date) {
      var d = new Date(date)
      date = (d.getDate()<10?'0':'') + d.getDate() + "/" + (d.getMonth()<10?'0':'') + d.getMonth() + "/" + d.getFullYear() + " - " + (d.getHours()<10?'0':'')+  d.getHours() + ":" + (d.getMinutes()<10?'0':'') + d.getMinutes()
      return date
    },
    deleteEvent() {
      delEvent(this.event_id).then(response => {
        if(response) {
          this.$message({
            message: 'Event deleted succesfully.',
            type: 'success'
          })
          this.$router.push({ path: this.redirect || '/events/recommended/' })
        }
        else {
          this.$message({
            message: 'Please delete again!',
            type: 'error'
          })
        }
      })
    }
    showSuccess(response, file, fileList){
      this.$alert('Picture is added to the event', 'Congrats!', {
          confirmButtonText: 'I love Cultidate',
        });
    },
  }
}
</script>

<style  scoped>
  .components-container {
    position: relative;
    height: 100vh;
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #1872f0;
  }
  .bg-purple {
    background: #376497;
  }
  .bg-purple-light {
    background: #f4f4f5;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 350px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
  .el-tag + .el-tag {
    margin-left: 10px;
  }
  .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 150px;
    margin: 0;
  }
  .el-carousel{
    max-width: 50%;
  }
  .imgs {
  position: absolute;
  top: 0;
  left: 0;
  min-width: 100%;
  height: 350px;
  max-width: none;
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
    width: 580px;
    max-height: 450px;
  }

</style>
