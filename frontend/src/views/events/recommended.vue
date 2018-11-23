<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="8">
      <el-col v-for="event in eventList" v-bind:key="event.id" :xs="{span: 24}" :sm="{span: 12}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}" style="margin-bottom:30px;">
          <box-card :event-name="event.title" :event-link="'events/show-event/' + event.id" :description="event.description" :date="event.date"
                    :owner="event.owner.username" :followers="event.followers" :votes="event.votes" 
                    :price="event.price" />
      </el-col>
    </el-row>

  </div>
</template>

<script>
import BoxCard from '@/views/dashboard/admin/components/BoxCard'
import { fetchEvents } from '@/api/event'

export default {
  name: 'DashboardAdmin',
  components: {
    BoxCard,
  },
  data() {
    return {
      eventList: null
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      fetchEvents().then(response => {
        this.eventList = response.data
        console.log(this.eventList)
      })
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
</style>
