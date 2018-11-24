<template>
  <div class="components-container">
    <el-row>
      <el-col :span="14"><div class="grid-content bg-purple-light">
        <center style="font-size: 25px; font-weight:bold"> {{ eventDetails.title }} </center>
        <p style="font-size: 20px; margin-left: 20px;">by {{ eventDetails.owner.username}} </p>
        <p style="font-size: 20px; margin-left: 20px; font-weight:bold;">Date and Time</p>
        <p style="font-size: 20px; margin-left: 20px;">{{ eventDetails.date }}</p>
        <div style="font-size: 20px; margin-left: 20px; margin-top: 130px;"> <span>Price: {{ eventDetails.price }} </span>
          <el-radio-group v-model="radio4" size="small" style="margin-left: 190px; margin-right: 20px;">
            <el-radio-button label="Attend" />
            <el-radio-button label="Maybe"/>
            <el-radio-button label="Won't attend"/>
            <el-radio-button label="Block"/>
          </el-radio-group>
        </div>
      </div>
      </el-col>
      <el-carousel trigger="click" height="350px">
        <el-carousel-item>
          <img style="object-fit: contain;" :src="eventDetails.featured_image">
        </el-carousel-item>
        <el-carousel-item v-for="media in eventDetails.medias" v-bind:key="media.id">
          <img style="object-fit: contain;" :src="media.file">
        </el-carousel-item>
      </el-carousel>
    </el-row>
    <div style="margin-top: 30 px" >
      <p/>
      <el-tag v-for="tag in tags" :key="tag" size="medium">
        {{ tag }}
      </el-tag>
      <el-button style="float: right;" type="primary" plain size="medium">Follow</el-button>
    </div>
    <div style="margin-top: 20px">
      <span style="font-size: 20px; font-weight:bold;">{{ eventDetails.description }}</span>
      <el-rate v-model="rate" :colors="['#99A9BF', '#F7BA2A', '#FF9900']" style="float: right;"/>
    </div>
  
<googlemaps-map
            style="height: 350px; max-width: %100;"
            ref="map"
            class="map"
            :center.sync="mapCenter"
            :zoom.sync="zoom">
    <googlemaps-marker
        title="Baran Et Mangal"
        label="Baran Et Mangal"
				:position="{ lat: 41.017822, lng: 28.954770 }" />
 </googlemaps-map>

  </div>
</template>

<script>
import { getEventDetail } from '@/api/event'



export default {
  name: 'ShowEvent',
  components: {},
  data() {
    return {
      mapCenter: {lat: 41.017822, lng: 28.954770},
      zoom: 11,
      radio4: 'Attend',
      rate: null,
      tags: ['food', 'culture', 'kebap'],
      eventDetails: null,
    }
  },
  created() {
    const event_id = this.$route.params.id
    this.fetchData(event_id)
  },
  methods: {
    fetchData(event_id) {
      getEventDetail(event_id).then(response => {
        this.eventDetails = response.data
        console.log(this.eventDetails)
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
    min-height: 340px;
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
