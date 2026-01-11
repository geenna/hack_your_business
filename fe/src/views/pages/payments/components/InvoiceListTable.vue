<template>
  <VCard title="Lista pagamenti" class="mt-6">
     <template #append>
        <VContainer width="300" fluid class="ma-0">
            <AppDateTimePicker
                v-model="dateRange"
                label="Periodo"
                placeholder="Seleziona periodo"
                :config="{ mode: 'range'}"
                
            />
        </VContainer>
      
      <VBtn
        size="small"
        prepend-icon="ri-add-line"
        @click="isAddPaymentDialogVisible = true"
      >
        Aggiungi pagamento
      </VBtn>
    </template>
    <VCardText>
        <VDataTable
        :headers="headers"
        :items="invoices"
        :loading="isLoading"
        class="text-no-wrap"
        >
        <template #item.date="{ item }">
            {{ new Date(item.date).toLocaleDateString() }}
        </template>

        <template #item.status="{ item }">
            <VChip
              :color="resolveUserStatusVariant(item.status)"
              size="small"
            >
              {{ item.status }}
            </VChip>
        </template>

        <template #item.value="{ item }">
            {{ item.value.toFixed(2) }} €
        </template>
        <template #item.actions="{ item }">
            <IconBtn @click="deletePayment(item.id)" size="x-small">
                <VIcon
                    icon="ri-delete-bin-line"
                    size="20"
                />
            </IconBtn>
        </template>
        </VDataTable>
    </VCardText>

  </VCard>

  <AddPaymentDialog
    v-model:is-dialog-visible="isAddPaymentDialogVisible"
    @submit="onPaymentSubmit"
  />
</template>

<script setup lang="ts">
import { inject } from 'vue'
import PaymentService from '@/services/PaymentService'
import type { Invoice } from '@/types/Invoice'
import type { UserDetail } from '@/types/UserProperties'
import { Italian } from 'flatpickr/dist/l10n/it.js'
import AddPaymentDialog from './AddPaymentDialog.vue'
import { useConfirm } from '@/shared/state/confirm'

const { show: showConfirm } = useConfirm()
const invoices = ref<Invoice[]>([])
const isLoading = ref(false)
const isAddPaymentDialogVisible = ref(false)
const userData = inject('userData') as Ref<UserDetail | undefined>

const formatDate = (date: Date) => date.toISOString().split('T')[0]

const today = new Date()
const ninetyDaysAgo = new Date()
ninetyDaysAgo.setDate(today.getDate() - 90)

const dateRange = ref(`${formatDate(ninetyDaysAgo)} to ${formatDate(today)}`)

const onPaymentSubmit = async (paymentData: any) => {
  try {
    paymentData.userId = userData.value?.id
    await PaymentService.createPayment({
      ...paymentData
    })
    fetchInvoices()
  } catch (error) {
    console.error('Failed to create payment:', error)
  }
}

const deletePayment = async (id: string) => {
    const confirmed = await showConfirm(
        'Eliminazione pagamento',
        `Sei sicuro di voler eliminare il pagamento?`
    )

    if (confirmed) {
        try {
            await PaymentService.deletePayment(id)
            fetchInvoices()
        } catch (error) {
            console.error('Failed to delete payment:', error)
        }
    }
}

const headers = [
  { title: 'ID', key: 'paymentId' },
  { title: 'Stato', key: 'status' },
  { title: 'Tipo', key: 'tipoPagamento' },
  { title: 'Valore', key: 'value' },
  { title: 'Data', key: 'date' },
  { title: 'Azioni', key: 'actions' },
]

const fetchInvoices = async () => {
  if (!userData.value?.id) return

  isLoading.value = true
  try {
    const [startStr, endStr] = dateRange.value.split(' to ')
    const fromDate = startStr ? new Date(startStr) : new Date()
    const toDate = endStr ? new Date(endStr) : new Date(fromDate)

    // Set toDate to end of day
    toDate.setHours(23, 59, 59, 999)

    const response = await PaymentService.getUserPayments(
      userData.value.id,
      fromDate.toISOString(),
      toDate.toISOString()
    )
    invoices.value = response.data
  }
  catch (error) {
    console.error('Error fetching invoices:', error)
  }
  finally {
    isLoading.value = false
  }
}

watch(userData, () => {
    if (userData.value?.id && invoices.value.length === 0) {
        fetchInvoices()
    }
})

watch(dateRange, () => {
    if (dateRange.value.includes(' to ')) {
        fetchInvoices()
    }
})

onMounted(() => {
  fetchInvoices()
})

const resolveUserStatusVariant = (role: string) => {
    const roleLowerCase = role.toLowerCase()
  
    if (roleLowerCase.toLowerCase() === 'pagato')
        return 'success'
    else if (roleLowerCase.toLowerCase() === 'rifiutato')
        return 'error'
    else if (roleLowerCase.toLowerCase() === 'in attesa')
        return 'primary'
    else if (roleLowerCase.toLowerCase() === 'annullato')
        return 'warning'

    return 'primary'

}


</script>