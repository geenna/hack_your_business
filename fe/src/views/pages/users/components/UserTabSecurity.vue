<script setup lang="ts">
import { useAlert } from '@/shared/state/alert'
import UserService from '@/services/UserService'

const { show: showAlert } = useAlert()
const selectedUserID = inject('selectedUserID') as Ref<string>

const isNewPasswordVisible = ref(false)
const isConfirmPasswordVisible = ref(false)

const newPassword = ref('')
const confirmPassword = ref('')
const errors = ref({
  passwordMatch: '',
})

const onSubmit = async () => {
  errors.value.passwordMatch = ''
  
  if (newPassword.value !== confirmPassword.value) {
    errors.value.passwordMatch = 'Le password non corrispondono'
    return
  }
  
  if (newPassword.value.length < 8) {
    errors.value.passwordMatch = 'La password deve essere di almeno 8 caratteri'
    return
  }

  try {
    await UserService.changePassword(selectedUserID.value, newPassword.value)
    showAlert('Successo', 'Password aggiornata con successo', 'success')
    newPassword.value = ''
    confirmPassword.value = ''
  } catch (error) {
    console.error(error)
    showAlert('Errore', 'Errore durante l\'aggiornamento della password', 'error')
  }
}
</script>

<template>
  <VRow>
    <VCol cols="12">
      <!-- 👉 Change password -->
      <VCard title="Cambia Password">
        <VCardText>
          <VAlert
            variant="tonal"
            color="warning"
            closable
            class="mb-6"
          >
            <VAlertTitle>Assicurati di usare una password complessa</VAlertTitle>
            <span>Minimo 8 caratteri, maiuscole e minuscole, numeri e simboli</span>
          </VAlert>

          <VForm @submit.prevent="onSubmit">
            <VRow>
              <VCol
                cols="12"
                md="6"
              >
                <VTextField
                  v-model="newPassword"
                  label="New Password"
                  placeholder="············"
                  :type="isNewPasswordVisible ? 'text' : 'password'"
                  :append-inner-icon="isNewPasswordVisible ? 'ri-eye-off-line' : 'ri-eye-line'"
                  :error-messages="errors.passwordMatch"
                  @click:append-inner="isNewPasswordVisible = !isNewPasswordVisible"
                />
              </VCol>
              <VCol
                cols="12"
                md="6"
              >
                <VTextField
                  v-model="confirmPassword"
                  label="Confirm Password"
                  autocomplete="confirm-password"
                  placeholder="············"
                  :type="isConfirmPasswordVisible ? 'text' : 'password'"
                  :append-inner-icon="isConfirmPasswordVisible ? 'ri-eye-off-line' : 'ri-eye-line'"
                  @click:append-inner="isConfirmPasswordVisible = !isConfirmPasswordVisible"
                />
              </VCol>

              <VCol cols="12">
                <VBtn type="submit">
                  Cambia Password
                </VBtn>
              </VCol>
            </VRow>
          </VForm>
        </VCardText>
      </VCard>
    </VCol>
  </VRow>
</template>
