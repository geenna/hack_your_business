<script setup lang="ts">

import { inject, type Ref } from 'vue'
import type { ProjectFull } from '@/types/UserToProjectSchema'

import { useConfirm } from '@/shared/state/confirm'
import { useAlert } from '@/shared/state/alert'
import AvanzamentoRadialGraph from './AvanzamentoRadialGraph.vue'


const { show: showConfirm } = useConfirm()
const { show: showAlert } = useAlert()

const project :Ref<ProjectFull> = inject('projectSelected') as Ref<ProjectFull>  


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
      <VCard>
        <VCardText class="text-center pt-12 pb-6">
          <!-- 👉 Avatar -->
          <AvanzamentoRadialGraph :avanzamento="project.avanzamento ?? 0"/>

            <!-- 👉 Role chip -->
          <VChip
            :color="resolveUserRoleVariant(project.stato!).color"
            size="small"
            class="text-capitalize mt-4"
          >
            {{ project.stato }}
          </VChip>
        </VCardText>

        <!-- 👉 Details -->
        <VCardText class="pb-6 mt-6">
          <h5 class="text-h6">
            Informazioni Progetto
          </h5>

          <VDivider class="my-4" />

          <!-- 👉 User Details list -->
          <VList class="card-list">
            <VListItem>
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                    Data inizio:
                </span>
                <span class="text-body-1">{{ new Date(project.datInizio!).toLocaleDateString() }}</span>
              </VListItemTitle>
            </VListItem>
            <VListItem>
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                    Data fine:
                </span>
                <span class="text-body-1">{{ new Date(project.datFine!).toLocaleDateString() }}</span>
              </VListItemTitle>
            </VListItem>
            <VListItem>
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                    Importo (€):
                </span>
                <span class="text-body-1">{{ project.costo }}</span>
              </VListItemTitle>
            </VListItem>
            <VListItem>
              <VListItemTitle class="text-sm">
                <span class="font-weight-medium">
                    Giorni rimanenti:
                </span>
                <span class="text-body-1">{{ Math.ceil((new Date(project.datFine!).getTime() - new Date(project.datInizio!).getTime()) / (1000 * 60 * 60 * 24)) }}</span>
              </VListItemTitle>
            </VListItem>
          </VList>
        </VCardText>

        <!-- 👉 Edit and Suspend button -->
        <VCardText class="d-flex justify-center">
          <VBtn class="me-2" color="primary">Modifica</VBtn>
          <VBtn class="ms-2" color="error">Elimina</VBtn>
        </VCardText>
      </VCard>
    </VCol>


    
  </VRow>


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
