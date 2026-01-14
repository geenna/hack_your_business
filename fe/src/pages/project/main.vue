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

const openDetailProject = (item: ProjectFull) => {
  projectSelected.value = item
  currentTab.value = 1
} 

onMounted(async () => {
  try {
    const response = await ProjectService.getProjectsFull()
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
