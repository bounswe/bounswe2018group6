<template>
  <div class="components-container">
    <el-row>
      <!-- <img height="340" width="480"  position=relative; src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQcQqPq3suSxF5X_e9OpVQxp-Y8x3eiHmldlcKFHw2SxRfSRmj"> -->
      <el-carousel trigger="click" height="350px">
        <el-carousel-item v-for="media in eventDetails.medias" v-bind:key="media">
          <img style="object-fit: contain;" :src="media.url">
        </el-carousel-item>
      </el-carousel>
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

  </div>
</template>

<script>
import { getEventDetail } from '@/api/event'

export default {
  name: 'ShowEvent',
  components: {},
  data() {
    return {
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
