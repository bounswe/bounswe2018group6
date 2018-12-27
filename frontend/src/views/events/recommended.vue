<template>
  <div class="dashboard-editor-container">
    <el-row style="margin-bottom: 15px;">
      <el-input placeholder="Please search event" v-model="search_word" class="input-with-select">
        <el-select v-model="search_type" slot="prepend" placeholder="Search with">
          <el-option label="Content" value="1"></el-option>
          <el-option label="Location" value="2"></el-option>
        </el-select>
        <el-button slot="append" icon="el-icon-search" @click.native.prevent="searchEvents"></el-button>
      </el-input>
    </el-row>
    <el-row :gutter="8">
      <el-col v-for="event in eventList" :key="event.id" :xs="{span: 24}" :sm="{span: 12}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}" style="margin-bottom:30px;">
        <box-card
          :event-name="event.title"
          :event-link="'events/show-event/' + event.id"
          :description="event.description"
          :date="beautifyDate(event.date)"
          :owner="event.owner.username"
          :followers="event.follower_count"
          :votes="event.vote_count"
          :price="event.price"
          :image="event.featured_image" />
      </el-col>
    </el-row>

  </div>
</template>

<script>
import BoxCard from '@/views/dashboard/admin/components/BoxCard'
import { fetchEvents, getTags, searchByTitle, searchByLocation } from '@/api/event'

export default {
  name: 'DashboardAdmin',
  components: {
    BoxCard
  },
  data() {
    return {
      eventList: null,
      search_type: null,
      search_word: null
    }
  },
  created() {
    this.fetchData()
    this.getTagList()
  },
  methods: {
    fetchData() {
      fetchEvents().then(response => {
        this.eventList = response.data
      })
    },
    beautifyDate(date) {
      var d = new Date(date)
      date = (d.getDate()<10?'0':'') + d.getDate() + "/" + d.getMonth() + "/" + d.getFullYear() + " - " + (d.getHours()<10?'0':'')+  d.getHours() + ":" + (d.getMinutes()<10?'0':'') + d.getMinutes()
      return date
    },
    searchEvents() {
      console.log("search type is " + this.search_type)
      if(this.search_type == 1) {
        searchByTitle(this.search_word).then(response => {
          this.eventList = response.data
        })
      } 
      else if(this.search_type == 2) {
        searchByLocation(this.search_word).then(response => {
          this.eventList = response.data
        })
      }
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
  .input-with-select .el-input-group__prepend {
    background-color: #fff;
  }
  .el-input {
    width: 500px;
  }
  .el-select {
    width: 120px;
  }
</style>
