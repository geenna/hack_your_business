<script setup lang="ts">
import { ref, watch, inject } from 'vue'
import ProjectService from '@/services/ProjectService'
import ConfirmDialog from '@/components/dialogs/ConfirmDialog.vue'

const isVisible = defineModel<boolean>('isDrawerOpen', { required: true })
const refreshProjects = inject('refreshProjects') as () => void
const emit = defineEmits(['refresh'])

const localProject = ref<any>({
    projectName: '',
    descrizioneProgetto: '',
    datInizio: '',
    datFine: '',
    stato: 'PENDING',
    avanzamento: 0,
    costo: 0
})

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
  if (newVal) {
    // Reset form on open
    localProject.value = {
        projectName: '',
        descrizioneProgetto: '',
        datInizio: undefined,
        datFine: undefined,
        stato: 'PENDING',
        avanzamento: 0,
        costo: 0
    }
  }
})

const onSaveClick = () => {
    // Basic validation could go here
    if (!localProject.value.projectName) {
        // Show error? For now just return or let basic html5 validation handle it if used
        return
    }
    isConfirmDialogVisible.value = true
}

const onConfirmSave = async (confirmed: boolean) => {
    if (confirmed) {
        isSaving.value = true
        try {
            await ProjectService.createProject(localProject.value)
            refreshProjects()
            isVisible.value = false
        } catch (error) {
            console.error("Error creating project:", error)
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
    <VCard title="Crea Progetto">
      <VCardText>
        <VRow>
            <VCol cols="12">
                <VTextField
                    v-model="localProject.projectName"
                    label="Nome Progetto"
                    :rules="[v => !!v || 'Il nome è obbligatorio']"
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
          Crea
        </VBtn>
      </VCardActions>
    </VCard>

    <ConfirmDialog
      v-model:isDialogVisible="isConfirmDialogVisible"
      confirmation-question="Sei sicuro di voler creare questo progetto?"
      confirm-title="Creato!"
      confirm-msg="Il progetto è stato creato con successo."
      cancel-title="Annullato"
      cancel-msg="Creazione annullata."
      @confirm="onConfirmSave"
    />
  </VDialog>
</template>
