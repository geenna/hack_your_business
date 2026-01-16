<script setup lang="ts">
import { ref, inject, watch, onMounted } from 'vue'
import UserService from '@/services/UserService'
import ProjectService from '@/services/ProjectService'
import { ProjectFull } from '@/types/UserToProjectSchema'

const isVisible = defineModel<boolean>('isDrawerOpen', { required: true })
const project = inject('projectSelected') as Ref<ProjectFull>
const emit = defineEmits(['refresh'])

const users = ref<any[]>([])
const selectedUserIds = ref<string[]>([])
const isLoading = ref(false)
const isSaving = ref(false)

const fetchUsers = async () => {
    isLoading.value = true
    try {
        const response = await UserService.getCollaborators()
        users.value = response.data
    } catch (error) {
        console.error("Error fetching users:", error)
    } finally {
        isLoading.value = false
    }
}

watch(isVisible, (newVal) => {
    if (newVal) {
        fetchUsers()
        selectedUserIds.value = [] // Reset selection
    }
})

const onSave = async () => {
    if (selectedUserIds.value.length === 0) {
        isVisible.value = false
        return
    }

    isSaving.value = true
    try {
      debugger;
        await ProjectService.addCollaborators(project.value.id, selectedUserIds.value)
        emit('refresh')
        isVisible.value = false
    } catch (error) {
        console.error("Error adding collaborators:", error)
        // Optionally show error toast
    } finally {
        isSaving.value = false
    }
}
</script>

<template>
  <VDialog
    v-model="isVisible"
    max-width="600"
  >
    <VCard title="Aggiungi Collaboratore">
      <VCardText>
        <div v-if="isLoading" class="d-flex justify-center align-center py-4">
            <VProgressCircular indeterminate color="primary" />
        </div>
        <div v-else-if="users.length === 0" class="text-center py-4">
            Nessun collaboratore trovato.
        </div>
        <VList v-else select-strategy="leaf">
            <VListItem
                v-for="user in users"
                :key="user.id"
                :value="user.id"
            >
                <template v-slot:prepend>
                    <VCheckbox
                        v-model="selectedUserIds"
                        :value="user.id"
                    ></VCheckbox>
                </template>
                <VListItemTitle>{{ user.nome }} {{ user.cognome }}</VListItemTitle>
                <VListItemSubtitle>{{ user.email }}</VListItemSubtitle>
            </VListItem>
        </VList>
      </VCardText>
      <VCardActions>
        <VSpacer />
        <VBtn
          color="error"
          variant="outlined"
          @click="isVisible = false"
        >
          Annulla
        </VBtn>
        <VBtn
          color="success"
          variant="elevated"
          :loading="isSaving"
          @click="onSave"
        >
          Salva
        </VBtn>
      </VCardActions>
    </VCard>
  </VDialog>
</template>
