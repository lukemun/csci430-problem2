<template>
  <div class="container">
    <div class="row">
      <b-col>
        <h1>Images for {{ email }}</h1>
        <h2>{{ first_name }} {{ last_name }}</h2>
        <h2>Date of birth: {{ dob }}</h2>
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
      email: "",
      first_name: '',
      last_name: '',
      dob: '',
      token: "",
			imgs: [],
			uploadFile: [],
		};
	},
	props: {
    raw_email: String,
    raw_first_name: String,
    raw_last_name: String,
    raw_dob: String,
    raw_token: String,
  },
	methods: {
		upload(evt) {
			evt.preventDefault();
      const path = 'http://192.168.1.142/upload';
			var reader = new FileReader();
			reader.onload = (e) => {
        // console.log('target', e.target.result);
				const payload = {
					name: this.uploadFile.name,
					file: e.target.result,
          creator_email: this.email,

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
      const path = 'http://192.168.1.142/getImages';
      const payload = {
        email: this.email,
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
    this.email = this.raw_email;
    this.first_name = this.raw_first_name;
    this.last_name = this.raw_last_name;
    this.dob = this.raw_dob;
    this.token = this.raw_token;
    console.log(this.username, this.token);
	}
}
</script>
