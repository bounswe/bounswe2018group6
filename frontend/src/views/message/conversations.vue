<template>
  <div class="components-container">
    <el-row :gutter="24" style="margin-top: 25px;">     
      <el-col :span="24">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span style="font-weight:bold;">Conversations</span>
            <el-popover placement="left" width="400" trigger="click">
              <el-input autosize placeholder="Please write username..." v-model="receiver_username"></el-input>
              <el-button style="float: left; margin-top: 5px;" type="primary" @click.native.prevent="createConversations">Submit</el-button>
              <el-button style="float: right;" type="primary" slot="reference">Create Conversation</el-button>
            </el-popover>
            
          </div>
          <div v-for="conversation in conversations" :key="conversation.id" class="text item">
            <router-link :to="'/message/' + conversation.id"><img :src="decideOwner(conversation, 'profile_photo')" class="user-avatar"></router-link>
            <div>
              <span style="font-weight: bold; font-size: 20px; text-transform: uppercase;">
              <router-link :to="'/message/' + conversation.id"><span>{{ decideOwner(conversation, 'first_name') + " " + decideOwner(conversation, 'last_name') }}</span></router-link> 
              <el-button style="float: right; margin-top: -15px;" type="danger" icon="el-icon-delete" @click="deleteConversation(conversation.id)">Delete</el-button>
              </span>
            </div>
            <span style="font-size: 18px;"> <router-link :to="'/message/' + conversation.id">{{ decideOwner(conversation, 'username') }}</router-link></span>
            <span style="float: right; font-size: 18px;"><span style="font-weight: bold;">Last message:</span>{{ beautifyDate(conversation.updated) }}</span>
            <hr class="hr">
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script>

import { getAllConversations, createConversation, getConversationDetails, deleteConversations } from '@/api/message'
import { getUserInfo, userSearch } from '@/api/user'
import { getToken } from '@/utils/auth' // getToken from cookie
import Mallki from '@/components/TextHoverEffect/Mallki'

export default {
  name: 'Conversations',
  components: { Mallki },
  data() {
    return {
      conversations: null,
      receiver_id: null,
      receiver_username: ''
    }
  },
  created() {
    this.getConversations()
  },
  methods: {
    createConversations() {
      userSearch(this.receiver_username).then(response => {
        console.log(response.data[0].id)
        this.receiver_id = response.data[0].id
        createConversation(parseFloat(this.receiver_id)).then(response => {
          this.receiver_id = null
          this.receiver_username = ''
          getAllConversations().then(response => {
            this.conversations = response.data
          })
        })
      })
    },
    getConversations() {
      getAllConversations().then(response => {
          this.conversations = response.data
      })
    },
    decideOwner(conversation, attr) {
      if(conversation.owner.username == this.$store.state.user.username) {
        return conversation.participant[attr];
      } else {
        return conversation.owner[attr];
      }
    },
    deleteConversation(conversation_id) {
      deleteConversations(parseFloat(conversation_id)).then(response => {
        getAllConversations().then(response => {
          this.conversations = response.data
        })
      })
    },
    beautifyDate(date) {
      var d = new Date(date)
      date = (d.getDate()<10?'0':'') + d.getDate() + "/" + ((d.getMonth() + 1)<10?'0':'') + (d.getMonth() + 1) + "/" + d.getFullYear() + " - " + (d.getHours()<10?'0':'')+  d.getHours() + ":" + (d.getMinutes()<10?'0':'') + d.getMinutes()
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
    min-height: 80vh;
  }
  .user-avatar {
    width: 80px;
    height: 80px;
    border-radius: 30px;
  }
  .hr {
    border-color: rgb(228, 228, 228);
  }
</style>
