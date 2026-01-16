<script setup lang="ts">

import { inject, type Ref } from 'vue'
import type { ProjectFull } from '@/types/UserToProjectSchema'

import { useConfirm } from '@/shared/state/confirm'
import { useAlert } from '@/shared/state/alert'
import AvanzamentoRadialGraph from './AvanzamentoRadialGraph.vue'
import EditProjectDialog from './EditProjectDialog.vue'
import ConfirmDialog from '@/components/dialogs/ConfirmDialog.vue'
import ProjectService from '@/services/ProjectService';


const { show: showConfirm } = useConfirm()
const { show: showAlert } = useAlert()

const project :Ref<ProjectFull> = inject('projectSelected') as Ref<ProjectFull>
const refreshProjects = inject('refreshProjects') as () => void

const isEditDialogVisible = ref(false)
const isConfirmDeleteDialogVisible = ref(false)
const isDeleting = ref(false)

const emit = defineEmits(['refresh'])

const onConfirmDelete = async (confirmed: boolean) => {
    if (confirmed) {
        isDeleting.value = true
        try {
            await ProjectService.deleteProject(project.value.id)
            // Emit refresh or navigate away. Ideally navigate away as the project is deleted.
            // Since this component is part of a list/detail view managed by main.vue, maybe we should emit an event.
            // But looking at the user request "Al click su conferma puoi procedere all'eliminazione".
            // After deletion, we probably want to go back to the list.
            // main.vue listens to @openDetailProject to switch tab.
            // We can reload the page or emit an event to parent to return to list.
            // Let's assume re-fetching projects will handle it or I can force a refresh.
            // However, simply refreshing projects won't switch the tab back to 0.
            // The user didn't specify what to do after delete only "procedere all'eliminazione".
            // I'll emit 'refresh' and reload the page or just reload the window for now to be safe and simple
            // But wait, ProjectFullDetail emits 'onBack'. Maybe I can emit that?
            // ProjectFullOverview is a child of ProjectFullDetail.
            // ProjectFullDetail doesn't listen to ProjectFullOverview events for navigation.
            // I will just reload the page for now as it ensures state is clean.
            // Actually, a cleaner way is to use window.location.reload() or refresh projects and unset selection.
            window.location.reload()
        } catch (error) {
            console.error("Error deleting project:", error)
        } finally {
            isDeleting.value = false
        }
    }
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
          <VBtn class="me-2" color="primary" @click="isEditDialogVisible = true">Modifica</VBtn>
          <VBtn class="ms-2" color="error" @click="isConfirmDeleteDialogVisible = true">Elimina</VBtn>
        </VCardText>
      </VCard>
    </VCol>


    
  </VRow>

  <EditProjectDialog v-model:isDrawerOpen="isEditDialogVisible" />
  
  <ConfirmDialog
    v-model:isDialogVisible="isConfirmDeleteDialogVisible"
    confirmation-question="Sei sicuro di voler eliminare questo progetto?"
    confirm-title="Eliminato!"
    confirm-msg="Il progetto è stato eliminato con successo."
    cancel-title="Annullato"
    cancel-msg="Eliminazione annullata."
    @confirm="onConfirmDelete"
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
