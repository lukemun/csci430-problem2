<template>
  <div class="container">
  	<b-row>
  		<b-col>
  		</b-col>
  		<b-col>
			<b-row>
				<b-button type='button' @click='chooseLogin' variant='info'>Login</b-button>
				<b-button type='button' @click='chooseRegister' variant='secondary'>Register</b-button>
			</b-row>
			<b-row>
				<h2> Photo App </h2>
			</b-row>
			<b-row v-if="this.loginBool">
				<b-form @submit='login'>
					<b-form-row>
  						<b-input-group prepend='Email'>
  							<b-form-input
  								v-model='form.email'
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
					</b-button-group>
				</b-form>
			</b-row>
			<b-row v-if="this.registerBool">
				<b-form @submit='register'>
					<b-form-row>
  						<b-input-group prepend='Email'>
  							<b-form-input
  								v-model='form.email'
  								type='text'
  								required>
							</b-form-input>
						</b-input-group>
					</b-form-row>
					<b-form-row class="mt-4 mb-4">
  						<b-input-group prepend='First name'>
  							<b-form-input
	  							v-model='form.first_name'
	  							type='text'
	  							required>
							</b-form-input>
						</b-input-group>
					</b-form-row>
					<b-form-row class="mt-4 mb-4">
  						<b-input-group prepend='Last Name'>
  							<b-form-input
	  							v-model='form.last_name'
	  							type='text'
	  							required>
							</b-form-input>
						</b-input-group>
					</b-form-row>
					<b-form-row class="mt-4 mb-4">
  						<b-input-group prepend='Date of Birth'>
  							<b-form-datepicker
								v-model='form.dob'
								required
							>
							</b-form-datepicker>
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
						<b-button type='submit' variant='secondary'>Register</b-button>
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
		email: '',
		first_name: '',
		last_name: '',
		dob: '',
      	password: '',
      },
	  loginBool: false,
	  registerBool: false
    };
  },
  methods: {
	chooseLogin() {
		this.loginBool = true;
		this.registerBool = false;
	},
	chooseRegister() {
		this.loginBool = false;
		this.registerBool = true;
	},
    login(evt) {
    	evt.preventDefault();
		const payload = {
			email: this.form.email,
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
				console.log("Hello!");
    			console.log(response.data);
    			if (response.data.error != null) {
    				alert(response.data.error);
    				this.clear();
    			} else {
    				console.log('succesful login');
    				this.$router.push({
    					name: 'User',
    					params: {
                			raw_email: this.form.email,
							raw_first_name: response.data.first_name,
							raw_last_name: response.data.last_name,
							raw_dob: response.data.dob,
    						raw_token: response.data.token,
    					}
    				});
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
			email: this.form.email,
			first_name: this.form.first_name,
			last_name: this.form.last_name,
			dob: this.form.dob,
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
    				alert(response.data.error);
    				this.clear();
    			} else {
            alert('user created, login to continue');
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