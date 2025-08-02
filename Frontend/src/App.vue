<template>
  <div class="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-6">
    <div v-if="!authenticated" class="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">
      <h2 class="text-2xl font-bold text-center mb-6">Login</h2>
      <form @submit.prevent="login" class="flex flex-col gap-4">
        <input
          v-model="email"
          type="email"
          placeholder="Email"
          required
          class="border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          required
          class="border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          type="submit"
          class="bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition"
        >
          Login
        </button>
        <p v-if="loginError" class="text-red-500 text-sm text-center">Invalid email or password.</p>
      </form>
    </div>

    <div v-else class="bg-white p-8 rounded-xl shadow-lg w-full max-w-xl mt-4">
      <h2 class="text-2xl font-bold text-center mb-6">Patient Record</h2>
      <div v-if="patient" class="space-y-4">
        <div>
          <h3 class="text-lg font-semibold">Name:</h3>
          <p>{{ patient.name }}</p>
        </div>
        <div>
          <h3 class="text-lg font-semibold">Medical History:</h3>
          <p>{{ patient.medical_history }}</p>
        </div>
        <div>
          <h3 class="text-lg font-semibold">Medications:</h3>
          <p>{{ patient.medications }}</p>
        </div>
        <div>
          <h3 class="text-lg font-semibold">Allergies:</h3>
          <p>{{ patient.allergies }}</p>
        </div>
        <div>
          <h3 class="text-lg font-semibold">Emergency Contact:</h3>
          <p>{{ patient.emergency_contact }}</p>
        </div>

        <hr class="my-4" />
        <div>
          <h4 class="text-lg font-semibold mb-2">Upload Image</h4>
          <input
            type="file"
            @change="handleFileUpload"
            class="file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          <p v-if="uploadSuccess" class="text-green-600 mt-2">File uploaded successfully</p>
        </div>
      </div>
      <p v-else class="text-center text-gray-500">Loading patient data...</p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import axios from 'axios'

const email = ref('')
const password = ref('')
const authenticated = ref(false)
const loginError = ref(false)

const patientId = ref<number | null>(null)
const patient = ref<any>(null)
const uploadSuccess = ref(false)

const login = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:5000/${email.value}/${password.value}`)
    if (res.data && res.data.id) {
      patientId.value = res.data.id
      authenticated.value = true
      fetchPatient()
    } else {
      loginError.value = true
    }
  } catch (error) {
    loginError.value = true
    console.error('Login failed:', error)
  }
}

const fetchPatient = async () => {
  if (patientId.value !== null) {
    try {
      const res = await axios.get(`http://127.0.0.1:5000/patients/${patientId.value}`)
      patient.value = res.data
    } catch (error) {
      console.error('Error fetching patient:', error)
    }
  }
}

const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    const file = target.files[0]
    console.log('Simulated upload for file:', file.name)
    setTimeout(() => {
      uploadSuccess.value = true
    }, 1000)
  }
}
</script>

<style scoped>
.patient-card {
  padding: 1rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}
</style>