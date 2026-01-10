<script setup lang="ts">
import { ref } from 'vue'
import { VForm } from 'vuetify/components/VForm'
import { requiredValidator } from '@/@core/utils/validators'

interface Props {
  isDialogVisible: boolean
}

interface Emits {
  (e: 'update:isDialogVisible', val: boolean): void
  (e: 'submit', data: { date: string; value: number; status: string; tipoPagamento: string }): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const paymentId = ref('')
const value = ref<number | null>(null)
const status = ref('')
const tipoPagamento = ref('')

const statusOptions = ['In attesa', 'Pagato', 'Rifiutato', 'Annullato']
const typeOptions = ['Bonifico', 'Carta di Credito', 'PayPal', 'Contanti']

const refForm = ref<VForm>()

const onSubmit = () => {
  refForm.value?.validate().then(({ valid: isValid }) => {
    if (isValid && value.value !== null) {
      emit('submit', {
        date: date.value,
        value: value.value,
        status: status.value,
        tipoPagamento: tipoPagamento.value,
      })
      closeDialog()
    }
  })
}

const date = ref(new Date())

const closeDialog = () => {
  emit('update:isDialogVisible', false)
  // Reset form? Optional
  value.value = null
  status.value = ''
  tipoPagamento.value = ''
  nextTick(() => {
    refForm.value?.resetValidation()
  })
}
</script>

<template>
  <VDialog
    :width="$vuetify.display.smAndDown ? 'auto' : 900 "
    :model-value="props.isDialogVisible"
    max-width="600"
    @update:model-value="emit('update:isDialogVisible', $event)"
  >
    <VCard class="pa-sm-11 pa-3">
      <VCardText class="pt-5">
        <div class="text-center pb-6">
          <h4 class="text-h4 mb-2">
            Aggiungi pagamento
          </h4>
        </div>
        <VForm ref="refForm" @submit.prevent>
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
                :config="{ mode: 'single' , format: 'dd/MM/yyyy' }"
                :rules="[requiredValidator]"
              />
            </VCol>
          </VRow>
        </VForm>
      </VCardText>

      <VCardActions>
        <VSpacer />
        <VBtn
          color="secondary"
          variant="tonal"
          @click="closeDialog"
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
  </VDialog>
</template>
