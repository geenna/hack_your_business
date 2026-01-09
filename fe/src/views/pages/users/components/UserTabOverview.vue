<script setup lang="ts">
import { useTheme } from 'vuetify'
//import UserInvoiceTable from './UserInvoiceTable.vue'
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

const { name } = useTheme()

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

const search = ref('')
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

    <VCol cols="12">
      <!-- 👉 Activity timeline -->
      <VCard title="Attività utente">
        <VCardText>
          <VTimeline
            density="compact"
            align="start"
            truncate-line="both"
            :line-inset="8"
            class="v-timeline-density-compact"
          >
            <VTimelineItem
              dot-color="error"
              size="x-small"
            >
              <div class="d-flex justify-space-between align-center flex-wrap gap-2 mb-3">
                <span class="app-timeline-title">
                  12 Invoices have been paid
                </span>
                <span class="app-timeline-meta">12 min ago</span>
              </div>

              <p class="app-timeline-text mb-2">
                Invoices have been paid to the company
              </p>
              <div class="d-inline-flex align-center timeline-chip">
                <img
                  :src="pdf"
                  height="20"
                  class="me-2"
                  alt="img"
                >

                <span class="app-timeline-text font-weight-medium">
                  invoice.pdf
                </span>
              </div>
            </VTimelineItem>

            <VTimelineItem
              dot-color="primary"
              size="x-small"
            >
              <div class="d-flex justify-space-between align-center flex-wrap gap-2 mb-3">
                <span class="app-timeline-title">
                  Client Meeting
                </span>
                <span class="app-timeline-meta">45 min ago</span>
              </div>

              <p class="app-timeline-text mb-2">
                React Project meeting with john @10:15am
              </p>

              <div class="d-flex align-center mt-3">
                <VAvatar
                  size="32"
                  class="me-2"
                  :image="avatar2"
                />
                <div>
                  <p class="text-sm font-weight-medium mb-0">
                    Lester McCarthy (Client)
                  </p>
                  <span class="text-sm">CEO of Kelly Group</span>
                </div>
              </div>
            </VTimelineItem>

            <VTimelineItem
              dot-color="info"
              size="x-small"
            >
              <div class="d-flex justify-space-between align-center flex-wrap gap-2 mb-3">
                <span class="app-timeline-title">
                  Create a new project for client
                </span>
                <span class="app-timeline-meta">2 day ago</span>
              </div>

              <p class="app-timeline-text mb-2">
                6 team members in a project
              </p>

              <div class="v-avatar-group">
                <VAvatar
                  v-for="avatar in [avatar2, avatar3, avatar4, avatar5]"
                  :key="avatar"
                  :image="avatar"
                />
                <VAvatar :color="name === 'light' ? '#F0EFF0' : '#3F3B59'">
                  <span class="text-high-emphasis">+3</span>
                </VAvatar>
              </div>
            </VTimelineItem>
          </VTimeline>
        </VCardText>
      </VCard>
    </VCol>

    <VCol cols="12">
      
    </VCol>
  </VRow>
</template>
