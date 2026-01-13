<script setup lang="ts">
import  CrmSalesOverview from '@/views/dashboards/CrmSalesOverview.vue'
import CardStatisticsWithImages from '@/views/dashboards/CardStatisticsWithImages.vue'
import illustration1 from '@images/cards/illustration-1.png'
import illustration2 from '@images/cards/illustration-2.png'
import ProjectListTableDetail from '@/views/pages/projects/ProjectListTableDetail.vue'

import ProjectService from '@/services/ProjectService'
import { ProjectFull, UserToProjectFull } from '@/types/UserToProjectSchema'
import { UserDetail } from '@/types/UserProperties'

const cardStatisticsWithImages = [
  {
    title: 'Numero progetti',
    subtitle: 'Progetti scaduti',
    stats: '5',
    image: illustration1,
    color: 'error',
  },
  {
    title: 'Numero progetti',
    subtitle: 'Progetti in corso',
    stats: '30',
    image: illustration2,
    color: 'primary',
  },
]

const currentTab = ref(0)
const userToProjects = ref<ProjectFull[]>([])



onMounted(async () => {
  try {
    const response = await ProjectService.getProjectsFull()
    debugger;
    let userMap = response.data["users"] 
    userToProjects.value = response.data["userToProjects"]
    userToProjects.value.forEach((project:ProjectFull) => {
     
      project.userToProjects?.forEach((userToProject:UserToProjectFull) => {
        if (userMap[userToProject.userId]) {
          userToProject.users = userMap[userToProject.userId] as [UserDetail]
        }
      })
    })
  } catch(error) {
    console.error('Error fetching projects:', error)
  }
})
</script>
<template>  
    <!--class="match-height"-->
    <VRow >
      <VCol
        v-for="statistics in cardStatisticsWithImages"
        :key="statistics.title"
        class="pt-8 pt-sm-3"
        cols="12"
        md="3"
        sm="6"
      >
        <CardStatisticsWithImages v-bind="statistics" />
      </VCol>
    

        <VCol cols="6">
            <CrmSalesOverview />
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
              In corso
            </VTab>
            <VTab prepend-icon="ri-alarm-warning-line">
              In scadenza
            </VTab>
            <VTab prepend-icon="ri-alert-line">
              Scaduti
            </VTab>
            <VTab prepend-icon="ri-check-line">
              completati
            </VTab>
          </VTabs>
          <VWindow v-model="currentTab">
            <VWindowItem>
              <ProjectListTableDetail :progetti="userToProjects.filter((project) => project.stato === 'IN PROGRESS')"/>
            </VWindowItem>

            <VWindowItem>
              <ProjectListTableDetail :progetti="userToProjects.filter((project) => project.stato === 'EXPIRING')" />  
            </VWindowItem>

            <VWindowItem>
              <ProjectListTableDetail :progetti="userToProjects.filter((project) => project.stato === 'EXPIRED')" />  
            </VWindowItem>

            <VWindowItem>
              <ProjectListTableDetail :progetti="userToProjects.filter((project) => project.stato === 'COMPLETED')" />  
            </VWindowItem>
          </VWindow>

        </VCardItem>
    </VCard>
    

</template>
