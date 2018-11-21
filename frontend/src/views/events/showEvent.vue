<template>
  <div class="components-container">
    <el-row>
      <img height="340" width="480" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQcQqPq3suSxF5X_e9OpVQxp-Y8x3eiHmldlcKFHw2SxRfSRmj">
      <el-col :span="14"><div class="grid-content bg-purple-light">
        <center style="font-size: 25px; font-weight:bold"> Turkish Cuisine - Meetup İstanbul </center>
        <p style="font-size: 20px; margin-left: 20px;">by Atif Emre Yuksel</p>
        <p style="font-size: 20px; margin-left: 20px; font-weight:bold;">Date and Time</p>
        <p style="font-size: 20px; margin-left: 20px;">27/12/2018 - 18.00</p>
        <div style="font-size: 20px; margin-left: 20px; margin-top: 130px;"> <span>Price: 19.99 TL</span>
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
      <span style="font-size: 20px; font-weight:bold;">Description</span>
      <el-rate v-model="rate" :colors="['#99A9BF', '#F7BA2A', '#FF9900']" style="float: right;"/>
      <p>
        Join The Telegraph for a Champions Tennis VIP Experience

        Watch the greats of tennis go to battle in the stunning setting of the Royal Albert Hall and enjoy an exclusive Q&A with our very own Simon Briggs as he interviews one of the legends.

        The VIP Experience will be taking place on three days:

        Thursday, December 6, 2018 at 12.15pm

        Friday, December 7, 2018 at 12.15pm

        Sunday, December 9, 2018 at 4pm (Final)
      </p>
    </div>

  </div>
</template>

<script>
export default {
  name: 'SplitpaneDemo',
  components: {},
  data() {
    return {
      radio4: 'Attend',
      rate: null,
      tags: ['food', 'culture', 'kebap']
    }
  },
  methods: {
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
</style>
