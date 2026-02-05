<script setup lang="ts">
import { requiredValidator } from '@/@core/utils/validators'
import { VCardText } from 'vuetify/components';
import { VForm } from 'vuetify/components/VForm'

interface Emits {
  (e: 'submit', data: { date: any; value: number; status: string; tipoPagamento: string }): void
  (e: 'cancel'): void
}

const props = defineProps({
    showVCard: {
        type: Boolean,
        default: true
    }
})  
const emit = defineEmits<Emits>()

const value = ref<number | null>(null)
const status = ref('')
const tipoPagamento = ref('')

const statusOptions = ['In attesa', 'Pagato', 'Rifiutato', 'Annullato']
const typeOptions = ['Bonifico', 'Carta di Credito', 'PayPal', 'Contanti']

const refForm = ref<VForm>()
const date = ref(new Date())

const onSubmit = () => {
  refForm.value?.validate().then(({ valid: isValid }) => {
    if (isValid && value.value !== null) {
      emit('submit', {
        date: date.value,
        value: value.value,
        status: status.value,
        tipoPagamento: tipoPagamento.value,
      })
      resetForm()
    }
  })
}

const onCancel = () => {
  emit('cancel')
  resetForm()
}

const validateAndGetPayload = async () => {
  onSubmit()
}

const resetForm = () => {
  value.value = null
  status.value = ''
  tipoPagamento.value = ''
  nextTick(() => {
    refForm.value?.resetValidation()
  })
}

defineExpose({
  validateAndGetPayload
})

</script>

<template>
  <VCard :class=" showVCard ? 'pa-sm-11 pa-3' :''" :flat="!showVCard">
    <VCardText :class=" showVCard ? 'pt-5' :''">
      <div class="text-center pb-6">
        <h4 class="text-h4 mb-2">
          Aggiungi pagamento
        </h4>
      </div>
      <VForm
        ref="refForm"
        @submit.prevent
      >
        <VRow>
          <VCol cols="12">
            <VTextField
              v-model.number="value"
              label="Importo"
              type="number"
              :rules="[requiredValidator]"
            />
          </VCol>
          <VCol cols="12">
            <VSelect
              v-model="status"
              :items="statusOptions"
              label="Stato"
              :rules="[requiredValidator]"
            />
          </VCol>
          <VCol cols="12">
            <VSelect
              v-model="tipoPagamento"
              :items="typeOptions"
              label="Tipo Pagamento"
              :rules="[requiredValidator]"
            />
          </VCol>
          <VCol cols="12">
            <AppDateTimePicker
              v-model="date"
              label="Data"
              placeholder="Seleziona la data"
              :config="{ mode: 'single', format: 'dd/MM/yyyy' }"
              :rules="[requiredValidator]"
            />
          </VCol>
        </VRow>
      </VForm>
    </VCardText>

    <VCardActions v-if="showVCard">
      <VSpacer />
      <VBtn
        color="secondary"
        variant="tonal"
        @click="onCancel"
      >
        Annulla
      </VBtn>
      <VBtn
        color="primary"
        variant="elevated"
        @click="onSubmit"
      >
        Salva
      </VBtn>
    </VCardActions>
  </VCard>
</template>