<script setup lang="ts">


import ProjectService from '@/services/ProjectService'
import { ProjectFull, UserToProjectFull } from '@/types/UserToProjectSchema'
import { UserDetail } from '@/types/UserProperties'
import ProjectFullList from '@/views/pages/projects/list/ProjectFullList.vue'
import ProjectFullDetail from '@/views/pages/projects/detail/ProjectFullDetail.vue'
import { DocumentProperties } from '@/types/DocumentProperties'
import RepositoryService from '@/services/RepositoryService'
import { useConfirm } from '@/shared/state/confirm'
import {getFilenameFromContentDisposition} from '@/utils/utility'

const currentTab = ref(0)
const userToProjects = ref<ProjectFull[]>([])
provide('userToProjects', userToProjects)
const projectSelected = ref<ProjectFull | null>(null)
provide('projectSelected', projectSelected)

const { show: showConfirm } = useConfirm()


const documents = ref<DocumentProperties[]>([])
provide('documents', documents)
const loadDocuments = async () => {
  documents.value = []
  try {
    if(projectSelected?.value?.id){
      const response = await RepositoryService.getAllProjectDocuments(projectSelected!.value!.id!)
      documents.value = response.data as DocumentProperties[]
    }
  } catch (error) {
      console.error('Error loading documents:', error)
      documents.value = []
  }
}
const uploadDocument = async () => {
    return new Promise<void>((resolve, reject) => {
        // Create a file input if not already present
        const input = document.createElement('input')
        input.type = 'file'
        input.accept = '*' // Optionally restrict file types
        
        input.onchange = async () => {
            if (!input.files || !input.files.length) {
                reject(new Error('No file selected'))
                return
            }
            const file = input.files[0]

            // Prepare payload for the backend
            const formData = new FormData()
            formData.append('files', file)
           

            try {
                // Call your backend API to upload the file
                // Adjust the endpoint and parameters according to your API
                const response = await RepositoryService.uploadUserDocument('project', projectSelected!.value!.id, formData)
                
                loadDocuments()

                resolve()
            } catch (error) {
                reject(error)
            }
        }

        input.click()
    })
}
provide('uploadDocumentHandler', uploadDocument)
const deleteDocument = async (documentId : string) => {
    try {

        const confirmed = await showConfirm(
        'Eliminazione documento',
        `Sei sicuro di voler eliminare il documento?`
    )

        if (confirmed) {
            try {
                const response = await RepositoryService.deleteDocument('project', documentId)
                loadDocuments()
            } catch (error) {
                console.error('Failed to delete document:', error)
            }
        }    
        
    } catch (error) {
        
    }
}
provide('deleteDocumentHandler', deleteDocument)

const downloadDocument = async (documentId : string) => {
    
  const res = await RepositoryService.downloadDocument('project', documentId)
  const contentType = res.headers["content-type"] || "application/octet-stream"
  const cd = res.headers["content-disposition"]
  const filename = getFilenameFromContentDisposition(cd) || `document-${documentId}`

  const blob = new Blob([res.data], { type: contentType })
  const url = URL.createObjectURL(blob)

  // Apri in nuova tab
  const win = window.open(url, "_blank", "noopener,noreferrer")

  // Opzionale: set title (funziona su molti browser)
  if (win) {
    win.onload = () => {
      try {
        win.document.title = filename
      } catch {}
    }
  }

  // NON revocare subito: la tab lo usa
  setTimeout(() => URL.revokeObjectURL(url), 60_000)
}
provide('downloadDocumentHandler', downloadDocument)

const stats = ref({
  numInCorso: 0,
  numInScadenza: 0,
  numScaduti: 0,
  numCompletati: 0
})
provide('stats', stats)

const openDetailProject = (item: ProjectFull) => {
  projectSelected.value = item
  loadDocuments()
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
