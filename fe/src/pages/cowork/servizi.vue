<script lang="ts" setup>
import { ref, Ref } from 'vue'
import type { ServiziModel } from '@/types/ServiziModel'
import CoWorkingService from '@/services/CoWorkingService'

const isDialogVisible = ref(false)
const isDeleteDialogVisible = ref(false)
const isEditMode = ref(false)
const pendingDeleteId = ref<string | null>(null)

const formServizio = ref<ServiziModel>({
  id: '',
  nome: '',
  key: '',
  costoIntero: 0,
  costoRidotto: 0,
})

const resetForm = () => {
  formServizio.value = {
    id: '',
    nome: '',
    key: '',
    costoIntero: 0,
    costoRidotto: 0,
  }
}

const aggiungiServizio = () => {
  isEditMode.value = false
  resetForm()
  isDialogVisible.value = true
}

const eliminaServizio = (id: string) => {
  pendingDeleteId.value = id
  isDeleteDialogVisible.value = true
}

const modificaServizio = (servizio: ServiziModel) => {
  isEditMode.value = true
  formServizio.value = { ...servizio }
  isDialogVisible.value = true
}

const annullaDialog = () => {
  resetForm()
  isDialogVisible.value = false
}

const salvaServizio = async () => {
  try {
    await CoWorkingService.upsertServizio({
      ...formServizio.value,
      id: formServizio.value.id || '',
    })
    await loadServizi()
    annullaDialog()
  } catch (error) {
    console.error('Errore salvataggio servizio:', error)
  }
}

const loadServizi = async () => {
  try {
    const response = await CoWorkingService.getServizi()
    servizi.value = response.data
  } catch (error) {
    console.error('Errore caricamento servizi:', error)
    servizi.value = []
  }
}

const onDeleteConfirm = async (confirmed: boolean) => {
  if (!confirmed) {
    pendingDeleteId.value = null
    return
  }
  if (!pendingDeleteId.value)
    return
  try {
    await CoWorkingService.deleteServizio(pendingDeleteId.value)
    await loadServizi()
  } catch (error) {
    console.error('Errore eliminazione servizio:', error)
  } finally {
    pendingDeleteId.value = null
  }
}

const headers = [
  { title: 'Nome Servizio', key: 'nome' },
  { title: 'Chiave', key: 'key' },
  { title: 'Costo Intero (€)', key: 'costoIntero', width: '200', align:'end' },
  { title: 'Costo Ridotto (€)', key: 'costoRidotto', width: '200', align:'end' },
  { title: 'Azioni', key: 'azioni', width: '150', align: 'center' },
]
const servizi:Ref<ServiziModel[]> = ref<ServiziModel[]>([])

onMounted(() => {
  loadServizi()
})


</script>

<template>

      <VRow>
        <VCol cols="12">
          <VCard title="Documenti">
            <template #append>
              <VBtn
                size="small"
                prepend-icon="ri-add-line"
                @click="aggiungiServizio"
              >
                Aggiungi Servizio
              </VBtn>

            </template>

            <VDataTable
              :headers="headers"
              :items="servizi"
              item-value="name"
              class="rounded-0"
            >
            <template #item.azioni="{ item }">
                <IconBtn size="small" color="error" @click="eliminaServizio(item.id)">
                    <VIcon icon="ri-delete-bin-line" />
                </IconBtn>
                <IconBtn size="small" @click="modificaServizio(item)">
                    <VIcon icon="ri-edit-line" />
                </IconBtn>
             </template>
            </VDataTable>
            <!-- !SECTION -->
          </VCard>
        </VCol>
      </VRow>

      <VDialog
        v-model="isDialogVisible"
        max-width="600"
      >
        <VCard class="pa-4">
          <VCardTitle>
            {{ isEditMode ? 'Modifica servizio' : 'Aggiungi servizio' }}
          </VCardTitle>
          <VCardText>
            <VForm @submit.prevent="salvaServizio">
              <VRow>
                <VCol cols="12">
                  <VTextField
                    v-model="formServizio.nome"
                    label="Nome servizio"
                  />
                </VCol>
                <VCol cols="12">
                  <VTextField
                    v-model="formServizio.key"
                    label="Chiave"
                  />
                </VCol>
                <VCol cols="12" sm="6">
                  <VTextField
                    v-model.number="formServizio.costoIntero"
                    label="Costo intero (€)"
                    type="number"
                  />
                </VCol>
                <VCol cols="12" sm="6">
                  <VTextField
                    v-model.number="formServizio.costoRidotto"
                    label="Costo ridotto (€)"
                    type="number"
                  />
                </VCol>
              </VRow>
            </VForm>
          </VCardText>
          <VCardActions>
            <VSpacer />
            <VBtn
              color="secondary"
              variant="tonal"
              @click="annullaDialog"
            >
              Annulla
            </VBtn>
            <VBtn
              color="primary"
              variant="elevated"
              @click="salvaServizio"
            >
              Salva
            </VBtn>
          </VCardActions>
        </VCard>
      </VDialog>

      <ConfirmDialog
        v-model:is-dialog-visible="isDeleteDialogVisible"
        cancel-title="Annullato"
        confirm-title="Eliminato"
        confirm-msg="Il servizio è stato eliminato."
        confirmation-question="Sei sicuro di voler cancellare il servizio?"
        cancel-msg="Eliminazione annullata."
        @confirm="onDeleteConfirm"
      />
</template>
