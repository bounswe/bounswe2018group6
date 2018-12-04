<template>
  <div class="components-container">
    <el-row>
      <el-col :xs="24" :sm="24" :md="16" :lg="16"> <div class="grid-content bg-purple-light">
        <el-input type="textarea" autosize :placeholder="eventDetails.title" v-model="formData.title"> </el-input>
        <p style="font-size: 20px; margin-left: 20px; font-weight:bold;">Date and Time</p>
        <el-date-picker
          v-model="formData.date"
          type="datetime"
          :placeholder="beautifyDate(eventDetails.date)">
        </el-date-picker>
        <p style="font-size: 20px; margin-left: 20px; font-weight:bold;">Price</p>
        <el-input type="number" style="width: 400px;" :placeholder="eventDetails.price" v-model="formData.price">
            <template slot="append">₺</template>
        </el-input>
      </div>
      </el-col>
      <el-col :xs="24" :sm="24" :md="8" :lg="8">
        <span style="margin-top: 20px;">Click image to change event's featured image</span>
           <profile-upload
            class="avatar-uploader"
            :show-file-list="false"
            :action="featuredMediaApiAddress"
            :headers="headers"
            :name="imageName"
            :on-success="changeImage"
            list-type="picture-card">
            <img v-if="eventDetails.featured_image" :src="eventDetails.featured_image" class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </profile-upload>
          

      </el-col>
    </el-row>

  
    <div  style="margin-top: 20px">
      <span style="font-size: 20px; font-weight:bold;">Description</span>
      <el-card class="box-card" style="margin-top: 10px; margin-right: 100px">
        <el-input type="textarea" autosize :placeholder="eventDetails.description" v-model="formData.description"> </el-input>
      </el-card>
    </div>
  

  
    <div style="margin-top: 30 px" >
      <p/>
        <el-checkbox-group v-model="formData.tags">
          <el-checkbox-button v-for="tag in tag_list" :label="tag.id" :key="tag.name">{{tag.name}}</el-checkbox-button>
        </el-checkbox-group>
    </div>

<div>
    <ul> 
      <li>Upload up to 5 images</li>
      <li>Green tick denotes that upload is succesful</li>
      <li>You can also drag and drop your image</li>
    </ul>
    <h3>Upload additional photos</h3>
    <el-upload
    class="upload-demo"
    drag
    :limit="mediaLimit"
    :action="mediaApiAddress"
    :headers="headers"
    :data="additionalBody"
    :name="keyName"
    :on-success="showSuccess"
    :file-list="mediaList"
    list-type="picture-card">
    <el-button size="small" type="primary">Click to upload</el-button>
    </el-upload>
</div>
<div>
  <el-button size="large" type="primary" style="margin-bottom:50px; margin-top: 50px;" @click.native.prevent="handleSubmit">Change Event with Current Values</el-button>
</div>

<el-row :gutter="32">
      <el-col :xs="24" :sm="24" :md="24" :lg="24">
        <div>
          <googlemaps-map
            ref="map"
            :center.sync="mapCenter"
            :zoom.sync="zoom"
            style="height: 350px; max-width: %50;"
            class="map">
            <googlemaps-marker
              :position="{ lat: 41.017822, lng: 28.954770 }"
              title="Baran Et Mangal"
              label="Baran Et Mangal" />
          </googlemaps-map>
        </div>
      </el-col>
</el-row>
</div>
</template>

<script>
import { getEventDetail, editEvent, getTags } from "@/api/event";
import ProfileUpload from '@/components/Upload'
import { getToken } from "@/utils/auth"; // getToken from cookie

export default {
  name: "EditEvent",
  components: {ProfileUpload},
  data() {
    return {
      formData: { tags: []},
      mediaList: [],
      mediaApiAddress: "https://cultidate.herokuapp.com/api/medias/",
      featuredMediaApiAddress: "",
      imageName: 'featured_image',
      headers: {
        // 'Content-Type': 'multipart/form-data',
        Authorization: "Token " + getToken()
      },
      additionalBody: {
        event: null
      },
      keyName: "file",
      mediaLimit: 30,
      mapCenter: { lat: 41.017822, lng: 28.95477 },
      zoom: 11,
      radio4: "Attend",
      rate: null,
      eventDetails: null,
      event_id: null,
      follow_event_id: null,
      tag_list: []
    };
  },
  created() {
    this.event_id = this.$route.params.id;
    this.featuredMediaApiAddress = "https://cultidate.herokuapp.com/api/events/" + this.event_id + '/'
    this.additionalBody.event = this.event_id;
    this.fetchData(this.event_id);
    this.getTagList()
  },
  methods: {
    fetchData(event_id) {
      let attends;
      attends = {
        Y: "Attend",
        N: "Won't attend",
        M: "Maybe",
        B: "Block"
      };
      getEventDetail(event_id).then(response => {
        this.eventDetails = response.data;
        for (let i = 0; i < this.eventDetails.medias.length; i++){
          this.mediaList.push({ 
            name: this.eventDetails.medias[i].id,
            url: this.eventDetails.medias[i].file
            })
        }
      });
    },
    beautifyDate(date) {
      var d = new Date(date)
      date = (d.getDate()<10?'0':'') + d.getDate() + "/" + d.getMonth() + "/" + d.getFullYear() + " - " + (d.getHours()<10?'0':'')+  d.getHours() + ":" + (d.getMinutes()<10?'0':'') + d.getMinutes()
      return date
    },
    showSuccess(response, file, fileList) {
      this.$alert("Picture is added to the event", "Congrats!", {
        confirmButtonText: "I love Cultidate"
      });
    },
    dontRemove(response, file, fileList) {
      this.$alert("Removing media is not supported yet.", "Error!", {
        confirmButtonText: "I do obey"
      });
    },
    changeImage(response, file, fileList){
      this.eventDetails.featured_image = response.featured_image
      this.$alert("Picture is added to the event", "Congrats!", {
        confirmButtonText: "I love Cultidate"
      });
    },
    getTagList() {
      getTags().then(response => {
        this.tag_list = response.data
      })
    },
    handleSubmit(){
      editEvent(this.formData, this.event_id).then(response => {
          if(response){
            this.$message({
              message: 'Event edited',
              type: 'success'
            })
            this.$router.push({ path: this.redirect || '/events/show-event/' + this.event_id})
          }
          else {
            this.$message({
              message: 'Check your event\'s details again!',
              type: 'error'
            })
          }
        })
    }
  }
};
</script>

<style  scoped>
.components-container {
  position: relative;
  height: 100vh;
}
.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: #1872f0;
}
.bg-purple {
  background: #376497;
}
.bg-purple-light {
  background: #f4f4f5;
}
.grid-content {
  border-radius: 4px;
  min-height: 350px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
.el-tag + .el-tag {
  margin-left: 10px;
}
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
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
  width: 330px;
  height: 330px;
  display: block;
}
</style>
