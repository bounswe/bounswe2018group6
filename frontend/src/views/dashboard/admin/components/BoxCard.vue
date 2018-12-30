<template>
  <el-card class="box-card-component" style="margin-left:8px;">
    <div slot="header" class="box-card-header">
      <router-link :to="'/' + eventLink">
        <img :src="image">
      </router-link>
    </div>
    <div style="position:relative;">
      <router-link :to="'/' + eventLink">
        <mallki :text="eventName" class-name="mallki-text" />
      </router-link>
      <div style="padding-top:35px;">
        <span><read-more more-str="Read more" less-str="Read less" :text="description" :max-chars="60" link="#"></read-more></span>
        

      </div>
      <div style="padding-top:20px;">
        <span>Date: {{ date }}</span>
      </div>
      <div style="padding-top:20px;">
        <span>Price: {{ price }}</span>
      </div>
      <div style="padding-top:20px;">
        <router-link :to="'/profile/' + ownerId">
          <span>Owner: {{ owner }}</span>
        </router-link>
      </div>
      <div style="padding-top:20px;">
        <span>Followers: {{ followers }}</span>
      </div>
      <div style="padding-top:20px;">
        <span>City: {{ city }}</span>
      </div>
      <div style="padding-top:20px;">
        <span>District: {{ district }}</span>
      </div>
      <div style="padding-top:20px;">
        <span>Votes: {{ votes }}</span>
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
  filters: {
    statusFilter(status) {
      const statusMap = {
        success: 'success',
        pending: 'danger'
      }
      return statusMap[status]
    }
  },
  props: {
    eventName: {
      type: String
    },
    eventLink: {
      type: String
    },
    description: {
      type: String
    },
    date: {
      type: String
    },
    price: {
      type: String
    },
    owner: {
      type: String
    },
    followers: {
      type: Number
    },
    votes: {
      type: Number
    },
    image: {
      type: String
    },
    ownerId: {
      type: Number
    },
    city: {
      type: String
    },
    district: {
      type: String
    },
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
   height: 650px;
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
}
</style>
