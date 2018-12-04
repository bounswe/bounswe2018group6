<template>
  <div class="components-container">
    <pan-thumb :image="image"/>
    <image-cropper
      v-show="imagecropperShow"
      :width="300"
      :height="300"
      :key="imagecropperKey"
      lang-type="en"
      @close="close"
      @crop-upload-success="cropSuccess"/>
    <el-span class="name"> {{ name }} </el-span>
    <el-popover v-if="is_corporate_user" :title="corporate_profile.url" placement="left" width="300" trigger="hover">
      <el-tag v-if="is_corporate_user" slot="reference" size="medium" class="corporate">Corporate </el-tag>
    </el-popover>
    <el-span style="float: right; margin-top: 100px;"><i class="el-icon-location" style="margin-right:5px;"></i>{{city}}</el-span>
    <div></div>
    <div class="features">
      <el-button round>{{ follower_count }} followers</el-button>
      <el-button round style="margin-left: 10px;">{{ following_count }} followings</el-button>
      <el-button round style="margin-left: 10px;">{{ owned_events_count }} events</el-button>
    </div>
    <div class="block">
      <el-span class="bio"><i class="el-icon-info" style="margin-right:5px;"></i>{{bio}}</el-span>
    </div>
    <div class="block">
      <el-tag v-for="tag in tags" :label="tag.name" :key="tag.id" size="medium">
        {{ tag.name }}
      </el-tag>
    </div>
  </div>
</template>

<script>
import ImageCropper from '@/components/ImageCropper'
import PanThumb from '@/components/PanThumb'
import { getUserInfo } from '@/api/user'

export default {
  name: 'Profile',
  components: { ImageCropper, PanThumb },
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
      image: 'https://wpimg.wallstcn.com/577965b9-bb9e-4e02-9f0c-095b41417191',
      inputVisible: false,
      inputValue: ''
    }
  },
  created() {
    this.getUser()
  },
  methods: {
    getUser() {
      getUserInfo(this.$route.params.id).then(response => {
        this.name = response.data.first_name + ' ' + response.data.last_name
        this.follower_count = response.data.follower_count
        this.following_count = response.data.following_count
        this.owned_events_count = response.data.owned_events_count
        this.tags = response.data.tags
        this.city = response.data.city
        this.bio = response.data.bio
        this.is_corporate_user = response.data.is_corporate_user
        this.corporate_profile = response.data.corporate_profile
        
      })
    },
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
  margin-left: 40px;
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
</style>
