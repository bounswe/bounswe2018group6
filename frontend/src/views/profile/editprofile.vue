<template>
  <div class="tab-container">
    <pan-thumb :image="image" class="center-item"/>
    <image-cropper
      v-show="imagecropperShow"
      :width="300"
      :height="300"
      :key="imagecropperKey"
      lang-type="en"
      @close="close"
      @crop-upload-success="cropSuccess"/>
    <div style="margin-left: 42%; margin-top: 5%;">
      <el-button type="primary" @click="imagecropperShow=true">Change Avatar</el-button>
    </div>
    <div style="margin-bottom: 25px; left: 50%;"/>
    <el-form :label-position="labelPosition" :model="formLabelAlign" label-width="100px">
      <el-form-item label="Name">
        <el-input v-model="formLabelAlign.name" :placeholder="name"/>
      </el-form-item>
      <el-form-item label="Birth date">
        <el-date-picker :placeholder="birth_date" v-model="formLabelAlign.birth_date" type="date" style="width: 100%;"/>
      </el-form-item>
      <el-form-item v-if="is_corporate_user" label="Description">
        <el-input v-model="formLabelAlign.corporate_profile.description" :placeholder="corporate_profile.description"/>
      </el-form-item>
      <el-form-item v-if="is_corporate_user" label="Link">
        <el-input v-model="formLabelAlign.corporate_profile.url" :placeholder="corporate_profile.url"/>
      </el-form-item>
      <el-form-item>
        <el-button type="primary">Update</el-button> <!-- @click="submitForm('ruleForm')" Add handler function for submit-->
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import ImageCropper from '@/components/ImageCropper'
import PanThumb from '@/components/PanThumb'
import { getUserInfo } from '@/api/user'

export default {
  name: 'Editprofile',
  components: { ImageCropper, PanThumb },
  data() {
    return {
      name: '',
      birth_date: null,
      is_corporate_user: null,
      corporate_profile: null,
      labelPosition: 'right',
      formLabelAlign: {
        name: '',
        birth_date: '',
        corporate_profile: {
          description: null,
          url: null
        }
      },
      rules: {
        birth_date: [
          { type: 'date', trigger: 'blur' }
        ]
      },
      imagecropperShow: false,
      imagecropperKey: 0,
      image: 'https://wpimg.wallstcn.com/577965b9-bb9e-4e02-9f0c-095b41417191',
      inputValue: ''
    }
  },
  created() {
    this.getUser()
  },
  methods: {
    cropSuccess(resData) {
      this.imagecropperShow = false
      this.imagecropperKey = this.imagecropperKey + 1
      this.image = resData.files.avatar
    },
    close() {
      this.imagecropperShow = false
    },
    handleClose(tag) {
      this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1)
    },
    getUser() {
      getUserInfo(this.$store.state.user.user_id).then(response => {
        this.name = response.data.first_name + ' ' + response.data.last_name
        this.birth_date = response.data.birth_date
        this.is_corporate_user = response.data.is_corporate_user
        this.corporate_profile = response.data.corporate_profile
      })
    }
  }
}
</script>

<style scoped>
.tab-container{
    margin: 380px;
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
  top: 25%;
  left: 50%;
  transform: translateX(-50%) translateY(-0%);
}
</style>
