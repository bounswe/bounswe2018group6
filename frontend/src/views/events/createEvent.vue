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
    <el-form-item label="City">
      <el-input v-model="form.location.city">
      </el-input>
    </el-form-item>
    <el-form-item label="District">
      <el-input v-model="form.location.district">
      </el-input>
    </el-form-item>
    <el-form-item label="Tags">
      <el-checkbox-group v-model="form.tags">
        <el-checkbox-button v-for="tag in tag_list" :label="tag.id" :key="tag.name">{{tag.name}}</el-checkbox-button>
      </el-checkbox-group>
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
          },
          tags: []
        },
        tag_list: []
      }
    },
    created() {
      this.getTagList()
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
