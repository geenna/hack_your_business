<script setup lang="ts">
import AddPaymentDialogContent from './AddPaymentDialogContent.vue'

interface Props {
  isDialogVisible: boolean
}

interface Emits {
  (e: 'update:isDialogVisible', val: boolean): void
  (e: 'submit', data: { date: any; value: number; status: string; tipoPagamento: string }): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const closeDialog = () => {
  emit('update:isDialogVisible', false)
}

const onSubmit = (data: { date: any; value: number; status: string; tipoPagamento: string }) => {
  emit('submit', data)
  closeDialog()
}
</script>

<template>
  <VDialog
    :width="$vuetify.display.smAndDown ? 'auto' : 900"
    :model-value="props.isDialogVisible"
    max-width="600"
    @update:model-value="emit('update:isDialogVisible', $event)"
  >
    <AddPaymentDialogContent
      @submit="onSubmit"
      @cancel="closeDialog"
    />
  </VDialog>
</template>
