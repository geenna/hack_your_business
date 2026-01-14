<script setup lang="ts">
import { useTheme } from 'vuetify'
import avatar2 from '@images/avatars/avatar-2.png'

import { ProjectFull } from '@/types/UserToProjectSchema'
const { name } = useTheme()

const props = defineProps<{progetti: ProjectFull[]}>() 
const openDetailDialog = ref(false)

const projectTableHeaders = [
  {
    title: 'Progetto',
    key: 'projectName',
    
  },
  {
    title: 'Data Inizio',
    key: 'datInizio',
    width: '150px'
  },{
    title: 'Data Fine',
    key: 'datFine',
    width: '150px'

  },
  {
    title: '% Completamento',
    key: 'avanzamento',
    align:'center' as const,
    width: '200px'

  },
  {
    title: 'Costo (€)',
    key: 'costo',
    width: '150px',
    align:'end' as const
  },
   {
    title: 'Azioni',
    width: '80px',
    key: 'azioni',
  },
]

const emit = defineEmits(['openDetailProject'])
const openDetailProject = (item: ProjectFull) => {

  emit('openDetailProject', item)
}
const search = ref('')

const resolveUserProgressVariant = (progress:number) => {
  if (progress <= 25)
    return 'error'
  if (progress > 25 && progress <= 50)
    return 'warning'
  if (progress > 50 && progress <= 75)
    return 'primary'
  if (progress > 75 && progress <= 100)
    return 'success'
  
  return 'secondary'
}
</script>

<template>
  <VRow>
    <VCol cols="12">
      <VCard title="Project List">
        <template #append>
           <VTextField class="mr-4"
            v-model="search"
            placeholder="Cerca Progetto"
            density="compact"
            style="inline-size: 10rem;"
          />
        </template>
        <!-- 👉 User Project List Table -->

        <!-- SECTION Datatable -->
        <VDataTable
          :search="search"
          :headers="projectTableHeaders"
          :items="props.progetti"
          class="rounded-0"
        >
          <!-- projects -->
          <template #item.projectName="{ item }">
            <div class="d-flex align-center py-2">
              <VAvatar
                :size="34"
                class="me-3"
                :image="avatar2"
              />
              <div>
                <h6 class="text-h6 mb-0">
                  {{ item.projectName }}
                </h6>
                <p class="text-sm text-medium-emphasis mb-0">
                  {{ item.descrizioneProgetto }}
                </p>
              </div>
            </div>
          </template>
          <template #item.datInizio="{ item }"> {{ item.datInizio ? new Date(item.datInizio).toLocaleDateString() : '-' }} </template>
          <template #item.datFine="{ item }"> {{ item.datFine ? new Date(item.datFine).toLocaleDateString() : '-' }} </template>
          <template #item.costo="{ item }"> {{ item.costo }} € </template>
          <!-- Progress -->
          <template #item.avanzamento="{ item }">
            <div class="text-high-emphasis">
              {{ item.avanzamento || 0 }}%
            </div>
            <VProgressLinear
              :height="6"
              :model-value="item.avanzamento || 0"
              rounded
              :color="resolveUserProgressVariant(item.avanzamento || 0)"
            />
          </template>
          <template #item.azioni="{ item }">
            <VBtn
              size="small"
              color="primary"
              variant="text"
              @click="openDetailProject(item)"
            >
              <VIcon
                icon="ri-search-ai-2-line"
                size="20"
              />
            </VBtn>
          </template>

          <!-- remove footer -->
          <!-- TODO refactor this after vuetify community gives answer -->
          <template #bottom />
        </VDataTable>
        <!-- !SECTION -->
      </VCard>
    </VCol>
    </VRow>
</template>

<style lang="scss" scoped>
.card-list {
  --v-card-list-gap: 16px;
}
</style>
