<script setup lang="ts">
    import { useTheme } from 'vuetify'
    import avatar2 from '@images/avatars/avatar-2.png'
    import ProjectService from '@/services/ProjectService'
    import { UserDetail } from '@/types/UserProperties'
    import { ProjectWithUserRole } from '@/types/ProjectWithUserRole'
    import { DocumentProperties } from '@/types/DocumentProperties'
    const { name } = useTheme()
    
    const isLoading = ref(false)
    
  
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
    

    </script>
    
    <template>
      <VRow>
        <VCol cols="12">
          <VCard title="Documenti">
            <template #append>
              <VTextField
                v-model="search"
                placeholder="Cerca File"
                density="compact"
                style="inline-size: 10rem;"
              />
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
    