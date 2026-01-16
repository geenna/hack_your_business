<template>
    <VRow class="mt-2">
      <VCol class="pt-8 pt-sm-3" cols="12" md="3" sm="6">
        <CardStatisticsWithImages v-bind="{
              title: 'Numero progetti',
              subtitle: 'Progetti scaduti',
              stats: stats.numCompletati,
              image: illustration1,
              color: 'error',
          }" />
      </VCol>
      <VCol class="pt-8 pt-sm-3" cols="12" md="3" sm="6">
        <CardStatisticsWithImages v-bind="{
                  title: 'Numero progetti',
                  subtitle: 'Progetti attivi',
                  stats: stats.numInCorso + stats.numInScadenza,
                  image: illustration2,
                  color: 'primary',
          }" />
      </VCol>

        <VCol cols="6">
            <CrmSalesOverview  v-bind="{
                 numInCorso: stats.numInCorso,
                 numInScadenza: stats.numInScadenza,
                 numScaduti: stats.numScaduti,
                 numCompletati: stats.numCompletati,
          }"/>
        </VCol>
    </VRow>


    <VCard class="mt-6" >
      <VCardItem>

          <VTabs
            v-model="currentTab"
            direction="horizontal"
            align-tabs="center"
            
          >
            <VTab prepend-icon="ri-loader-line">
              In corso ({{stats.numInCorso}})
            </VTab>
            <VTab prepend-icon="ri-alarm-warning-line">
              In scadenza ({{stats.numInScadenza}})
            </VTab>
            <VTab prepend-icon="ri-alert-line">
              Scaduti ({{stats.numScaduti}})
            </VTab>
            <VTab prepend-icon="ri-check-line">
              completati ({{stats.numCompletati}})
            </VTab>
          </VTabs>
          <VWindow v-model="currentTab">
            <VWindowItem>
              <ProjectListTableDetail @openDetailProject="openDetailProject" :progetti="userToProjects.filter((project) => project.stato === 'IN_PROGRESS')"/>
            </VWindowItem>

            <VWindowItem>
              <ProjectListTableDetail @openDetailProject="openDetailProject" :progetti="userToProjects.filter((project) => project.stato === 'EXPIRING')" />  
            </VWindowItem>

            <VWindowItem>
              <ProjectListTableDetail @openDetailProject="openDetailProject" :progetti="userToProjects.filter((project) => project.stato === 'EXPIRED')" />  
            </VWindowItem>

            <VWindowItem>
              <ProjectListTableDetail @openDetailProject="openDetailProject" :progetti="userToProjects.filter((project) => project.stato === 'COMPLETED')" />  
            </VWindowItem>
          </VWindow>

        </VCardItem>
    </VCard>
</template>

<script setup lang="ts">

import  CrmSalesOverview from '@/views/dashboards/CrmSalesOverview.vue'
import CardStatisticsWithImages from '@/views/dashboards/CardStatisticsWithImages.vue'
import ProjectListTableDetail from './ProjectListTableDetail.vue'
import { inject } from 'vue'
import illustration1 from '@images/cards/illustration-1.png'
import illustration2 from '@images/cards/illustration-2.png'
import type { ProjectFull } from '@/types/UserToProjectSchema'

const currentTab = ref(0)  
const userToProjects = inject<ProjectFull[]>('userToProjects', [])
const stats = inject('stats', {numInCorso: 0, numInScadenza: 0, numScaduti: 0, numCompletati: 0})
const emit = defineEmits(['openDetailProject'])
const openDetailProject = (item: ProjectFull) => {
  emit('openDetailProject', item)
}
const cardStatisticsWithImages = [
{
    title: 'Numero progetti',
    subtitle: 'Progetti scaduti',
    stats: 10,
    image: illustration1,
    color: 'error',
},
{
    title: 'Numero progetti',
    subtitle: 'Progetti in corso',
    stats: '30',
    image: illustration2,
    color: 'primary',
}]
</script>
