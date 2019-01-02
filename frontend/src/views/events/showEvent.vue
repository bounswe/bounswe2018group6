<template>
  <div class="components-container">
    <el-row>
      <el-col :span="14"><div class="grid-content bg-purple-light">
        <center style="font-size: 25px; font-weight:bold;font-family: 'Helvetica', 'Arial', sans-serif; color: #38A1F3;"> {{ eventDetails.title }} </center>
        <el-button class="message-owner" style="float: right; margin-right: 20px; margin-top: 10px;" type="warning" @click.native.prevent="message2owner" icon="el-icon-message">Message {{ eventDetails.owner.username }}</el-button>
        <el-button style="float: right; margin-right: 5px; margin-top: 10px;" icon="el-icon-question" type="primary" @click.prevent.stop="guide">Guide</el-button>
        <p style="font-size: 20px; margin-left: 20px;"><span style="color: #9ab97d; ">by</span> <router-link :to="'/profile/' + eventDetails.owner.id + '/'"><mallki :text="eventDetails.owner.username" class-name="mallki-text"/></router-link></p>
        <el-button class="rate" size="large" style="float: right; margin-right: 20px;" type="success" @click.native.prevent="rateUpEvent" icon="el-icon-arrow-up" circle></el-button>
        <p style="font-size: 20px; margin-left: 20px; font-weight:bold; color: #38A1F3;">Date and Time</p>
        <span style="font-size: 20px; margin-left: 20px;"> {{ beautifyDate(eventDetails.date) }}</span>
        <span style="font-size: 20px; float: right; margin-right: 34px;">{{ eventDetails.vote_count }}</span>
        <div></div>
        <el-button size="large" style="float: right; margin-right: 20px;" type="danger" @click.native.prevent="rateDownEvent" icon="el-icon-arrow-down" circle></el-button>
        <div  style="font-size: 20px; margin-left: 20px; margin-top: 60px;"> <span style="font-weight: bold; color: #38A1F3;">Followers:</span> {{ eventDetails.follower_count }}</div>
        <div style="font-size: 20px; margin-left: 20px; margin-top: 70px;"> <span><span style="font-weight: bold; color: #38A1F3;">Price:</span> {{ eventDetails.price }} ₺ </span>
          <el-select class="attendance" v-model="attend" clearable placeholder="Tell Us Your Status" style="margin-right: 20px; float: right;" @change="attendanceEvent">
            <el-option v-for="item in options" :key="item.attend" :label="item.label" :value="item.attend"/>
          </el-select>
        </div>
      </div>
      </el-col>
      <el-carousel ref="imcarousel" trigger="click" height="350px" :autoplay="is_loop" :loop="is_loop">
        <el-carousel-item>
          <img :src="eventDetails.featured_image" class="imgs">
        </el-carousel-item>
        <el-carousel-item v-for="media in eventDetails.medias" :key="media.id">
          <img :src="media.file" class="imgs">
        </el-carousel-item>
      </el-carousel>
    </el-row>

<el-row :gutter="32">
  <div style="margin-top: 15px;">
    <el-tag style="margin-left: 15px;" v-for="tag in eventDetails.tags" :key="tag" size="medium">
      {{ tag.name }}
    </el-tag>
    <el-button style="float: right; margin-right: 15px" type="primary" plain size="small" @click.native.prevent="followEvent">{{ following }}</el-button>
    <el-button size="small" style="float: right; margin-right: 10px;" type="success" @click="shareEvent">{{ is_share }}</el-button>
    <router-link v-if="is_owner" :to="'/events/edit-event/' + event_id">
      <el-button type="primary" plain size="small" style="float: right;">Edit Event</el-button>
    </router-link>
    <el-button v-if="is_owner" size="small" style="float: right; margin-right: 10px;" type="danger" @click="deleteEvent">Delete Event</el-button>
    <el-popover
      placement="bottom"
      title="Annotation"
      width="400"
      trigger="click"
      :content="annot_info">
      <el-button slot="reference" size="small" style="float: right; margin-right: 10px;" @click="stopCarousel">Show Annotations</el-button>
    </el-popover>
    <router-link :to="'/events/annotate-event/' + event_id">
      <el-button type="primary" plain size="small" style="float: right;">Create Annotation</el-button>
    </router-link>
  </div>
</el-row>

<el-row :gutter="10" style="margin-top: 25px;">     
  <el-col :span="14">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span style="font-weight:bold;">Description</span>
      </div>
      <div class="text item">
        {{ eventDetails.description }}
      </div>
    </el-card>
  </el-col>  
   
  <el-col :span="10">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span style="font-weight:bold;">Comments</span>
        <el-popover placement="left" width="400" trigger="click">
          <el-input type="textarea" autosize placeholder="Please comment..." v-model="comment"></el-input>
          <el-button style="float: left; margin-top: 5px;" type="primary" @click.native.prevent="addComment">Submit</el-button>
          <el-button class="add-comment" style="float: right; padding: 3px 0" type="text" slot="reference">Add Comment</el-button>
        </el-popover>
      </div>
      <div v-for="com in eventDetails.comments" :key="com.content" class="text item">
        <span v-if="com.owner.username != $store.state.user.username" style="font-weight: bold; margin-left: 5px"><router-link :to="'/profile/' + eventDetails.owner.id + '/'">{{com.owner.username + ": " }}</router-link></span>
        <span v-else style="font-weight: bold; margin-left: 5px">{{com.owner.username + ": " }}</span>
        <span> {{ com.content }} </span>
        <el-button v-if="com.owner.username === $store.state.user.username" size="mini" style="float: right;" type="danger" icon="el-icon-delete" circle @click.native.prevent="deleteComment(com.id)"></el-button>
        <span style="font-weight: bold; margin-right: 15px; float: right; color: #77450d;"> {{ beautifyDate(com.created)}} </span>
      </div>
    </el-card>
  </el-col>
</el-row>

<el-row :gutter="32" style="margin-top: 25px;">
  <el-col :xs="24" :sm="24" :md="24" :lg="24">
    <div>
      <GmapMap 
      style="height: 350px; max-width: %50;" 
      :zoom="11" 
      :center="{ lat: eventDetails.location.lat,lng: eventDetails.location.lng }">
        <GmapMarker 
        :position="{ lat: eventDetails.location.lat, lng: eventDetails.location.lng }" 
        :title="eventDetails.location.name"
        :label="eventDetails.location.name"/>
      </GmapMap>
    </div>
  </el-col>
</el-row>

</div>
</template>

<script>

import { getEventDetail, follow, unfollow, attendance, delAttendance, rate, delEvent, createComment, delComment, share, unshare } from '@/api/event'
import { createConversation } from '@/api/message'
import { getToken } from '@/utils/auth' // getToken from cookie
import Mallki from '@/components/TextHoverEffect/Mallki'
import * as Driver from 'driver.js' // import driver.js
import 'driver.js/dist/driver.min.css' // import driver.js css
import steps from './defineSteps'

export default {
  name: 'ShowEvent',
  components: {Mallki},
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
      radio4: 'Attend',
      rate: null,
      eventDetails: null,
      date: null,
      following: null,
      event_id: null,
      follow_event_id: null,
      is_owner: false,
      comment: null,
      attend_id: null,
      owner_conversation_id: null,
      is_share: null,
      share_event_id: null,
      driver: null,
      is_loop: true,
      annot_info: '',
    }
  },
  created() {
    this.event_id = this.$route.params.id
    this.additionalBody.event = this.event_id
    this.fetchData(this.event_id)
  },
  mounted() {
    this.driver = new Driver()
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
        if (response.data.own_attendance_status != null) {
          this.attend = attends[response.data.own_attendance_status.status]
        }
        if (response.data.own_follow_status == null) {
          this.following = 'follow'
        } else {
          this.following = 'unfollow'
          this.follow_event_id = response.data.own_follow_status.id
        }
        if (response.data.own_share_status == null) {
          this.is_share = 'share'
        } else {
          this.is_share = 'unshare'
          this.share_event_id = response.data.own_share_status.id
        }
        this.eventDetails.location.lat = parseFloat(this.eventDetails.location.lat)
        this.eventDetails.location.lng = parseFloat(this.eventDetails.location.lng)
        this.is_owner = (this.eventDetails.owner.id == this.$store.state.user.user_id) ? true : false
        for(var i = 0; i < this.eventDetails.attendance_status.length; i++) {
          if(this.eventDetails.attendance_status[i].owner.username == this.$store.state.user.username) {
            this.attend_id = this.eventDetails.attendance_status[i].id
          }
        }
        const last_annotation = this.eventDetails.annotations[this.eventDetails.annotations.length -1]
        this.annot_info = "Owner: " + last_annotation.owner.username + "\n" + 
                          "Motivation: " + last_annotation.data.motivation + "\n" + 
                          "Text: " + last_annotation.data.body + "\n"
        })
    },
    followEvent() {
      if (this.following == 'follow') {
        follow(parseInt(this.event_id)).then(response => {
          this.following = 'unfollow'
          this.follow_event_id = response.data.id
          getEventDetail(this.event_id).then(response => {
            this.eventDetails.follower_count = response.data.follower_count
          })
        })
      } else {
        unfollow(this.follow_event_id).then(response => {
          this.following = 'follow'
          this.follow_event_id = null
          getEventDetail(this.event_id).then(response => {
            this.eventDetails.follower_count = response.data.follower_count
          })
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
      if (this.attend == '') {
        delAttendance(this.attend_id).then(response => {
          this.attend = null
          this.attend_id = null
        })
      } else {
          attendance(this.event_id, this.attend).then(response => {
          this.attend = attends[response.data.status]
          this.attend_id = response.data.id
        })
      }
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
      date = (d.getDate()<10?'0':'') + d.getDate() + "/" + ((d.getMonth() + 1)<10?'0':'') + (d.getMonth() + 1) + "/" +
               d.getFullYear() + " - " + (d.getHours()<10?'0':'')+  d.getHours() + ":" + (d.getMinutes()<10?'0':'') + d.getMinutes()
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
    },
    showSuccess(response, file, fileList){
      this.$alert('Picture is added to the event', 'Congrats!', {
          confirmButtonText: 'I love Cultidate',
        });
    },
    message2owner() {
      createConversation(parseFloat(this.eventDetails.owner.id)).then(response => {
        this.owner_conversation_id = response.data.id
        this.$router.push('/message/' + this.owner_conversation_id)
      })
    },
    shareEvent() {
      if (this.is_share == 'share') {
        share(parseInt(this.event_id)).then(response => {
          this.is_share = 'unshare'
          this.share_event_id = response.data.id
        })
      } else {
        unshare(this.share_event_id).then(response => {
          this.is_share = 'share'
          this.share_event_id = null
        })
      }
    },
    guide() {
      this.driver.defineSteps(steps)
      this.driver.start()
    },
    stopCarousel(){
      this.$refs.imcarousel.setActiveItem(0)
      this.is_loop = false
    }
  }
}
</script>

<style scoped>
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
    min-height: 250px;
  }

  .mallki-text {
    top: 4px;
    left: 3px;
    font-size: 20px;
    font-weight: bold;
    color: black;
  }
</style>
