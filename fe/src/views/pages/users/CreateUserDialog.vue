<script setup lang="ts">
import { countries } from '@/utils/constants'
import { requiredValidator } from '@core/utils/validators'
import UserService from '@/services/UserService'

interface UserData {
  id?: string
  nome: string
  cognome: string
  email: string
  cf: string
  indirizzoResidenza: string
  citta: string
  cap: string
  prov: string
  regioneSociale: string
  piva: string
  telefono: string
  stato: string
  userType: string
}

interface Props {
  userData?: UserData
  isDialogVisible: boolean
}

interface Emit {
  (e: 'submit', value: UserData): void
  (e: 'update:isDialogVisible', val: boolean): void
}

const props = withDefaults(defineProps<Props>(), {
  userData: () => ({
    email: '',
    nome: '',
    cognome: '',
    cf: '',
    indirizzoResidenza: '',
    citta: '',
    cap: '',
    prov: '',
    regioneSociale: '',
    piva: '',
    telefono: '',
    stato: '',
    userType: '',
  }),
})

const emit = defineEmits<Emit>()

const userData = ref<UserData>(structuredClone(toRaw(props.userData)))

watch(() => props, () => {
  userData.value = structuredClone(toRaw(props.userData))
})



const onFormReset = () => {
  userData.value = structuredClone(toRaw(props.userData))
  emit('update:isDialogVisible', false)
}

type VForm = {
  validate: () => Promise<{ valid: boolean }>
}

const refForm = ref<VForm>()

const onSubmit = () => {
  refForm.value?.validate().then(({ valid: isValid }) => {
    if (isValid) {
      if (userData.value.id) {
         UserService.updateUser(userData.value.id, userData.value).then(() => {
          emit('submit', userData.value)
          emit('update:isDialogVisible', false)
        }).catch(error => {
          console.error("Error updating user:", error)
          // Optionally handle error (e.g. show notification)
        })
      } else {
        const userToSave = {
          ...userData.value,
          password: 'Password@123', // Default password
          roles: []                  // Default roles (backend handles logic)
        }
        UserService.createUser(userToSave).then(() => {
          emit('submit', userData.value)
          emit('update:isDialogVisible', false)
        }).catch(error => {
          console.error("Error creating user:", error)
          // Optionally handle error (e.g. show notification)
        })
      }
    }
  })
}

</script>

<template>
  <VDialog
    :width="$vuetify.display.smAndDown ? 'auto' : 900 "
    :model-value="props.isDialogVisible"
  >
    <VCard class="pa-sm-11 pa-3">
      <!-- 👉 dialog close btn -->
      <DialogCloseBtn
        variant="text"
        size="default"
        @click="onFormReset"
      />

      <VCardText class="pt-5">
        <div class="text-center pb-6">
          <h4 class="text-h4 mb-2">
            {{ userData.id ? 'Modifica utente' : 'Crea nuovo utente' }}
          </h4>
        </div>

        <!-- 👉 Form -->
        <VForm
          ref="refForm"
          class="mt-4"
          @submit.prevent="onSubmit"
        >
          <VRow>
            <!-- 👉 First Name -->
            <VCol
              cols="12"
              md="6"
            >
              <VTextField
                v-model="userData.nome"
                label="Nome"
                placeholder="Mario"
                :rules="[requiredValidator]"
              />
            </VCol>

            <!-- 👉 Last Name -->
            <VCol
              cols="12"
              md="6"
            >
              <VTextField
                v-model="userData.cognome"
                label="Cognome"
                placeholder="Rossi"
                :rules="[requiredValidator]"
              />
            </VCol>

            <VCol
              cols="12"
              md="6"
            >
             <VTextField
                v-model="userData.cf"
                label="Cod. Fiscale"
                placeholder="RSSMRA80C12H501Z"
                :rules="[requiredValidator]"
              />
            </VCol>

            <!-- 👉 Email -->
            <VCol
              cols="12"
              md="6"
            >
              <VTextField
                v-model="userData.email"
                label="email"
                placeholder="m.rossi@email.com"
                :rules="[requiredValidator]"
              />
            </VCol>

           
            
            <VCol
              cols="12"
              md="6"
            >
              <VTextField
                v-model="userData.indirizzoResidenza"
                label="Indirizzo Residenza"
                placeholder="Via Roma 123"
              />
            </VCol>

            <VCol
              cols="12"
              md="6"
            >
              <VTextField
                v-model="userData.citta"
                label="Città"
                placeholder="Roma"
                :rules="[requiredValidator]"
              />
            </VCol>

            <VCol
              cols="12"
              md="6"
            >
              <VTextField
                v-model="userData.cap"
                label="Cap"
                placeholder="00123"
                :rules="[requiredValidator]"
              />
            </VCol>

            <VCol
              cols="12"
              md="6"
            >
              <VTextField
                v-model="userData.prov"
                label="Provincia"
                placeholder="RM"
                :rules="[requiredValidator]"
              />
            </VCol>

               <VCol
              cols="12"
              md="6"
            >
              <VSelect
                v-model="userData.stato"
                :items="countries"
                label="Stato"
                placeholder="Italy"
                :rules="[requiredValidator]"
              />
            </VCol>

            <!-- 👉 Contact -->
            <VCol
              cols="12"
              md="6"
            >
              <VTextField
                v-model="userData.telefono"
                label="Telefono"
                placeholder="+39 347123456"
                :rules="[requiredValidator]"
              />
            </VCol>
            <!-- 👉 Role -->
            <VCol
              cols="12"
              md="6"
            >
              <VSelect
                v-model="userData.userType"
                :items="['Collaboratore', 'Cliente']"
                label="Ruolo"
                placeholder="Seleziona Ruolo"
                :rules="[requiredValidator]"
              />
            </VCol>
            <!-- 👉 Submit and Cancel -->
            <VCol
              cols="12"
              class="d-flex flex-wrap justify-center gap-4"
            >
              <VBtn type="submit">
                Submit
              </VBtn>

              <VBtn
                color="secondary"
                variant="outlined"
                @click="onFormReset"
              >
                Cancel
              </VBtn>
            </VCol>
          </VRow>
        </VForm>
      </VCardText>
    </VCard>
  </VDialog>
</template>
