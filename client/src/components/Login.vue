<template>
  <div class="container">
  	<b-row>
  		<b-col>
  		</b-col>
  		<b-col>
			<b-row>
				<h2> Photo App </h2>
			</b-row>
			<b-row>
				<p> Create account or login here </p>
			</b-row>
			<b-row>
				<b-form @submit='login'>
					<b-form-row>
  					<b-input-group prepend='Username'>
  						<b-form-input
  							v-model='form.username'
  							type='text'
  							required>
							</b-form-input>
						</b-input-group>
					</b-form-row>
					<b-form-row class="mt-4 mb-4">
  						<b-input-group prepend='Password'>
  							<b-form-input
	  							v-model='form.password'
	  							type='password'
	  							required>
							</b-form-input>
						</b-input-group>
					</b-form-row>
					<b-button-group>
						<b-button type='submit' variant='info'>Login</b-button>
						<b-button type='button' @click='register' variant='secondary'>Register</b-button>
					</b-button-group>
				</b-form>
			</b-row>
  		</b-col>
  		<b-col>
  		</b-col>
  	</b-row>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      msg: '',
      form: {
      	username: '',
      	password: '',
      }
    };
  },
  methods: {
    login(evt) {
    	evt.preventDefault();
    	const payload = {
    		username: this.form.username,
    		password: this.form.password,
    	}
    	console.log(payload);
    	this.attemptLogin(payload);
    },
    attemptLogin(payload) {
    	console.log('login attempt');
    	const path = 'http://localhost:5000/login'

    	axios.post(path, payload)
    		.then((response) => {
    			console.log(response.data);
    			if (response.data.error != null) {
    				alert(response.data.error);
    				this.clear();
    			} else {

    			}
    		})
    		.catch((error) => {
    			console.log('error', error);
    			alert("unauthorized login");
    		});
    },
    register(evt) {
    	evt.preventDefault();
    	const payload = {
    		username: this.form.username,
    		password: this.form.password,
    	}
    	console.log(payload);
    	this.attemptRegister(payload);
    },
    attemptRegister(payload) {
    	console.log('register attempt');
    	const path = 'http://localhost:5000/register'

    	axios.post(path, payload)
    		.then((response) => {
    			console.log(response.data);
    			if (response.data.error != null) {
    				alert('username taken');
    				this.clear();
    			}
    		})
    		.catch((error) => {
    			console.log('error', error);
    		});
    },
    clear() {
    	this.form.username = '';
    	this.form.password = '';
    }
  },
  created() {
    // this.getMessage();
  },
};
</script>