<template>
  <div class="dashboard-editor-container">
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
          :image="event.featured_image" 
          :owner-id="event.owner.id" 
          :city="event.location.city"
          :district="event.location.district"
          />
      </el-col>
    </el-row>

  </div>
</template>

<script>
import BoxCard from '@/views/dashboard/admin/components/BoxCard'
import { fetchRecommendations } from '@/api/event'

export default {
  name: 'Recommendations',
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
  },
  methods: {
    fetchData() {
      fetchRecommendations().then(response => {
        this.eventList = response.data
      })
    },
    beautifyDate(date) {
      var d = new Date(date)
      date = (d.getDate()<10?'0':'') + d.getDate() + "/" + d.getMonth() + "/" + d.getFullYear() + " - " + (d.getHours()<10?'0':'')+  d.getHours() + ":" + (d.getMinutes()<10?'0':'') + d.getMinutes()
      return date
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
