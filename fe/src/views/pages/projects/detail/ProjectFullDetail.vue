<script setup lang="ts">


import { inject, ref } from 'vue'
import ProjectFullOverview from './ProjectFullOverview.vue'
import { ProjectFull } from '@/types/UserToProjectSchema'
import UserAllowedList from './UserAllowedList.vue'
import AggiungiCollaboratoreDialog from './AggiungiCollaboratoreDialog.vue'
import AggiungiDocumentoDialog from './AggiungiDocumentoDialog.vue'

const project :Ref<ProjectFull> = inject('projectSelected') as Ref<ProjectFull>  




const projectTab = ref(null)
const isAddCollaboratorDialogOpen = ref(false)
const isAddDocumentDialogOpen = ref(false)

const refreshProjects = inject('refreshProjects') as () => void

const emit = defineEmits(['onBack'])

const tabs = [
  {
    icon: 'ri-group-line',
    title: 'Overview',
  }
]
</script>

<template>
  <VBtn variant="text" @click="emit('onBack', false)">Indietro</VBtn>
  <VRow class="mt-6">
    <VCol
      cols="12"
      md="5"
      lg="4"
    >
      <ProjectFullOverview />
    </VCol>

    <VCol
      cols="12"
      md="7"
      lg="8"
    >
      <VTabs
        v-model="projectTab"
       
      >
        <VTab
          v-for="tab in tabs"
          :key="tab.icon"
        >
          <VIcon
            start
            :icon="tab.icon"
          />
          <span>{{ tab.title }}</span>
        </VTab>
      </VTabs>

      <VWindow
        v-model="projectTab"
        class="mt-6 disable-tab-transition"
        :touch="false"
      >
        <VWindowItem>

          <VCard>
            <VCardTitle>{{ project.projectName }}</VCardTitle>
            <VCardText>
              {{ project.descrizioneProgetto }}
            </VCardText>
          </VCard>
          
          
          <VCard class="mt-6" title="Utenti">
            <template #append>
              <VBtn
                size="small"
                prepend-icon="ri-add-line"
                @click="isAddCollaboratorDialogOpen = true"
              >
                Aggiungi collaboratore
              </VBtn>
            </template>
            <VCardText>
              <UserAllowedList />
            </VCardText>
          </VCard>



          <VCard class="mt-6" title="Documenti">
            <template #append>
              <VBtn
                size="small"
                prepend-icon="ri-add-line"
                @click="isAddDocumentDialogOpen = true"
              >
                Aggiungi documento
              </VBtn>
            </template>
            <VCardText>
              {{ project.descrizioneProgetto }}
            </VCardText>
          </VCard>
        </VWindowItem>
      </VWindow>
    </VCol>
  </VRow>

  <AggiungiCollaboratoreDialog v-model:isDrawerOpen="isAddCollaboratorDialogOpen" @refresh="refreshProjects" />
  <AggiungiDocumentoDialog v-model:isDrawerOpen="isAddDocumentDialogOpen" />
</template>
