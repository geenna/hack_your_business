<script setup lang="ts">

import type { UserDetail } from '@/types/UserProperties'

import { useConfirm } from '@/shared/state/confirm'
import { useAlert } from '@/shared/state/alert'
import UserService from '@/services/UserService'
import CreateUserDialog from '../CreateUserDialog.vue'

const { show: showConfirm } = useConfirm()
const { show: showAlert } = useAlert()

const userData :UserDetail = inject('userData') as UserDetail

const onSuspend = async () => {
    const confirmed = await showConfirm(
        'Sospensione Utente',
        `Sei sicuro di voler sospendere l'utente ${userData.nome} ${userData.cognome}?`
    )

    if (confirmed) {
        try {
            await UserService.suspendUser(userData.id)
            userData.user_status = 'DISATTIVO'
            showAlert('Successo', 'Utente sospeso con successo', 'success')
        } catch (error) {
            // Error is handled by global interceptor, but we can catch specific logic here if needed
        }
    }
}

const onActivate = async () => {
    const confirmed = await showConfirm(
        'Attivazione Utente',
        `Sei sicuro di voler attivare l'utente ${userData.nome} ${userData.cognome}?`
    )

    if (confirmed) {
        try {
            await UserService.activateUser(userData.id)
            userData.user_status = 'ATTIVO'
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
    Object.assign(userData, updatedUser)
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
      <VCard v-if="userData">
        <VCardText class="text-center pt-12 pb-6">
          <!-- 👉 Avatar -->
          <VAvatar
            rounded
            :size="120"
            :color="!userData.avatar ? 'primary' : undefined"
            :variant="!userData.avatar ? 'tonal' : undefined"
          >
            <VImg
              v-if="userData.avatar"
              :src="userData.avatar"
            />
            <span
              v-else
              class="text-5xl font-weight-medium"
            >
              {{ avatarText(userData.nome) }}
            </span>
          </VAvatar>

          <!-- 👉 User fullName -->
          <h5 class="text-h5 mt-4">
            {{ userData.nome }} {{ userData.cognome }}
          </h5>

            <!-- 👉 Role chip -->
          <VChip
            :color="resolveUserRoleVariant(userData.userType).color"
            size="small"
            class="text-capitalize mt-4"
          >
            {{ userData.userType }}
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
                <span class="text-body-1">{{ userData.email }}</span>
              </VListItemTitle>
            </VListItem>

            <VListItem>
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                  Stato:
                </span>
                <VChip
                  size="small"
                  :color="resolveUserStatusVariant(userData.user_status)"
                  class="text-capitalize"
                >
                  {{ userData.user_status }}
                </VChip>
              </VListItemTitle>
            </VListItem>
            <VListItem>
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                  Codice Fiscale:
                </span>
                <span class="text-body-1">
                  {{ userData.cf }}
                </span>
              </VListItemTitle>
            </VListItem>

            <VListItem>
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                  Indirizzo:
                </span>
                <span class="text-body-1">
                  {{ userData.indirizzoResidenza }}
                </span>
              </VListItemTitle>
            </VListItem>

            <VListItem>
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                  Città:
                </span>
                <span class="text-body-1">
                  {{ userData.citta }} ({{ userData.prov }}) - {{ userData.cap }}
                </span>
              </VListItemTitle>
            </VListItem>

            <VListItem v-if="userData.regioneSociale">
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                  Ragione Sociale:
                </span>
                <span class="text-body-1">
                  {{ userData.regioneSociale }}
                </span>
              </VListItemTitle>
            </VListItem>

            <VListItem v-if="userData.piva">
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                  P.IVA:
                </span>
                <span class="text-body-1">
                  {{ userData.piva }}
                </span>
              </VListItemTitle>
            </VListItem>

            <VListItem>
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                   Telefono:
                </span>
                <span class="text-body-1">
                  {{ userData.telefono }}
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
            v-if="userData.user_status === 'ATTIVO'"
            variant="outlined"
            color="error"
            @click="onSuspend"
          >
            Sospendi
          </VBtn>
          <VBtn
            v-if="userData.user_status === 'DISATTIVO'"
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
    :user-data="userData"
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
