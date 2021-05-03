<template>
  <div class="container">
    <div class="row">
      <b-col>
        <h1>Images for {{ username }}</h1>
        <hr><br>
        <button type="button" @click='getImages' class="btn btn-success btn-sm">Get Images</button>
        <hr><br>
      </b-col>
    </div>
    <b-row>
    	<b-col>
    		<b-form @submit='upload'>
    			<b-form-row>
    				<b-col>
    				</b-col>
    				<b-col>
			    		<b-form-file v-model='uploadFile' plain>
			    		</b-form-file>
			    		<p>
			    			{{ uploadFile.name }}
			    		</p>
			    	</b-col>
			    	<b-col>
			    		<b-button type='submit' variant='info'>Upload</b-button>
			    	</b-col>
			    	<b-col>
			    	</b-col>
		    	</b-form-row>
	    	</b-form>
    	</b-col>
    </b-row>
    <hr>
    <b-row class="mt-2" v-for="(item) in imgs" :key="imgs.index">
    	<b-col>
	    	<p> {{ item.name }} </p>
	    	<img style="width: 200px; height:200px;" :src="item.file" >
	    </b-col>
    </b-row>
  </div>
</template>

<script>
import axios from 'axios';

export default {
	name: 'User',
	data() {
		return {
      username: "",
      token: "",
			imgs: [],
			uploadFile: [],
		};
	},
	props: {
    raw_username: String, 
    raw_token: String,
  },
	methods: {
		upload(evt) {
			evt.preventDefault();
      const path = 'http://localhost:5000/upload';
			var reader = new FileReader();
			reader.onload = (e) => {
        // console.log('target', e.target.result);
				const payload = {
					name: this.uploadFile.name,
					file: e.target.result,
          creator_name: this.username,
          token: this.token,

				}

        axios.post(path, payload)
          .then((response) => {
            console.log(response);
            if (response.data.error != null) {
              alert(response.data.error);
            } else {
              this.imgs.push(payload);
            }
          })
          .catch((error) => {
            console.log('error', error);
          });
      }

			// console.log('file', this.uploadFile);

			reader.readAsDataURL(this.uploadFile);
      // console.log('imgs', this.imgs);
		},
    getImages() {
      const path = 'http://localhost:5000/getImages';
      const payload = {
        username: this.username,
        token: this.token,
      }
      axios.post(path, payload)
        .then((response) => {
          console.log(response);
          if (response.data.error != null) {
            alert(response.data.error);
          } else {
            this.imgs = response.data.imgs;
          }
        })
        .catch((error) => {
          console.log('error', error);
        });
    }
	},
	created() {
		console.log('created');
    this.username = this.raw_username;
    this.token = this.raw_token;
    console.log(this.username, this.token);
	}
}
</script>