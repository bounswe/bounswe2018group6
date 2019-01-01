<template>
  <div class="social-signup-container">
    <div>
      <!-- <span class="wx-svg-container"><svg-icon icon-class="wechat" class="icon"/></span> 微信 -->
      <fb-signin-button
        :params="fbSignInParams"
        @success="onSignInSuccess"
        @error="onSignInError">
        Sign in with Facebook
      </fb-signin-button>
    </div>
    <!-- <div class="sign-btn" @click="tencentHandleClick('tencent')">
      <span class="qq-svg-container"><svg-icon icon-class="qq" class="icon"/></span> QQ
    </div> -->
  </div>
</template>

<script>
// import openWindow from '@/utils/openWindow'

export default {
  name: 'SocialSignin',
  data () {
    return {
      fbSignInParams: {
        scope: 'email',
        return_scopes: true
      }
    }
  },
  methods: {
    wechatHandleClick(thirdpart) {
      alert('ok')
      // this.$store.commit('SET_AUTH_TYPE', thirdpart)
      // const appid = 'xxxxx'
      // const redirect_uri = encodeURIComponent('xxx/redirect?redirect=' + window.location.origin + '/auth-redirect')
      // const url = 'https://open.weixin.qq.com/connect/qrconnect?appid=' + appid + '&redirect_uri=' + redirect_uri + '&response_type=code&scope=snsapi_login#wechat_redirect'
      // openWindow(url, thirdpart, 540, 540)
    },
    tencentHandleClick(thirdpart) {
      alert('ok')
      // this.$store.commit('SET_AUTH_TYPE', thirdpart)
      // const client_id = 'xxxxx'
      // const redirect_uri = encodeURIComponent('xxx/redirect?redirect=' + window.location.origin + '/auth-redirect')
      // const url = 'https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=' + client_id + '&redirect_uri=' + redirect_uri
      // openWindow(url, thirdpart, 540, 540)
    },
    onSignInSuccess (response) {
      FB.api('/me', dude => {
        console.log(`Good to see you, ${dude.name}.`)
        console.log(dude)
      })
    },
    onSignInError (error) {
      console.log('OH NOES', error)
      console.log(error)
    }
    
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .social-signup-container {
    margin: 20px 0;
    .sign-btn {
      display: inline-block;
      cursor: pointer;
    }
    .icon {
      color: #fff;
      font-size: 24px;
      margin-top: 8px;
    }
    .wx-svg-container,
    .qq-svg-container {
      display: inline-block;
      width: 40px;
      height: 40px;
      line-height: 40px;
      text-align: center;
      padding-top: 1px;
      border-radius: 4px;
      margin-bottom: 20px;
      margin-right: 5px;
    }
    .wx-svg-container {
      background-color: #8ada53;
    }
    .qq-svg-container {
      background-color: #6BA2D6;
      margin-left: 50px;
    }
  }
  .fb-signin-button {
  /* This is where you control how the button looks. Be creative! */
  display: inline-block;
  padding: 4px 8px;
  border-radius: 3px;
  background-color: #4267b2;
  color: #fff;
}
</style>
