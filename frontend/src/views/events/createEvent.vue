<template>
<div class="tab-container">
  <el-form ref="form" :model="form" label-width="200px" label-position="top" style="margin:20px">
    <el-form-item label="Title of event">
      <el-input v-model="form.title"></el-input>
    </el-form-item>
    <el-form-item label="Description of event">
      <el-input v-model="form.description"></el-input>
    </el-form-item>
    <el-form-item label="Date and time">
      <el-date-picker
          v-model="form.date"
          type="datetime"
          placeholder="Select date and time">
      </el-date-picker>
    </el-form-item>
    <el-form-item label="Price, enter 0 if free.">
      <el-input type="number" v-model="form.price">
        <template slot="append">₺</template>
      </el-input>
    </el-form-item>
    <el-form-item label="Website">
      <el-input v-model="form.organizer_url">
      </el-input>
    </el-form-item>
    <el-form-item label="Tags">
      <el-checkbox-group v-model="form.tags">
        <el-checkbox-button v-for="tag in tag_list" :label="tag.id" :key="tag.name">{{tag.name}}</el-checkbox-button>
      </el-checkbox-group>
    </el-form-item>


    <el-form-item label="Select location">
        <div>
          <label>
            <GmapAutocomplete placeholder="Please insert location" @place_changed="setPlace">
            </GmapAutocomplete>
            <el-button style="float: right;" type="primary" @click="usePlace">Add Location</el-button>
          </label>
          <br/>

          <GmapMap style="width: 600px; height: 300px; margin-top: 15px;" :zoom="5" :center="{ lat: 41.015137,lng: 28.979530 }">
            <GmapMarker v-for="(marker, index) in markers"
              :key="index"
              :position="marker.position"
              />
            <GmapMarker
              v-if="this.place"
              label="★"
              :position="{
                lat: this.place.geometry.location.lat(),
                lng: this.place.geometry.location.lng(),
              }"
              />
          </GmapMap>
        </div>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="onSubmit">Create</el-button>
    </el-form-item>
  </el-form>
  
</div>
</template>


<script>
import { createEvent, getTags } from '@/api/event'

  export default {
    data() {
      return {
        form: {
          title: '',
          description: '',
          date: '',
          price: null,
          organizer_url: '',
          location: {
            city: '',
            district: '',
            google_place_id: '',
            name: '',
            lat: null,
            lng: null
          },
          tags: []
        },
        tag_list: [],
        markers: [],
        place: null

      }
    },
    created() {
      this.getTagList()
    },
    methods: {
      setPlace(place) {
        this.place = place
        for (var i = 0; i < this.place.address_components.length; i++) {
          if(this.place.address_components[i].types[0] == "administrative_area_level_1") {
            this.form.location.city = this.place.address_components[i].long_name
          }
          else if(this.place.address_components[i].types[0] == "administrative_area_level_2") {
            this.form.location.district = this.place.address_components[i].long_name
          }
        }
        console.log(this.form.location.district + ", " + this.form.location.city)
        this.form.location.name = this.place.name
        this.form.location.lat = this.place.geometry.location.lat().toFixed(6)
        this.form.location.lng = this.place.geometry.location.lng().toFixed(6)
        this.form.location.google_place_id = this.place.id
      },
      usePlace(place) {
        if (this.place) {
          this.markers.push({
            position: {
              lat: this.place.geometry.location.lat(),
              lng: this.place.geometry.location.lng(),
            }
          })
          this.place = null;
        }
      },
      onSubmit() {
        // URL needs to start with http or https as dictated by backend
        if(!this.form.organizer_url.startsWith('http://') &&
        !this.form.organizer_url.startsWith('https://') ){
          this.form.organizer_url = 'http://' + this.form.organizer_url
        }
        createEvent(this.form).then(response => {
          
          if(response){
          this.$message({
            message: 'Event created',
            type: 'success'
          })
          this.$router.push({ path: this.redirect || '/dashboard' })
          }
          else {
            this.$message({
              message: 'Check your event\'s details again!',
              type: 'error'
            })
          }
        })
      },
      getTagList() {
        getTags().then(response => {
          this.tag_list = response.data
        })
      }
    }
  }
</script>

<style>
.el-form-item{
  width: 400px;
  max-width: 100%;
}
</style>
