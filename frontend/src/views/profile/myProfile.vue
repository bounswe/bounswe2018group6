<template>
  <div class="components-container">
    <pan-thumb :image="profile_photo"/>
    <profile-upload
      class="avatar-uploader"
      :action="apiAddress"
      :headers="headers"
      :name="field"
      :on-success="refresh"
      > 
      <el-button size="small" type="primary" style="margin-top: 10px;">Change Profile Photo</el-button>
    </profile-upload>
    <el-span class="name"> {{ name }} </el-span>
    <el-popover v-if="is_corporate_user" :title="corporate_profile.url" placement="left" width="300" trigger="hover">
      <el-tag v-if="is_corporate_user" slot="reference" size="medium" class="corporate">Corporate </el-tag>
    </el-popover>
    <router-link to="/editprofile"><el-button type="primary" icon="el-icon-edit" class="edit" circle/></router-link>
    <el-span style="float: right; margin-top: -80px;"><i class="el-icon-location" style="margin-right: 5px;"></i>{{city}}</el-span>
    <div></div>
    <div class="features">
      <el-button round @click="dialogFollowerVisible = true">{{ follower_count }} followers</el-button>
      <el-dialog title="Followers" :visible.sync="dialogFollowerVisible">
          <el-table :data="followers" style="width: 100%">
            <el-table-column v-for="v in props" :key="v.prop" :prop="v.prop" :label="v.label"/>
          </el-table>
      </el-dialog>
      <el-button round style="margin-left: 10px;" @click="dialogFollowingVisible = true">{{ following_count }} followings</el-button>
      <el-dialog title="Followings" :visible.sync="dialogFollowingVisible">
        <el-table :data="followings" style="width: 100%">
          <el-table-column v-for="v in props" :key="v.prop" :prop="v.prop" :label="v.label"/>
        </el-table>
      </el-dialog>
      <el-button round style="margin-left: 10px;">{{ owned_events_count }} events</el-button>
    </div>
    <div class="block">
      <el-span class="bio"><i class="el-icon-info" style="margin-right: 5px;"></i>{{bio}}</el-span>
    </div>
    <div class="block">
      <el-tag v-for="tag in tags" :label="tag.name" :key="tag.id" size="medium">
        {{ tag.name }}
      </el-tag>
    </div>
    <div style="margin-top: 20px;">
      <h3 style="margin-left: 8px;">Shared Events</h3>
      <el-row :gutter="8">
        <el-col v-for="event in sharedEvents" :key="event.id" :xs="{span: 24}" :sm="{span: 12}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}" style="margin-bottom:30px;">
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
  </div>
</template>

<script>
import ImageCropper from '@/components/ImageCropper'
import PanThumb from '@/components/PanThumb'
import { getUserInfo } from '@/api/user'
import ProfileUpload from '@/components/Upload'
import { getToken } from '@/utils/auth'
import BoxCard from '@/views/dashboard/admin/components/BoxCard'
import Vue from 'vue'

Vue.component('column', {
	props: ['prop', 'label'],
	template:'<el-table-column :prop="prop" :label="label" min-width="180"></el-table-column>'
})
export default {
  name: 'Profile',
  components: { ImageCropper, PanThumb, ProfileUpload, BoxCard },
  data() {
    return {
      name: '',
      follower_count: 0,
      following_count: 0,
      owned_events_count: 0,
      tags: [],
      city: null,
      bio: null,
      is_corporate_user: null,
      corporate_profile: null,
      imagecropperShow: false,
      imagecropperKey: 0,
      inputVisible: false,
      inputValue: '',
      profile_photo: null,
      user_id: null,
      apiAddress: '',
      field: 'profile_photo',
      headers : {
        Authorization: 'Token ' + getToken()
      },
      followers: null,
      dialogFollowerVisible: false,
      followings: null,
      dialogFollowingVisible: false,
      props: [{
        prop:'username',
        label:'Username'
      },{
        prop:'first_name',
        label:'First name'
      },{
        prop:'last_name',
        label:'Last name'
      }],
      sharedEvents: null
    }
  },
  created() {
    this.user_id = this.$store.state.user.user_id
    this.apiAddress = 'https://cultidate.herokuapp.com/api/user/' + this.user_id + '/'
    this.getUser()
  },
  methods: {
    getUser() {
      getUserInfo(this.user_id).then(response => {
        this.name = response.data.first_name + ' ' + response.data.last_name
        this.follower_count = response.data.follower_count
        this.following_count = response.data.followings.users.length
        this.owned_events_count = response.data.owned_events_count
        this.tags = response.data.tags
        this.city = response.data.city
        this.bio = response.data.bio
        this.is_corporate_user = response.data.is_corporate_user
        this.corporate_profile = response.data.corporate_profile
        this.profile_photo = response.data.profile_photo
        this.followers = response.data.followers.users
        this.followings = response.data.followings.users
        this.sharedEvents = response.data.shared_events
        for(var i = 0; i < this.followers.length; i++) {
          this.followers[i] = this.followers[i].user
        }
        for(var i = 0; i < this.followings.length; i++) {
          this.followings[i] = this.followings[i].user
        }
      })
    },
    refresh(){
      getUserInfo(this.user_id).then(response => {
        this.profile_photo = response.data.profile_photo
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

<style scoped>
.block {
  padding: 15px 20px;
}

.tag-item {
  margin-right: 15px;
}

.avatar{
  width: 200px;
  height: 200px;
  border-radius: 50%;
}

.name{
  position: absolute;
  top: 20px;
  margin-left: 190px;
  font-weight: bold;
  font-size: 25px;
  text-transform: uppercase;
}

.bio{
  position: absolute;
  top: 120px;
  margin-left: 170px;
  font-size: 16px;
  text-transform: uppercase;
}

.features{
  position: absolute;
  top: 70px;
  left: 190px;
}

.edit{
  position: absolute;
  top: 16px;
  right: 0px;
}

.corporate{
  position: absolute;
  top: 60px;
  right: 0px;
}

.el-tag + .el-tag {
  margin-left: 10px;
}

.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}

.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  border-radius: 50%;
}
.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>
