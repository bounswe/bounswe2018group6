<template>
  <div class="components-container">
    <el-row>
      <el-col :span="14"><div class="grid-content bg-purple-light">
        <center style="font-size: 25px; font-weight:bold"> {{ eventDetails.title }} </center>
        <p style="font-size: 20px; margin-left: 20px;">by {{ eventDetails.owner.username }} </p>
        <p style="font-size: 20px; margin-left: 20px; font-weight:bold;">Date and Time</p>
        <p style="font-size: 20px; margin-left: 20px;">{{ eventDetails.date }}</p>
        <div style="font-size: 20px; margin-left: 20px; margin-top: 130px;"> <span>Price: {{ eventDetails.price }} </span>
          <el-select v-model="attend" placeholder="Attendance" style="margin-right: 20px; float: right;" @change="attendanceEvent">
            <el-option v-for="item in options" :key="item.attend" :label="item.label" :value="item.attend"/>
          </el-select>
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
    <div style="margin-top: 30 px" >
      <p/>
      <el-tag v-for="tag in tags" :key="tag" size="medium">
        {{ tag }}
      </el-tag>
      <el-button style="float: right;" type="primary" plain size="medium" @click.native.prevent="followEvent">{{ following }}</el-button>
    </div>
    <div style="margin-top: 20px">
      <span style="font-size: 20px; font-weight:bold;">Description</span>
      <el-rate v-model="rate" :colors="['#99A9BF', '#F7BA2A', '#FF9900']" style="float: right;"/>
      <p>{{ eventDetails.description }} </p>

    </div>

    <googlemaps-map
      ref="map"
      :center.sync="mapCenter"
      :zoom.sync="zoom"
      style="height: 350px; max-width: %100;"
      class="map">
      <googlemaps-marker
        :position="{ lat: 41.017822, lng: 28.954770 }"
        title="Baran Et Mangal"
        label="Baran Et Mangal" />
    </googlemaps-map>

  </div>
</template>

<script>
import { getEventDetail, follow, unfollow, attendance } from '@/api/event'
export default {
  name: 'ShowEvent',
  components: {},
  data() {
    return {
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
      follow_event_id: null
    }
  },
  created() {
    this.event_id = this.$route.params.id
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
      })
    },
    followEvent() {
      if (this.following == 'follow') {
        follow(parseInt(this.event_id)).then(response => {
          this.following = 'unfollow'
          this.follow_event_id = response.data.id
          console.log(this.follow_event_id)
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
    }
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
