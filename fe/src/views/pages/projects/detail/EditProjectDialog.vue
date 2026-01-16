<script setup lang="ts">
import { ref, watch, inject } from 'vue'
import { ProjectFull } from '@/types/UserToProjectSchema'
import ProjectService from '@/services/ProjectService'
import ConfirmDialog from '@/components/dialogs/ConfirmDialog.vue'

const isVisible = defineModel<boolean>('isDrawerOpen', { required: true })
const project = inject('projectSelected') as Ref<ProjectFull>
const refreshProjects = inject('refreshProjects') as () => void
const emit = defineEmits(['refresh'])

const localProject = ref<Partial<ProjectFull>>({})

const isConfirmDialogVisible = ref(false)
const isSaving = ref(false)

const statusOptions = [
  'IN_PROGRESS',
  'COMPLETED',
  'EXPIRING',
  'EXPIRED',
  'PENDING'
]

watch(() => isVisible.value, (newVal) => {
  if (newVal && project.value) {
    localProject.value = {
      ...project.value,
      datInizio: project.value.datInizio ? new Date(project.value.datInizio).toISOString().split('T')[0] : undefined,
      datFine: project.value.datFine ? new Date(project.value.datFine).toISOString().split('T')[0] : undefined,
    }
  }
})

const onSaveClick = () => {
    isConfirmDialogVisible.value = true
}

const onConfirmSave = async (confirmed: boolean) => {
    if (confirmed) {
        isSaving.value = true
        try {
            await ProjectService.updateProject(project.value.id, localProject.value)
            refreshProjects()
            isVisible.value = false
        } catch (error) {
            console.error("Error updating project:", error)
        } finally {
            isSaving.value = false
        }
    }
}

</script>

<template>
  <VDialog
    v-model="isVisible"
    max-width="600"
  >
    <VCard title="Modifica Progetto">
      <VCardText>
        <VRow>
            <VCol cols="12">
                <VTextField
                    v-model="localProject.projectName"
                    label="Nome Progetto"
                />
            </VCol>
            <VCol cols="12">
                <VTextarea
                    v-model="localProject.descrizioneProgetto"
                    label="Descrizione"
                    rows="3"
                />
            </VCol>
            <VCol cols="12" md="6">
                <VTextField
                    v-model="localProject.datInizio"
                    label="Data Inizio"
                    type="date"
                />
            </VCol>
            <VCol cols="12" md="6">
                <VTextField
                    v-model="localProject.datFine"
                    label="Data Fine"
                    type="date"
                />
            </VCol>
            <VCol cols="12" md="6">
                <VSelect
                    v-model="localProject.stato"
                    :items="statusOptions"
                    label="Stato"
                />
            </VCol>
            <VCol cols="12" md="6">
                <VTextField
                    v-model.number="localProject.avanzamento"
                    label="Avanzamento (%)"
                    type="number"
                    min="0"
                    max="100"
                />
            </VCol>
            <VCol cols="12" md="6">
                <VTextField
                    v-model.number="localProject.costo"
                    label="Costo (€)"
                    type="number"
                />
            </VCol>
        </VRow>
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
          @click="onSaveClick"
        >
          Salva
        </VBtn>
      </VCardActions>
    </VCard>

    <ConfirmDialog
      v-model:isDialogVisible="isConfirmDialogVisible"
      confirmation-question="Sei sicuro di voler salvare le modifiche?"
      confirm-title="Salvato!"
      confirm-msg="Le modifiche al progetto sono state salvate."
      cancel-title="Annullato"
      cancel-msg="Salvataggio annullato."
      @confirm="onConfirmSave"
    />
  </VDialog>
</template>
