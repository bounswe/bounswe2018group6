<template>
  <div class="components-container">
    <el-row :gutter="24" style="margin-top: 25px;">     
      <el-col :span="24">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span><img :src="conversation.participant.profile_photo" class="user-avatar"></span>
            <span style="font-weight:bold; font-size: 20px; text-transform: uppercase; margin-left: 10px;">{{ conversation.participant.first_name + " " + conversation.participant.last_name }}</span>
          </div>
          <div v-for="message in conversation.messages" :key="message.id" class="text item">
            <div style="font-weight:bold; text-transform: uppercase;">{{message.owner.first_name + " " + message.owner.last_name }}</div> 
            <span>{{ message.content }}</span>
            <span style="float: right;">{{ beautifyDate(message.created) }}</span>
          </div>
        </el-card>
        <el-footer style="margin-right: 110px; margin-left: 110px;">
          <el-input placeholder="Please write message..." v-model="current_message" class="input-with-select">
            <el-button slot="append" icon="el-icon-check" @click.native.prevent="createMessages"></el-button>
          </el-input>
        </el-footer>
      </el-col>
    </el-row>
  </div>
</template>
<script>

import { getAllConversations, createConversation, getConversationDetails, createMessage } from '@/api/message'
import { getUserInfo } from '@/api/user'
import { getToken } from '@/utils/auth' // getToken from cookie
import Mallki from '@/components/TextHoverEffect/Mallki'

export default {
  name: 'Messaging',
  components: { Mallki },
  data() {
    return {
      current_message: '',
      conversation: null,
      interval: null
    }
  },
  created() {
    this.getConversationDetail()
    this.interval = setInterval(() => {
      this.getConversationDetail()
    }, 3000)
  },
  beforeDestroy() {
    clearInterval(this.interval)    
  },
  methods: {
    getConversationDetail() {
      getConversationDetails(this.$route.params.id).then(response => {
          this.conversation = response.data
      })
    },
    createMessages() {
      createMessage(this.conversation.participant.id, this.conversation.id, this.current_message).then( response => {
        getConversationDetails(this.$route.params.id).then(response => {
          this.conversation = response.data
          this.current_message = ''
        })
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
    height: 80vh;
    margin-left: 130px;
    margin-right: 130px;
  }
  .user-avatar {
    width: 45px;
    height: 45px;
    border-radius: 30px;
    float: left;
  }
</style>
