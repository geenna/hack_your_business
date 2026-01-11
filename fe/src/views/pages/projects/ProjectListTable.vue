<script setup lang="ts">
import { useTheme } from 'vuetify'
import avatar2 from '@images/avatars/avatar-2.png'
import ProjectService from '@/services/ProjectService'
import { UserDetail } from '@/types/UserProperties'
import { ProjectWithUserRole } from '@/types/ProjectWithUserRole'
const { name } = useTheme()

const userData = inject('userData') as Ref<UserDetail | undefined>
const isLoading = ref(false)
const projects = ref<ProjectWithUserRole[]>([])

const getProjectsByUser = () => {
    isLoading.value = true
    ProjectService.getAllProjectsByUser(userData.value!.id)
        .then(response => {
            projects.value = response.data
        })
        .catch(error => {
            console.error(error)
        })
        .finally(() => {
            isLoading.value = false
        })
}

watch(userData, () => {
    if (userData.value?.id ) {
        getProjectsByUser()
    }
}, { immediate: true })

const projectTableHeaders = [
  {
    title: 'Progetto',
    key: 'projectName',
  },
    {
    title: 'Ruolo',
    key: 'role',
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
    key: 'avanzamento',
  },
  {
    title: 'Costo (€)',
    key: 'costo',
  },
]

const search = ref('')

const resolveUserProgressVariant = (progress:number) => {
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
          <template #item.projectName="{ item }">
            <div class="d-flex align-center">
              <VAvatar
                :size="34"
                class="me-3"
                :image="avatar2"
              />
              <div>
                <h6 class="text-h6 mb-0">
                  {{ item.projectName }}
                </h6>
                <p class="text-sm text-medium-emphasis mb-0">
                  {{ item.descrizioneProgetto }}
                </p>
              </div>
            </div>
          </template>
          <template #item.datInizio="{ item }"> {{ new Date(item.datInizio).toLocaleDateString() }} </template>
          <template #item.datFine="{ item }"> {{ new Date(item.datFine).toLocaleDateString() }} </template>
          <template #item.costo="{ item }"> {{ item.costo }} € </template>
          <!-- Progress -->
          <template #item.avanzamento="{ item }">
            <div class="text-high-emphasis">
              {{ item.avanzamento }}%
            </div>
            <VProgressLinear
              :height="6"
              :model-value="item.avanzamento"
              rounded
              :color="resolveUserProgressVariant(item.avanzamento)"
            />
          </template>

          <!-- remove footer -->
          <!-- TODO refactor this after vuetify community gives answer -->
          <template #bottom />
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
