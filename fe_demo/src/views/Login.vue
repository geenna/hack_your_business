<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12" rounded="lg">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Login</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="login" ref="form">
              <v-text-field
                v-model="email"
                label="Email"
                name="email"
                prepend-icon="mdi-account"
                type="email"
                required
              ></v-text-field>
              <v-text-field
                v-model="password"
                id="password"
                label="Password"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                required
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="login" :loading="loading">Login</v-btn>
          </v-card-actions>
          <v-alert v-if="error" type="error" dense class="ma-4">
            {{ error }}
          </v-alert>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

const email = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);
const router = useRouter();

const login = async () => {
  error.value = '';
  loading.value = true;
  
  // Create form data as URLSearchParams (standard for OAuth2PasswordRequestForm expected by backend)
  const formData = new URLSearchParams();
  formData.append('username', email.value);
  formData.append('password', password.value);

  try {
    const response = await api.post('/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    
    // Check if token exists
    if (response.data && response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      router.push('/dashboard');
    } else {
       error.value = 'Failed to retrieve token';
    }
  } catch (err) {
    if (err.response && err.response.data && err.response.data.detail) {
        error.value = err.response.data.detail;
    } else {
        error.value = 'Login failed. Please check your credentials.';
    }
  } finally {
    loading.value = false;
  }
};
</script>
