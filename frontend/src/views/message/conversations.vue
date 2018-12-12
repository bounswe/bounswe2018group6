<template>
  <div class="components-container">
    <el-row :gutter="24" style="margin-top: 25px;">     
      <el-col :span="24">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span style="font-weight:bold;">Conversations</span>
            <el-popover placement="left" width="400" trigger="click">
              <el-input autosize placeholder="Please write user id..." v-model="receiver_id"></el-input>
              <el-button style="float: left; margin-top: 5px;" type="primary" @click.native.prevent="createConversations">Submit</el-button>
              <el-button style="float: right;" type="primary" slot="reference">Create Conversation</el-button>
            </el-popover>
            
          </div>
          <div v-for="conversation in conversations" :key="conversation.id" class="text item">
            <router-link :to="'/message/' + conversation.id"><img :src="conversation.participant.profile_photo" class="user-avatar"></router-link>
            <div>
              <span style="font-weight: bold; font-size: 20px; text-transform: uppercase;">
              <router-link :to="'/message/' + conversation.id"><span>{{ conversation.participant.first_name + " " + conversation.participant.last_name }}</span></router-link> 
              </span>
            </div>
            <span style="font-size: 18px;"> <router-link :to="'/message/' + conversation.id">{{ conversation.participant.username }}</router-link></span>
            <span style="float: right; font-size: 18px;"><span style="font-weight: bold;">Last message:</span>{{ beautifyDate(conversation.updated) }}</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script>

import { getAllConversations, createConversation, getConversationDetails } from '@/api/message'
import { getUserInfo } from '@/api/user'
import { getToken } from '@/utils/auth' // getToken from cookie
import Mallki from '@/components/TextHoverEffect/Mallki'

export default {
  name: 'Conversations',
  components: { Mallki },
  data() {
    return {
      conversations: null,
      receiver_id: null
    }
  },
  created() {
    this.getConversations()
  },
  methods: {
    createConversations() {
      createConversation(parseFloat(this.receiver_id)).then(response => {
        this.receiver_id = null
        getAllConversations().then(response => {
          this.conversations = response.data
        })
      }) 
    },
    getConversations() {
      getAllConversations().then(response => {
          this.conversations = response.data
      })
    },
    beautifyDate(date) {
      var d = new Date(date)
      date = (d.getDate()<10?'0':'') + d.getDate() + "/" + (d.getMonth()<10?'0':'') + d.getMonth() + "/" + d.getFullYear() + " - " + (d.getHours()<10?'0':'')+  d.getHours() + ":" + (d.getMinutes()<10?'0':'') + d.getMinutes()
      return date
    }
  }
}
</script>

<style scoped>
  .components-container {
    position: relative;
    height: 100vh;
  }
  .el-col {
    border-radius: 4px;
  }
  .el-tag + .el-tag {
    margin-left: 10px;
  }
  .text {
    font-size: 14px;
  }
  .item {
    margin-bottom: 18px;
  }
  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }
  .box-card {
    margin-left: 330px;
    margin-right: 330px;
    height: 80vh;
  }
  .user-avatar {
    width: 80px;
    height: 80px;
    border-radius: 30px;
  }
</style>
