<template>
  <el-card class="box-card-component" style="margin-left:8px;">
    <div slot="header" class="box-card-header">
      <img src="https://wpimg.wallstcn.com/e7d23d71-cf19-4b90-a1cc-f56af8c0903d.png">
    </div>
    <div style="position:relative;">
      <mallki class-name="mallki-text" :text="eventName"/>
      <div style="padding-top:35px;">
        <span>{{description}}</span>
      </div>
      <div style="padding-top:20px;">
        <span>Date: {{date}}</span>
      </div>
      <div style="padding-top:20px;">
        <span>Owner: {{owner}}</span>
      </div>
      <div style="padding-top:20px;">
        <span>Followers: {{followers}}</span>
      </div>
      <div style="padding-top:20px;">
        <span>Votes: {{votes}}</span>
      </div>
      
    </div>
  </el-card>
</template>

<script>
import { mapGetters } from 'vuex'
import PanThumb from '@/components/PanThumb'
import Mallki from '@/components/TextHoverEffect/Mallki'

export default {
  components: { PanThumb, Mallki },
  props: {
    eventName: {
      type: String,
    },
    description: {
      type: String,
    },
    date: {
      type: Date,
    },
    owner: {
      type: String,
    },
    followers: {
      type: Number,
    },
    votes: {
      type: Number,
    },
  },
  filters: {
    statusFilter(status) {
      const statusMap = {
        success: 'success',
        pending: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'avatar',
      'roles'
    ])
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" >
.box-card-component{
  .el-card__header {
    padding: 0px!important;
  }
}
</style>
<style rel="stylesheet/scss" lang="scss" scoped>
.box-card-component {
  .box-card-header {
    position: relative;
    height: 220px;
    img {
      width: 100%;
      height: 100%;
      transition: all 0.2s linear;
      &:hover {
        transform: scale(1.1, 1.1);
        filter: contrast(130%);
      }
    }
  }
  .mallki-text {
    position: absolute;
    top: 0px;
    left: 0px;
    font-size: 20px;
    font-weight: bold;
    color: black;
  }
  .panThumb {
    z-index: 100;
    height: 70px!important;
    width: 70px!important;
    position: absolute!important;
    top: -45px;
    left: 0px;
    border: 5px solid #ffffff;
    background-color: #fff;
    margin: auto;
    box-shadow: none!important;
    /deep/ .pan-info {
      box-shadow: none!important;
    }
  }
 
  @media only screen and (max-width: 1510px){
    .mallki-text{
      display: none;
    }
  }
}
</style>
