<script setup lang="ts">
import { BillingAddress } from '@/types/BillingAddress'
import { UserDetail } from '@/types/UserProperties'

interface Props {
  isDialogVisible: boolean
}

interface Emit {
  (e: 'update:isDialogVisible', value: boolean): void
  (e: 'submit', value: BillingAddress): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emit>()

const userData = inject('userData') as Ref<UserDetail | undefined>

const billingAddress = ref<Partial<BillingAddress>>({
  regSociale: '',
  piva: '',
  address: '',
  city: '',
  prov: '',
  stato: '',
  cap: '',
  ...userData.value?.billing_address
})

const resetForm = () => {
  emit('update:isDialogVisible', false)
  billingAddress.value = {
    regSociale: '',
    piva: '',
    address: '',
    city: '',
    prov: '',
    stato: '',
    cap: '',
    ...userData.value?.billing_address
  }
}

const onFormSubmit = () => {
  emit('update:isDialogVisible', false)
  emit('submit', billingAddress.value as BillingAddress)
}
</script>

<template>
  <VDialog
    :width="$vuetify.display.smAndDown ? 'auto' : 900 "
    :model-value="props.isDialogVisible"
    @update:model-value="val => $emit('update:isDialogVisible', val)"
  >
    <VCard class="pa-sm-11 pa-3">
      <VCardText class="pt-5">
        <!-- 👉 dialog close btn -->
        <DialogCloseBtn
          variant="text"
          size="default"
          @click="resetForm"
        />

        <!-- 👉 Title -->
        <div class="text-center mb-6">
          <h4 class="text-h4 mb-2">
            {{ userData?.billing_address ? 'Modifica' : 'Aggiungi' }} Indirizzo
          </h4>

          <p class="text-body-1">
            Indirizzo di fatturazione per l'utente {{ userData?.nome }} {{ userData?.cognome }}
          </p>
        </div>

        <!-- 👉 Form -->
        <VForm @submit.prevent="onFormSubmit">
          <VRow>
            <!-- 👉 Ragione Sociale -->
            <VCol
              cols="12"
              md="6"
            >
              <VTextField
                v-model="billingAddress.regSociale"
                label="Ragione Sociale"
                placeholder="Azienda SRL"
              />
            </VCol>

            <!-- 👉 P.IVA -->
            <VCol
              cols="12"
              md="6"
            >
              <VTextField
                v-model="billingAddress.piva"
                label="Partita Link / C.F."
                placeholder="IT12345678901"
              />
            </VCol>

            <!-- 👉 Indirizzo -->
            <VCol cols="12">
              <VTextField
                v-model="billingAddress.address"
                label="Indirizzo"
                placeholder="Via Roma, 1"
              />
            </VCol>

            <!-- 👉 Città -->
            <VCol
              cols="12"
              md="6"
            >
               <VTextField
                v-model="billingAddress.city"
                label="Città"
                placeholder="Milano"
              />
            </VCol>

            <!-- 👉 Provincia -->
            <VCol
              cols="12"
              md="6"
            >
              <VTextField
                v-model="billingAddress.prov"
                label="Provincia"
                placeholder="MI"
              />
            </VCol>

            <!-- 👉 Stato -->
            <VCol
              cols="12"
              md="6"
            >
              <VTextField
                v-model="billingAddress.stato"
                label="Stato"
                placeholder="Italia"
              />
            </VCol>

            <!-- 👉 CAP -->
            <VCol
              cols="12"
              md="6"
            >
              <VTextField
                v-model="billingAddress.cap"
                label="CAP"
                placeholder="20100"
                type="number"
              />
            </VCol>

            <!-- 👉 Submit and Cancel button -->
            <VCol
              cols="12"
              class="text-center"
            >
              <VBtn
                type="submit"
                class="me-3"
              >
                Salva
              </VBtn>

              <VBtn
                variant="outlined"
                color="secondary"
                @click="resetForm"
              >
                Annulla
              </VBtn>
            </VCol>
          </VRow>
        </VForm>
      </VCardText>
    </VCard>
  </VDialog>
</template>
