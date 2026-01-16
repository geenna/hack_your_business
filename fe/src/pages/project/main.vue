<script setup lang="ts">


import ProjectService from '@/services/ProjectService'
import { ProjectFull, UserToProjectFull } from '@/types/UserToProjectSchema'
import { UserDetail } from '@/types/UserProperties'
import ProjectFullList from '@/views/pages/projects/list/ProjectFullList.vue'
import ProjectFullDetail from '@/views/pages/projects/detail/ProjectFullDetail.vue'



const currentTab = ref(0)
const userToProjects = ref<ProjectFull[]>([])
provide('userToProjects', userToProjects)
const projectSelected = ref<ProjectFull | null>(null)
provide('projectSelected', projectSelected)
const stats = ref({
  numInCorso: 0,
  numInScadenza: 0,
  numScaduti: 0,
  numCompletati: 0
})
provide('stats', stats)

const openDetailProject = (item: ProjectFull) => {
  projectSelected.value = item
  currentTab.value = 1
} 

const fetchProjects = async () => {
  try {
    const response = await ProjectService.getProjectsFull()
    let userMap = (response.data as any)["users"] 
    userToProjects.value = (response.data as any)["userToProjects"]
    userToProjects.value.forEach((project:ProjectFull) => {
     
      project.userToProjects?.forEach((userToProject:UserToProjectFull) => {
        if (userToProject.userId && userMap[userToProject.userId]) {
          userToProject.users = userMap[userToProject.userId] as [UserDetail]
        }
      })
    })
    stats.value.numInCorso = (response.data as any)["numInCorso"]
    stats.value.numInScadenza = (response.data as any)["numInScadenza"]
    stats.value.numScaduti = (response.data as any)["numScaduti"]
    stats.value.numCompletati = (response.data as any)["numCompletati"]
    // Update projectSelected if it exists
    if (projectSelected.value) {
        const currentId = projectSelected.value.id
        const updatedProject = userToProjects.value.find(p => p.id === currentId)
        if (updatedProject) {
            projectSelected.value = updatedProject
        }
    }

  } catch(error) {
    console.error('Error fetching projects:', error)
  }
}

provide('refreshProjects', fetchProjects)

onMounted(() => {
    fetchProjects()
})
</script>

<template>  

 <VWindow v-model="currentTab">
        <VWindowItem>
          <ProjectFullList @openDetailProject="openDetailProject"/>
        </VWindowItem>

        <VWindowItem>
          <ProjectFullDetail @onBack="currentTab = 0"/>
        </VWindowItem>
  </VWindow>  
    <!--class="match-height"-->
    
    

</template>
