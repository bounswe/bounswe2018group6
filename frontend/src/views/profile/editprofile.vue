<template>
  <div class="tab-container">
    <div style="margin-left: 44.5%; margin-top: 10px;">
    <pan-thumb :image="profile_photo" class="center-item"/>
      <profile-upload
        class="avatar-uploader"
        :action="apiAddress"
        :headers="headers"
        :name="field"
        :on-success="refresh"
        > 
        <el-button size="small" type="primary">Change Profile Photo</el-button>
      </profile-upload>
    </div>
    <div style="margin-bottom: 35px; left: 50%;"/>
    <el-form :label-position="labelPosition"  :model="form" label-width="120px">
      <el-form-item label="First Name">
        <el-input v-model="form.first_name" :placeholder="form.first_name"/>
      </el-form-item>
      <el-form-item label="Last Name">
        <el-input v-model="form.last_name" :placeholder="form.last_name"/>
      </el-form-item>
      <el-form-item label="Bio">
        <el-input v-model="form.bio" :placeholder="form.bio"/>
      </el-form-item>
      <el-form-item label="City">
        <el-input v-model="form.city" :placeholder="form.city"/>
      </el-form-item>
      <el-form-item label="Old Password" prop="password">
        <el-input :type="passwordType"  v-model="form.current_password" auto-complete="off"/>
      </el-form-item>
      <el-form-item label="New Password" prop="password">
        <el-input :type="passwordType" v-model="form.new_password" auto-complete="off"/>
      </el-form-item>
      <el-form-item label="Tags">
        <el-checkbox-group v-model="form.tags">
          <el-checkbox-button v-for="tag in tag_list" :label="tag.id" :key="tag.name">{{tag.name}}</el-checkbox-button>
        </el-checkbox-group>
      </el-form-item>
      <el-form-item label="User type">
        <el-radio-group v-model="form.is_corporate_user">
          <el-radio :label="true">Corporate</el-radio>
          <el-radio :label="false">Not Corporate</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item v-if="form.is_corporate_user" label="Link">
        <!-- <el-input v-model="form.corporate_profile.url" :placeholder="form.corporate_profile.url"/> -->
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Update</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import ImageCropper from '@/components/ImageCropper'
import PanThumb from '@/components/PanThumb'
import { getUserInfo, editUser } from '@/api/user'
import { getTags } from '@/api/event'
import { getToken } from '@/utils/auth' // getToken from cookie
import Vue from 'vue'

export default {
  name: 'Editprofile',
  components: { ImageCropper, PanThumb },
  data() {
    return {
      labelPosition: 'left',
      passwordType: 'password',
      form: {
        first_name: '',
        last_name: '',
        city: null,
        bio: null,
        tags: [],
        current_password: null,
        new_password: null,
        is_corporate_user: null,
        corporate_profile: {
          url: ''
        }
      },
      tag_list: null,
      user_id: null,
      apiAddress: '',
      field: 'profile_photo',
      headers : {
        Authorization: 'Token ' + getToken()
      },
      profile_photo: '',
    }
  },
  created() {
    this.user_id = this.$store.state.user.user_id
    this.apiAddress = 'https://cultidate.herokuapp.com/api/user/' + this.user_id + '/'
    this.getUser()
    this.getTagList()
  },
  methods: {
    getUser() {
      getUserInfo(this.user_id).then(response => {
        this.form.first_name = response.data.first_name
        this.form.last_name = response.data.last_name
        this.form.city = response.data.city
        this.form.bio = response.data.bio
        console.log(response)
        this.form.is_corporate_user = response.data.is_corporate_user
        this.form.corporate_profile = response.data.corporate_profile
        this.profile_photo = response.data.profile_photo
        console.log(response.data)
      })
    },
    refresh(){
      getUserInfo(this.user_id).then(response => {
        this.profile_photo = response.data.profile_photo
      })
    },
    /*
    changeImage(profile_photo) {
      editUser(this.$store.state.user.user_id, profile_photo).then(response => {
        if(response){
          this.$message({
            message: 'Avatar changed',
            type: 'success'
          })
        }
        else {
          this.$message({
            message: 'Try again!',
            type: 'error'
          })
        }
      })
    },*/
    getTagList() {
      getTags().then(response => {
        this.tag_list = response.data
      })
    },
    onSubmit() {
      if (this.form.current_password == null || this.form.new_password == null) {
        Vue.delete(this.form, 'current_password')
        Vue.delete(this.form, 'new_password')
      }
      console.log(this.form.tags)
      editUser(this.$store.state.user.user_id, this.form).then(response => {
        if(response){
          this.$message({
            message: 'Changes saved',
            type: 'success'
          })
          this.$router.push({ path: this.redirect || '/my-profile/' })
          }
          else {
            this.$message({
              message: 'Please write your correct password!',
              type: 'error'
            })
          }
      })
    }
   }
}
</script>

<style scoped>
.tab-container{
    margin: 200px;
}

.change-avatar {
  position: absolute;
  top: 35%;
  left: 50%;

  -moz-transform: translateX(-50%) translateY(-50%);
  -webkit-transform: translateX(-50%) translateY(-50%);
  transform: translateX(-50%) translateY(-50%);
}
.center-item{
  position: absolute;
  top: 5%;
  left: 50%;
  transform: translateX(-50%) translateY(-0%);
}
</style>
