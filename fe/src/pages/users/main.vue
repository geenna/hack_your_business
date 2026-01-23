<script setup lang="ts">
import UserList from '@/views/pages/users/UserList.vue'
import UserDetail from '@/views/pages/users/UserDetail.vue'
import { UserProperties } from '@/types/UserProperties'
import UserService from '@/services/UserService'
import RepositoryService from '@/services/RepositoryService'
import { DocumentProperties } from '@/types/DocumentProperties'

import { useConfirm } from '@/shared/state/confirm'
const currentTab = ref("lista-utenti")
const { show: showConfirm } = useConfirm()
const selectedUserID = ref()
provide('selectedUserID', selectedUserID)

const documents = ref<DocumentProperties[]>([])
provide('documents', documents)
const loadDocuments = async () => {
    try {
        const response = await RepositoryService.getAllUserDocuments(selectedUserID.value)
        documents.value = response.data as DocumentProperties[]
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
                const response = await RepositoryService.uploadUserDocument('user', selectedUserID.value, formData)

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
                const response = await RepositoryService.deleteDocument('user', documentId)
                loadDocuments()
            } catch (error) {
                console.error('Failed to delete document:', error)
            }
        }

    } catch (error) {

    }
}
provide('deleteDocumentHandler', deleteDocument)
const onDetailUser = async (userID: string) => {
    currentTab.value = 'dettaglio-utente'
    selectedUserID.value = userID
    loadDocuments()

}
const downloadDocument = async (documentId : string) => {

    const res = await RepositoryService.downloadDocument('user', documentId)
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
  onMounted(() => {
      getUser()
  })



const getUser = async () => {
    const response = await UserService.getAllUsers()
    users.value = response.data
}

const users: Ref<UserProperties[]> = ref<UserProperties[]>([])
provide('users', users)

const onBack = (refresh: boolean | undefined) => {
    currentTab.value = 'lista-utenti'
    selectedUserID.value = null
    if(refresh){
        getUser()
    }
}
</script>

<template>
  <VWindow v-model="currentTab">
    <VWindowItem value="lista-utenti">
        <UserList @onDetailUser="onDetailUser" />
    </VWindowItem>

    <VWindowItem value="dettaglio-utente">
        <UserDetail @onBack="onBack"/>
    </VWindowItem>
    </VWindow>
</template>
