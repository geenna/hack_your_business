<template>
  <v-container>
    <v-row class="mb-5">
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
             Dashboard
             <v-btn color="error" variant="text" @click="logout" prepend-icon="mdi-logout">Logout</v-btn>
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <!-- Create User Section -->
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Create New User</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="createUser" ref="createForm">
              <v-text-field v-model="newUser.email" label="Email" required></v-text-field>
              <v-text-field v-model="newUser.password" label="Password" type="password" required></v-text-field>
              <v-text-field v-model="newUser.nome" label="First Name" required></v-text-field>
              <v-text-field v-model="newUser.cognome" label="Last Name" required></v-text-field>
              <v-select 
                v-model="newUser.userType" 
                :items="['admin', 'user']" 
                label="User Type" 
                required
              ></v-select>
              <v-select
                v-model="newUser.roles"
                :items="['admin', 'user']"
                label="Roles"
                multiple
                clearable
                chips
              ></v-select>
              
              <v-btn color="success" class="mt-4" type="submit" :loading="creatingUser">Create User</v-btn>
            </v-form>
          </v-card-text>
          <v-alert v-if="createMsg" :type="createStatus" class="ma-4">
             {{ createMsg }}
          </v-alert>
        </v-card>
      </v-col>

      <!-- Test Data Section -->
      <v-col cols="12" md="6">
        <v-card class="h-100">
          <v-card-title>Test API Endpoints</v-card-title>
          <v-card-text>
             <div class="d-flex flex-column gap-4">
                <v-btn color="info" class="mb-4" @click="testAdminData">Test Admin Data</v-btn>
                <v-btn color="warning" class="mb-4" @click="testUserData">Test User Data</v-btn>
                <v-btn color="warning" class="mb-4" @click="testAllData">Test All Data</v-btn>
             </div>
             
             <v-divider class="my-4"></v-divider>
             
             <div v-if="testResult">
               <strong>Response:</strong>
               <pre class="bg-grey-darken-3 pa-2 rounded mt-2">{{ testResult }}</pre>
             </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

const router = useRouter();

// Create User State
const newUser = reactive({
  email: '',
  password: '',
  nome: '',
  cognome: '',
  userType: 'user',
  roles: ['user']
});
const creatingUser = ref(false);
const createMsg = ref('');
const createStatus = ref('success');

// Test Data State
const testResult = ref(null);

const createUser = async () => {
  creatingUser.value = true;
  createMsg.value = '';
  try {
    const response = await api.post('/users', newUser);
    createStatus.value = 'success';
    createMsg.value = `User created: ${response.data.email}`;
    // Reset form mostly
    newUser.email = '';
    newUser.password = '';
  } catch (error) {
    createStatus.value = 'error';
    createMsg.value = error.response?.data?.detail || 'Failed to create user';
  } finally {
    creatingUser.value = false;
  }
};

const testAdminData = async () => {
  testResult.value = 'Loading...';
  try {
    const response = await api.get('/admin-data'); // Endpoint from memory: Check actual path in users.py
    testResult.value = JSON.stringify(response.data, null, 2);
  } catch (error) {
    testResult.value = `Error: ${error.response?.status} - ${error.response?.data?.detail || error.message}`;
  }
};

const testAllData = async () => {
  testResult.value = 'Loading...';
  try {
    const response = await api.get('/all-data'); // Endpoint from memory: Check actual path in users.py
    testResult.value = JSON.stringify(response.data, null, 2);
  } catch (error) {
    testResult.value = `Error: ${error.response?.status} - ${error.response?.data?.detail || error.message}`;
  }
};

const testUserData = async () => {
  testResult.value = 'Loading...';
  try {
    const response = await api.get('/user-data');
    testResult.value = JSON.stringify(response.data, null, 2);
  } catch (error) {
    testResult.value = `Error: ${error.response?.status} - ${error.response?.data?.detail || error.message}`;
  }
};

const logout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};
</script>
