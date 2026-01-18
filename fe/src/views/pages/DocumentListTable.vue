<script setup lang="ts">
    import { useTheme } from 'vuetify'
    import { DocumentProperties } from '@/types/DocumentProperties'
    const { name } = useTheme()
 
     
    const documents = inject('documents') as Ref<DocumentProperties[]>
    
    const headers = [
      {
        title: 'Nome File',
        key: 'fileNameOriginal',
      },
        {
        title: 'Tipo File',
        key: 'contentType',
        width: '150px',
        align: 'center',
      },
      {
        title: 'Data Creazione',
        key: 'createdAt',
        width: '180px',
        align: 'center',
      },
      {
        title: 'Azioni',
        key: 'azioni',
        width: '150px',
        align: 'center',
      },
    ]
    
    const search = ref('')

    const uploadDocument = inject('uploadDocumentHandler') as () => Promise<void>
    const deleteDocument = inject('deleteDocumentHandler') as (documentId:string) => void
    const downloadDocument = inject('downloadDocumentHandler') as (documentId:string) => void


    </script>
    
    <template>
      <VRow>
        <VCol cols="12">
          <VCard title="Documenti">
            <template #append>
              <VBtn
                size="small"
                prepend-icon="ri-add-line"
                @click="uploadDocument"
              >
                Aggiungi documento
              </VBtn>

            </template>
            
            <VDataTable
              :search="search"
              :headers="headers"
              :items="documents"
              item-value="name"
              class="rounded-0"
            >
              <template #item.createdAt="{ item }">
                  {{ new Date(item.createdAt).toLocaleDateString() }}
              </template>

             <template #item.azioni="{ item }">
                <IconBtn size="small" color="error" @click="deleteDocument(item.id)">
                    <VIcon icon="ri-delete-bin-line" />
                </IconBtn>
                
                <IconBtn size="small" color="primary" @click="downloadDocument(item.id)">
                    <VIcon icon="ri-download-line" />
                </IconBtn>
             </template>
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
    