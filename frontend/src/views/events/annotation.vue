<template>
<div>
  <el-row :gutter="8">
    <el-col v-for="(media, index) in eventDetails.medias" :key="media.id" :xs="{span: 24}" :sm="{span: 12}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}" style="margin-bottom:30px;">
      <el-card class="box-card-component" style="margin-left:8px;">
        <div slot="header" class="box-card-header">
            <img :src="media.file">
        </div>
        <div style="position:relative;">
          <el-select class="center-button" v-model="motivations[index]" slot="prepend" placeholder="Select Motivation">
            <el-option label="assessing" value="assessing"></el-option>
            <el-option label="bookmarking" value="bookmarking"></el-option>
            <el-option label="classifying	" value="classifying"></el-option>
            <el-option label="commenting" value="commenting"></el-option>
            <el-option label="describing" value="describing"></el-option>
            <el-option label="editing" value="editing"></el-option>
            <el-option label="identifying" value="identifying"></el-option>
            <el-option label="linking" value="linking"></el-option>
            <el-option label="moderating" value="moderating"></el-option>
            <el-option label="questioning" value="questioning"></el-option>
            <el-option label="tagging" value="tagging"></el-option>
          </el-select>
          <el-input
            type="textarea"
            autosize
            placeholder="Add Annotation"
            v-model="annot_texts[index]">
          </el-input>
          <div>
            <el-button round size="small" @click="annotate(media.id, media.file, index)" class="center-button" type="primary" icon="el-icon-check">Create Annotation</el-button>
          </div>
        </div>
      </el-card>
    </el-col>
  </el-row>
  <el-dialog
    title="Congrats"
    :visible.sync="dialogVisible"
    width="50%"
    :before-close="handleClose">
    <span>Annotation is added.</span>
    <span slot="footer" class="dialog-footer">
      <el-popover
      placement="bottom"
      title="The W3C Web Annotation Data Model: "
      width="600"
      trigger="hover"
      :content="last_annot_data">
      <el-button slot="reference">How do you store annotations?</el-button>
    </el-popover>
      <el-button type="primary" @click="dialogVisible = false">I love Cultidate!</el-button>
    </span>
  </el-dialog>
</div>
</template>


<script>
import { getEventDetail, createAnnotation} from '@/api/event'


  export default {
    data() {
      return {
        event_id: null,
        eventDetails: null,
        object_id: null,
        motivation: null,
        page_url: null,
        annot_texts: null,
        motivations: null,
        dialogVisible: false,
        last_annot_data: null,
      }
    },
    created() {
      this.event_id = this.$route.params.id
      const visited = this.$store.state.tagsView.visitedViews
      this.page_url = 'http://cultidate.ml/#/' + visited[visited.length - 1]
      this.fetchData(this.event_id)
    },
    methods: {
      fetchData(event_id) {
        getEventDetail(event_id).then(response => {
          this.eventDetails = response.data
          this.annot_texts = new Array(this.eventDetails.medias.length).fill(null);
          this.motivations = new Array(this.eventDetails.medias.length).fill(null);
        })
      },
      annotate(media_id, media_file, media_order){
        let d = new Date();
        const current_time = d.toISOString();
        const user_info = this.$store.state.user
        let annot_data = {
          content_type : "event",
          object_id: this.$route.params.id, // event_id
          data: {
            "@context": "http://www.w3.org/ns/anno.jsonld",
            id: (((1+Math.random())*0x10000)|0).toString(16).substring(1), //some random number currently
            type: "Annotation",
            motivation: this.motivations[media_order],
            target: {
              source: media_file,
              scope: this.page_url // url of page
            },
            body: this.annot_texts[media_order],// annotation itself
            created: current_time,
            creator: {
              type: "Person",
              email: user_info.username + '@cultidate.ml',
              name: user_info.first_name + user_info.last_name,
            },
            media_id: media_id,
          }
        }
        createAnnotation(annot_data).then(response => {
          if(response) {
            this.last_annot_data = JSON.stringify(annot_data, undefined, 2);
            this.dialogVisible = true
          }
        })
      }      
    }
  }
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .box-card-component {
    .box-card-header {
      position: relative;
      height: 220px;
      img {
        width: 100%;
        height: 100%;
        transition: all 0.4s linear;
        &:hover {
          transform: scale(1.1, 1.1);
          filter: contrast(130%);
        }
      }
    }
  }
  .center-button{
    margin:0 auto;
    display:block;
    margin-top: 10px;
  }
</style>
