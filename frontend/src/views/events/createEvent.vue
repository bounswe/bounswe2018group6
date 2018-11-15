<template>
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
    <el-input type="number" v-model="form.price"></el-input>
  </el-form-item>
  <el-form-item label="Website">
    <el-input v-model="form.organizer_url">
    </el-input>
  </el-form-item>
  <el-form-item label="Artists - NOT AVAILABLE">
    <el-input v-model="form.artists"></el-input>
  </el-form-item>
  <el-form-item label="Medias- NOT AVAILABLE">
    <el-input v-model="form.medias"></el-input>
  </el-form-item>
  <el-form-item label="Tags">
    <el-input v-model="form.tags"></el-input>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="onSubmit">Create</el-button>
  </el-form-item>
</el-form>
</template>


<script>
import { createEvent } from '@/api/event'

  export default {
    data() {
      return {
        form: {
          title: '',
          description: '',
          date: '',
          price: '',
          organizer_url: '',
          artist: '',
          medias: [],
          tags: []
        }
      }
    },
    methods: {
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
