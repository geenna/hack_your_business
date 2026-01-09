<script setup lang="ts">

import type { UserDetail } from '@/types/UserProperties'

import { useConfirm } from '@/shared/state/confirm'
import { useAlert } from '@/shared/state/alert'
import UserService from '@/services/UserService'
import CreateUserDialog from '../CreateUserDialog.vue'

const { show: showConfirm } = useConfirm()
const { show: showAlert } = useAlert()

const props = defineProps({
  userData: {
    type: Object as PropType<UserDetail>,
    required: true,
  },
})

const onSuspend = async () => {
    const confirmed = await showConfirm(
        'Sospensione Utente',
        `Sei sicuro di voler sospendere l'utente ${props.userData.nome} ${props.userData.cognome}?`
    )

    if (confirmed) {
        try {
            await UserService.suspendUser(props.userData.id)
            props.userData.user_status = 'DISATTIVO'
            showAlert('Successo', 'Utente sospeso con successo', 'success')
        } catch (error) {
            // Error is handled by global interceptor, but we can catch specific logic here if needed
        }
    }
}

const onActivate = async () => {
    const confirmed = await showConfirm(
        'Attivazione Utente',
        `Sei sicuro di voler attivare l'utente ${props.userData.nome} ${props.userData.cognome}?`
    )

    if (confirmed) {
        try {
            await UserService.activateUser(props.userData.id)
            props.userData.user_status = 'ATTIVO'
            showAlert('Successo', 'Utente attivato con successo', 'success')
        } catch (error) {
            // Error is handled by global interceptor, but we can catch specific logic here if needed
        }
    }
}

const standardPlan = {
  plan: 'Standard',
  price: 99,
  benefits: [
    '10 Users',
    'Up to 10GB storage',
    'Basic Support',
  ],
}

const isUserInfoEditDialogVisible = ref(false)
const isUpgradePlanDialogVisible = ref(false)

const onUserUpdate = async (updatedUser: any) => {
    Object.assign(props.userData, updatedUser)
    showAlert('Successo', 'Dati utente aggiornati con successo', 'success')
}

const resolveUserStatusVariant = (stat: string) => {
  if (stat === 'pending')
    return 'warning'
  if (stat === 'ATTIVO')
    return 'success'
  if (stat === 'DISATTIVO')
    return 'secondary'
  
  return 'primary'
}



const resolveUserRoleVariant = (role: string) => {

  if (role === 'cliente')
    return { color: 'success', icon: 'ri-user-line' }
  if (role === 'collaboratore')
    return { color: 'info', icon: 'ri-pie-chart-line' }
  if (role === 'admin')
    return { color: 'primary', icon: 'ri-vip-crown-line' }

  return { color: 'success', icon: 'ri-user-line' }
}
</script>

<template>
  <VRow>
    <!-- SECTION User Details -->
    <VCol cols="12">
      <VCard v-if="props.userData">
        <VCardText class="text-center pt-12 pb-6">
          <!-- 👉 Avatar -->
          <VAvatar
            rounded
            :size="120"
            :color="!props.userData.avatar ? 'primary' : undefined"
            :variant="!props.userData.avatar ? 'tonal' : undefined"
          >
            <VImg
              v-if="props.userData.avatar"
              :src="props.userData.avatar"
            />
            <span
              v-else
              class="text-5xl font-weight-medium"
            >
              {{ avatarText(props.userData.nome) }}
            </span>
          </VAvatar>

          <!-- 👉 User fullName -->
          <h5 class="text-h5 mt-4">
            {{ props.userData.nome }} {{ props.userData.cognome }}
          </h5>

            <!-- 👉 Role chip -->
          <VChip
            :color="resolveUserRoleVariant(props.userData.userType).color"
            size="small"
            class="text-capitalize mt-4"
          >
            {{ props.userData.userType }}
          </VChip>
        </VCardText>


        <!-- 👉 Details -->
        <VCardText class="pb-6">
          <h5 class="text-h5">
            Details
          </h5>

          <VDivider class="my-4" />

          <!-- 👉 User Details list -->
          <VList class="card-list">
        
            <VListItem>
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                    Email:
                </span>
                <span class="text-body-1">{{ props.userData.email }}</span>
              </VListItemTitle>
            </VListItem>

            <VListItem>
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                  Stato:
                </span>
                <VChip
                  size="small"
                  :color="resolveUserStatusVariant(props.userData.user_status)"
                  class="text-capitalize"
                >
                  {{ props.userData.user_status }}
                </VChip>
              </VListItemTitle>
            </VListItem>
            <VListItem>
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                  Codice Fiscale:
                </span>
                <span class="text-body-1">
                  {{ props.userData.cf }}
                </span>
              </VListItemTitle>
            </VListItem>

            <VListItem>
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                  Indirizzo:
                </span>
                <span class="text-body-1">
                  {{ props.userData.indirizzoResidenza }}
                </span>
              </VListItemTitle>
            </VListItem>

            <VListItem>
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                  Città:
                </span>
                <span class="text-body-1">
                  {{ props.userData.citta }} ({{ props.userData.prov }}) - {{ props.userData.cap }}
                </span>
              </VListItemTitle>
            </VListItem>

            <VListItem v-if="props.userData.regioneSociale">
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                  Ragione Sociale:
                </span>
                <span class="text-body-1">
                  {{ props.userData.regioneSociale }}
                </span>
              </VListItemTitle>
            </VListItem>

            <VListItem v-if="props.userData.piva">
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                  P.IVA:
                </span>
                <span class="text-body-1">
                  {{ props.userData.piva }}
                </span>
              </VListItemTitle>
            </VListItem>

            <VListItem>
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                   Telefono:
                </span>
                <span class="text-body-1">
                  {{ props.userData.telefono }}
                </span>
              </VListItemTitle>
            </VListItem>
          </VList>
        </VCardText>

        <!-- 👉 Edit and Suspend button -->
        <VCardText class="d-flex justify-center">
          <VBtn
            variant="elevated"
            class="me-4"
            @click="isUserInfoEditDialogVisible = true"
          >
            Modifica
          </VBtn>
          <VBtn
            v-if="props.userData.user_status === 'ATTIVO'"
            variant="outlined"
            color="error"
            @click="onSuspend"
          >
            Sospendi
          </VBtn>
          <VBtn
            v-if="props.userData.user_status === 'DISATTIVO'"
            variant="outlined"
            color="success"
            @click="onActivate"
          >
            Attiva
          </VBtn>
        </VCardText>
      </VCard>
    </VCol>
    <!-- !SECTION -->

    <!-- !SECTION -->

    
  </VRow>

  <CreateUserDialog
    v-model:is-dialog-visible="isUserInfoEditDialogVisible"
    :user-data="props.userData"
    @submit="onUserUpdate"
  />


</template>

<style lang="scss" scoped>
.card-list {
  --v-card-list-gap: 0.5rem;
}

.current-plan {
  border: 2px solid rgb(var(--v-theme-primary));
}

.text-capitalize {
  text-transform: capitalize !important;
}
</style>
