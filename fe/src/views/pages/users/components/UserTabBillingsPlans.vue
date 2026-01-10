<script setup lang="ts">
import { UserDetail } from '@/types/UserProperties'
import { BillingAddress } from '@/types/BillingAddress'
import { useAlert } from '@/shared/state/alert'
import PaymentService from '@/services/PaymentService'
import InvoiceListTable from '@/views/pages/payments/components/InvoiceListTable.vue'

const { show: showAlert } = useAlert()

const isEditAddressDialogVisible = ref(false)
const userData = inject('userData') as Ref<UserDetail | undefined>
const billingAddress = ref<BillingAddress | undefined>(userData.value?.billing_address)

watch(userData, () => {
  billingAddress.value = userData.value?.billing_address
}, { immediate: true })

const onAddressSubmit = async (addressData: BillingAddress) => {
  try {
    const updatedAddress = await PaymentService.saveBillingAddress(addressData)
    // Update local state
    billingAddress.value = updatedAddress.data
    // Update injected userData if possible (it's a ref so it should propagate if we mutate value)
    if (userData.value) {
      userData.value.billing_address = updatedAddress.data
    }
    showAlert('Successo', 'Indirizzo di fatturazione aggiornato con successo', 'success')
  } catch (error) {
    console.error('Failed to save billing address:', error)
    // Alert is handled by interceptor usually, but safe to log
  }
}

</script>

<template>
  <VRow>
    <VCol cols="12">
      <!-- 👉 Billing Address -->
      <VCard title="Indirizzo di fatturazione">
        <template #append>
          <VBtn
            size="small"
            prepend-icon="ri-add-line"
            @click="isEditAddressDialogVisible = !isEditAddressDialogVisible"
          >
            Modifica Indirizzo
          </VBtn>
        </template>

        <VCardText>
          <VRow>
            <VCol
              cols="12"
              lg="6"
            >
              <VTable class="billing-address-table">
                <tr>
                  <td>
                    <h6 class="text-h6 text-no-wrap mb-2">
                      Nome Azienda:
                    </h6>
                  </td>
                  <td>
                    <p class="text-body-1 mb-2">
                      {{ billingAddress?.regSociale }}
                    </p>
                  </td>
                </tr>

                <tr>
                  <td>
                    <h6 class="text-h6 text-no-wrap mb-2">
                      Cf / Partita iva:
                    </h6>
                  </td>
                  <td>
                    <p class="text-body-1 mb-2">
                      {{ billingAddress?.piva ?? userData?.cf }}
                    </p>
                  </td>
                </tr>
               
                <tr>
                  <td class="d-flex align-baseline">
                    <h6 class="text-h6 text-no-wrap">
                      Indirizzo:
                    </h6>
                  </td>
                  <td>
                    <p class="text-body-1 mb-0">
                      {{ billingAddress?.address ?? userData?.indirizzoResidenza }}
                    </p>
                  </td>
                </tr>
              </VTable>
            </VCol>

            <VCol
              cols="12"
              lg="6"
            >
              <VTable class="billing-address-table">
                <tr>
                  <td>
                    <h6 class="text-h6 text-no-wrap mb-2">
                      Telefono:
                    </h6>
                  </td>
                  <td>
                    <p class="text-body-1 mb-2">
                      {{ userData?.telefono }}
                    </p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <h6 class="text-h6 text-no-wrap mb-2">
                      Citta:
                    </h6>
                  </td>
                  <td>
                    <p class="text-body-1 mb-2">
                     {{ billingAddress?.city ?? userData?.citta }} ({{ billingAddress?.prov ?? userData?.prov }})
                    </p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <h6 class="text-h6 text-no-wrap mb-2">
                      Stato:
                    </h6>
                  </td>
                  <td>
                    <p class="text-body-1 mb-2">
                      {{ billingAddress?.stato ?? userData?.stato }}
                    </p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <h6 class="text-h6 text-no-wrap">
                      Zip Code:
                    </h6>
                  </td>
                  <td>
                    <p class="text-body-1 mb-0">
                      {{ billingAddress?.cap ?? userData?.cap }}
                    </p>
                  </td>
                </tr>
              </VTable>
            </VCol>
          </VRow>
        </VCardText>
      </VCard>
    </VCol>
  </VRow>

  <InvoiceListTable />

  <!-- 👉 Edit Address dialog -->

  <AddEditAddressDialog
    v-model:is-dialog-visible="isEditAddressDialogVisible"
    @submit="onAddressSubmit"
  />

</template>

<style lang="scss">
.billing-address-table {
  tr {
    td:first-child {
      inline-size: 148px;
    }
  }
}
</style>
