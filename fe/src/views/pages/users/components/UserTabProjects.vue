<script setup lang="ts">
  import { useTheme } from 'vuetify'
  import pdf from '@images/icons/project-icons/pdf.png'
import avatar2 from '@images/avatars/avatar-2.png'
import avatar3 from '@images/avatars/avatar-3.png'
import avatar4 from '@images/avatars/avatar-4.png'
import avatar5 from '@images/avatars/avatar-5.png'
  import figma from '@images/icons/project-icons/figma.png'
import html5 from '@images/icons/project-icons/html5.png'
import python from '@images/icons/project-icons/python.png'
import react from '@images/icons/project-icons/react.png'
import sketch from '@images/icons/project-icons/sketch.png'
import vue from '@images/icons/project-icons/vue.png'
import xamarin from '@images/icons/project-icons/xamarin.png'
const { name } = useTheme()
const projectTableHeaders = [
  {
    title: 'Progetto',
    key: 'name',
  },
  {
    title: 'Data Inizio',
    key: 'datInizio',
  },
  {
    title: 'Data Fine',
    key: 'datFine',
  },
  {
    title: '% Completamento',
    key: 'progress',
  },
  {
    title: 'Costo',
    key: 'price',
  },
]

const projects = [
  {
    logo: react,
    name: 'Cliente A',
    project: 'Sviluppo bando MIUR ',
    datInizio: '20/11/2025',
    datFine: '20/12/2026',
    price:"1000 €",
    progress: 78,
  },
  {
    logo: figma,
    name: 'Falcon Logo Design',
    project: 'Figma Project',
    progress: 18,
    datInizio: '20/11/2025',
    datFine: '20/12/2026',
    price:"1000 €",
  },
  {
    logo: vue,
    name: 'Dashboard Design',
    project: 'Vuejs Project',
    progress: 62,
    datInizio: '20/11/2025',
    datFine: '20/12/2026',
    price:"1000 €",
  },
  {
    logo: xamarin,
    name: 'Foodista mobile app',
    project: 'Xamarin Project',
    progress: 8,
    datInizio: '20/11/2025',
    datFine: '20/12/2026',
    price:"1000 €",
  },
  {
    logo: python,
    name: 'Dojo Email App',
    project: 'Python Project',
    progress: 49,
    datInizio: '20/11/2025',
    datFine: '20/12/2026',
    price:"1000 €",
  },
  {
    logo: sketch,
    name: 'Blockchain Website',
    project: 'Sketch Project',
    progress: 92,
    datInizio: '20/11/2025',
    datFine: '20/12/2026',
    price:"1000 €",
  },
  {
    logo: html5,
    name: 'Hoffman Website',
    project: 'HTML Project',
    datInizio: '20/11/2025',
    datFine: '20/12/2026',
    price:"1000 €",   
    progress: 88,
    
  },
]

const resolveUserProgressVariant = progress => {
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
          <VTextField
            v-model="search"
            placeholder="Search Project"
            density="compact"
            style="inline-size: 10rem;"
          />
        </template>
        <!-- 👉 User Project List Table -->

        <!-- SECTION Datatable -->
        <VDataTable
          :search="search"
          :headers="projectTableHeaders"
          :items="projects"
          item-value="name"
          class="text-no-wrap rounded-0"
        >
          <!-- projects -->
          <template #item.name="{ item }">
            <div class="d-flex align-center">
              <VAvatar
                :size="34"
                class="me-3"
                :image="item.logo"
              />
              <div>
                <h6 class="text-h6 mb-0">
                  {{ item.name }}
                </h6>
                <p class="text-sm text-medium-emphasis mb-0">
                  {{ item.project }}
                </p>
              </div>
            </div>
          </template>

          <!-- total task -->
          <template #item.totalTask="{ item }">
            <div class="text-high-emphasis">
              {{ item.totalTask }}
            </div>
          </template>

          <!-- Progress -->
          <template #item.progress="{ item }">
            <div class="text-high-emphasis">
              {{ item.progress }}%
            </div>
            <VProgressLinear
              :height="6"
              :model-value="item.progress"
              rounded
              :color="resolveUserProgressVariant(item.progress)"
            />
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
