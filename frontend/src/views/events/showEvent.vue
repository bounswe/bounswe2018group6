<template>
  <div class="components-container">
    <el-row>
      <el-col :span="14"><div class="grid-content bg-purple-light">
        <center style="font-size: 25px; font-weight:bold"> {{ eventDetails.title }} </center>
        <p style="font-size: 20px; margin-left: 20px;">by {{ eventDetails.owner.username }} </p>
        <p style="font-size: 20px; margin-left: 20px; font-weight:bold;">Date and Time</p>
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
          <img :src="eventDetails.featured_image" style="object-fit: contain;">
        </el-carousel-item>
        <el-carousel-item v-for="media in eventDetails.medias" :key="media.id">
          <img :src="media.file" style="object-fit: contain;">
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
      <el-tag v-for="tag in tags" :key="tag" size="medium">
        {{ tag }}
      </el-tag>
      <el-button style="float: right;" type="primary" plain size="medium" @click.native.prevent="followEvent">{{ following }}</el-button>
      <router-link v-if="is_owner" :to="'/events/edit-event/' + event_id">
        <el-button >Edit Event</el-button>
      </router-link>
    <el-rate v-model="rate" :colors="['#99A9BF', '#F7BA2A', '#FF9900']"/>
    </div>
  </el-col>
</el-row>
  <el-row :gutter="32">
    <el-col :xs="24" :sm="24" :md="24" :lg="24">
    <div>
      <googlemaps-map
        ref="map"
        :center.sync="mapCenter"
        :zoom.sync="zoom"
        style="height: 350px; max-width: %50;"
        class="map">
        <googlemaps-marker
          :position="{ lat: 41.017822, lng: 28.954770 }"
          title="Baran Et Mangal"
          label="Baran Et Mangal" />
      </googlemaps-map>
    </div>
    </el-col>
  </el-row>
  </div>
</template>

<script>
import { getEventDetail, follow, unfollow, attendance } from '@/api/event'
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
      tags: ['food', 'culture', 'kebap'],
      eventDetails: null,
      following: null,
      event_id: null,
      follow_event_id: null,
      is_owner: false,
    }
  },
  created() {
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
</style>
