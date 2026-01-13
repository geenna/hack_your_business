<script setup lang="ts">
import  CrmSalesOverview from '@/views/dashboards/CrmSalesOverview.vue'
import CardStatisticsWithImages from '@/views/dashboards/CardStatisticsWithImages.vue'
import illustration1 from '@images/cards/illustration-1.png'
import illustration2 from '@images/cards/illustration-2.png'


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
        <VCardTitle class="d-flex justify-end align-center">
            <VBtn>
                Nuovo progetto
            <VIcon
                end
                icon="ri-sticky-note-add-line"
            />
            </VBtn>
        </VCardTitle>
        <VCardItem>
          <VRow>
    <VCol
      cols="12"
      sm="4"
      lg="2"
      xl="2"
      md="3"
    >
      <VTabs
        v-model="currentTab"
        direction="vertical"
        class="v-tabs-pill"
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
    </VCol>

    <VCol
      cols="12"
      sm="8"
    >
      <VWindow v-model="currentTab">
        <VWindowItem>
          <p>
            Sed aliquam ultrices mauris. Donec posuere vulputate arcu. Morbi ac felis. Etiam feugiat lorem non metus. Sed a libero.
          </p>

          <p class="mb-0">
            Phasellus dolor. Fusce neque. Fusce fermentum odio nec arcu. Pellentesque libero tortor, tincidunt et, tincidunt eget, semper nec, quam. Phasellus blandit leo ut odio.
          </p>
        </VWindowItem>

        <VWindowItem>
          <p>
            Morbi nec metus. Suspendisse faucibus, nunc et pellentesque egestas, lacus ante convallis tellus, vitae iaculis lacus elit id tortor. Sed mollis, eros et ultrices tempus, mauris ipsum aliquam libero, non adipiscing dolor urna a orci. Curabitur ligula sapien, tincidunt non, euismod vitae, posuere imperdiet, leo. Nunc sed turpis.
          </p>

          <p class="mb-0">
            Donec venenatis vulputate lorem. Aenean viverra rhoncus pede. In dui magna, posuere eget, vestibulum et, tempor auctor, justo. Fusce commodo aliquam arcu. Suspendisse enim turpis, dictum sed, iaculis a, condimentum nec, nisi.
          </p>
        </VWindowItem>

        <VWindowItem>
          <p>
            Fusce a quam. Phasellus nec sem in justo pellentesque facilisis. Nam eget dui. Proin viverra, ligula sit amet ultrices semper, ligula arcu tristique sapien, a accumsan nisi mauris ac eros. In dui magna, posuere eget, vestibulum et, tempor auctor, justo.
          </p>

          <p class="mb-0">
            Cras sagittis. Phasellus nec sem in justo pellentesque facilisis. Proin sapien ipsum, porta a, auctor quis, euismod ut, mi. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nam at tortor in tellus interdum sagittis.
          </p>
        </VWindowItem>
        <VWindowItem>
          <p>
            Fusce a quam. Phasellus nec sem in justo pellentesque facilisis. Nam eget dui. Proin viverra, ligula sit amet ultrices semper, ligula arcu tristique sapien, a accumsan nisi mauris ac eros. In dui magna, posuere eget, vestibulum et, tempor auctor, justo.
          </p>

          <p class="mb-0">
            Cras sagittis. Phasellus nec sem in justo pellentesque facilisis. Proin sapien ipsum, porta a, auctor quis, euismod ut, mi. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nam at tortor in tellus interdum sagittis.
          </p>
        </VWindowItem>
      </VWindow>
    </VCol>
  </VRow>
        </VCardItem>
    </VCard>
    

</template>
