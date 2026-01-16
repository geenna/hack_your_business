<script setup lang="ts">
import { ProjectFull } from '@/types/UserToProjectSchema'
import ConfirmDialog from '@/components/dialogs/ConfirmDialog.vue'
import ProjectService from '@/services/ProjectService';
import { inject, ref } from 'vue';


// 👉 Store
const searchQuery = ref('')
const selectedRole = ref()
const project :Ref<ProjectFull> = inject('projectSelected') as Ref<ProjectFull>
const refreshProjects = inject('refreshProjects') as () => void  

// Data table options
const itemsPerPage = ref(10)
const page = ref(1)
const sortBy = ref()
const orderBy = ref()

// Update data table options
const updateOptions = (options: any) => {
  sortBy.value = options.sortBy[0]?.key
  orderBy.value = options.sortBy[0]?.order
}

// Headers
const headers = [
  { title: 'Cognome', key: 'users.cognome' },
  { title: 'Nome', key: 'users.nome' },
  { title: 'Email', key: 'users.email' },
  { title: 'Ruolo', key: 'role' },
  { title: 'Azioni', key: 'actions', sortable: false },
]




// 👉 search filters
const roles = [
  { title: 'Amministratore', value: 'admin' },
  { title: 'Collaboratore', value: 'collaboratore' },
  { title: 'Cliente', value: 'cliente' },
]

const status = [
  { title: 'Attivo', value: 'active' },
  { title: 'Disattivo', value: 'inactive' },
]

const resolveUserRoleVariant = (role: string) => {
  const roleLowerCase = role.toLowerCase()

  if (roleLowerCase === 'cliente')
    return { color: 'success', icon: 'ri-user-line' }
  if (roleLowerCase === 'collaboratore')
    return { color: 'info', icon: 'ri-pie-chart-line' }
  if (roleLowerCase === 'admin')
    return { color: 'primary', icon: 'ri-vip-crown-line' }

  return { color: 'success', icon: 'ri-user-line' }
}


// 👉 Delete user
// 👉 Delete user
const isConfirmDialogVisible = ref(false)
const userToDelete = ref<{projectId: string, userId: string} | null>(null)

const deleteUser = async (projectId: any, userId: any) => {
  userToDelete.value = { projectId, userId }
  isConfirmDialogVisible.value = true
}

const onConfirmDelete = async (confirmed: boolean) => {
    if (confirmed && userToDelete.value) {
        try {
            await ProjectService.removeRelazioneUtenteProgetto(userToDelete.value.projectId, userToDelete.value.userId)
            refreshProjects()
        } catch (error) {
            console.error("Error removing collaborator:", error)
        }
    }
}




const isUserCreateDialogVisible = ref(false)

</script>

<template>
    <section>
        
        <!-- SECTION datatable -->
        <VDataTable
            no-data-text="Nessun collaboratore trovato"
            hide-default-footer
            :items="project.userToProjects"
            item-value="id"
            :headers="headers"
            class="text-no-wrap rounded-0"
            @update:options="updateOptions"
        >
            <template #item.actions="{ item }">
            <IconBtn
                size="small"
                color="error"
                @click="deleteUser(item.projectId!, item.userId!)"
            >
                <VIcon icon="ri-delete-bin-7-line" />
            </IconBtn>        
            </template>
        </VDataTable>
    </section>

    <ConfirmDialog
      v-model:isDialogVisible="isConfirmDialogVisible"
      confirmation-question="Sei sicuro di voler rimuovere questo collegamento?"
      confirm-title="Eliminato!"
      confirm-msg="la relazione è stata rimossa dal progetto."
      cancel-title="Annullato"
      cancel-msg="Rimozione annullata."
      @confirm="onConfirmDelete"
    />
</template>

<style lang="scss">
.app-user-search-filter {
  inline-size: 24.0625rem;
}

.text-capitalize {
  text-transform: capitalize;
}

.user-list-name:not(:hover) {
  color: rgba(var(--v-theme-on-background), var(--v-high-emphasis-opacity));
}
</style>
