<script setup lang="ts">
import type { UserProperties } from '@/types/UserProperties'
import CreateUserDialog from './CreateUserDialog.vue'

const emit = defineEmits(['onDetailUser'])
// 👉 Store
const searchQuery = ref('')
const selectedRole = ref()
const selectedPlan = ref()
const selectedStatus = ref()

// Data table options
const itemsPerPage = ref(10)
const page = ref(1)
const sortBy = ref()
const orderBy = ref()

// Update data table options
const updateOptions = (options: any) => {
  sortBy.value = options.sortBy[0]?.key
  orderBy.value = options.sortBy[0]?.order
}

// Headers
const headers = [
  { title: 'Cognome', key: 'cognome' },
  { title: 'Nome', key: 'nome' },
  { title: 'Email', key: 'email' },
  { title: 'Ruolo', key: 'userType' },
  { title: 'Stato', key: 'user_status' },
  { title: 'Actions', key: 'actions', sortable: false },
]


const totalUsers = computed(() => 100)

// 👉 search filters
const roles = [
  { title: 'Amministratore', value: 'admin' },
  { title: 'Collaboratore', value: 'collaboratore' },
  { title: 'Cliente', value: 'cliente' },
]

const status = [
  { title: 'Attivo', value: 'active' },
  { title: 'Disattivo', value: 'inactive' },
]

const resolveUserRoleVariant = (role: string) => {
  const roleLowerCase = role.toLowerCase()

  if (roleLowerCase === 'cliente')
    return { color: 'success', icon: 'ri-user-line' }
  if (roleLowerCase === 'collaboratore')
    return { color: 'info', icon: 'ri-pie-chart-line' }
  if (roleLowerCase === 'admin')
    return { color: 'primary', icon: 'ri-vip-crown-line' }

  return { color: 'success', icon: 'ri-user-line' }
}

const resolveUserStatusVariant = (role: string) => {
  const roleLowerCase = role.toLowerCase()
  
  if (roleLowerCase === 'disattivo')
    return 'error'

  return 'primary'

}


const isAddNewUserDrawerVisible = ref(false)

// 👉 Add new user
const addNewUser = async () => {

}

// 👉 Delete user
const deleteUser = async (id: number) => {
 
}

const users = inject<Ref<UserProperties[]>>('users')

const filteredUsers = computed(() => {
  if (!users || !users.value) return []
  
  if (!selectedRole.value)
    return users.value

  return users.value.filter(user => user.userType.toLowerCase() === selectedRole.value.toLowerCase())
})

const widgetData = ref([
  { title: 'Session', value: '21,459', change: 29, desc: 'Total Users', icon: 'ri-group-line', iconColor: 'primary' },
  { title: 'Paid Users', value: '4,567', change: 18, desc: 'Last Week Analytics', icon: 'ri-user-add-line', iconColor: 'error' },
  { title: 'Active Users', value: '19,860', change: -14, desc: 'Last Week Analytics', icon: 'ri-user-follow-line', iconColor: 'success' },
  { title: 'Pending Users', value: '237', change: 42, desc: 'Last Week Analytics', icon: 'ri-user-search-line', iconColor: 'warning' },

])

const isUserCreateDialogVisible = ref(false)

</script>

<template>
    <!-- 👉 create user dialog -->
  <CreateUserDialog
    v-model:is-dialog-visible.capitialize="isUserCreateDialogVisible"
    :user-data="undefined"
  />
  <section>
    <!-- 👉 Widgets -->
    <div class="d-flex mb-6">
      <VRow>
        <template
          v-for="(data, id) in widgetData"
          :key="id"
        >
          <VCol
            cols="12"
            md="3"
            sm="6"
          >
            <VCard>
              <VCardText>
                <div class="d-flex justify-space-between">
                  <div class="d-flex flex-column gap-y-1">
                    <span class="text-base text-high-emphasis">{{ data.title }}</span>
                    <h4 class="text-h4 d-flex align-center gap-2">
                      {{ data.value }}
                      <span
                        class="text-base font-weight-regular"
                        :class="data.change > 0 ? 'text-success' : 'text-error'"
                      >({{ prefixWithPlus(data.change) }}%)</span>
                    </h4>

                    <p class="text-sm mb-0">
                      {{ data.desc }}
                    </p>
                  </div>
                  <VAvatar
                    :color="data.iconColor"
                    variant="tonal"
                    rounded
                    size="42"
                  >
                    <VIcon
                      :icon="data.icon"
                      size="26"
                    />
                  </VAvatar>
                </div>
              </VCardText>
            </VCard>
          </VCol>
        </template>
      </VRow>
    </div>

    <VCard
      title="Filters"
      class="mb-6"
    >
      <VCardText>
        <VRow>
          <!-- 👉 Select Role -->
          <VCol
            cols="12"
            sm="4"
          >
            <VSelect
              v-model="selectedRole"
              label="Select Role"
              placeholder="Select Role"
              :items="roles"
              clearable
              clear-icon="ri-close-line"
            />
          </VCol>

          <!-- 👉 Select Status -->
          <VCol
            cols="12"
            sm="4"
          >
            <VSelect
              v-model="selectedStatus"
              label="Select Status"
              placeholder="Select Status"
              :items="status"
              clearable
              clear-icon="ri-close-line"
            />
          </VCol>
        </VRow>
      </VCardText>

      <VDivider />

      <VCardText class="d-flex flex-wrap gap-4">
        <VSpacer />
        <div class="app-user-search-filter d-flex align-center">
          <!-- 👉 Search  -->
          <VTextField
            v-model="searchQuery"
            placeholder="Search User"
            density="compact"
            class="me-4"
          />
          <!-- 👉 Add user button -->
          <VBtn @click="isUserCreateDialogVisible = true">
            Aggiungi Utente
          </VBtn>
        </div>
      </VCardText>

      <!-- SECTION datatable -->
      <VDataTable
        v-model:items-per-page="itemsPerPage"
        v-model:page="page"
        :items="filteredUsers"
        item-value="id"
        :items-length="totalUsers"
        :headers="headers"
        show-select
        class="text-no-wrap rounded-0"
        @update:options="updateOptions"
      >
      <!-- Role -->
        <template #item.userType="{ item }">
          <div class="d-flex gap-4">
            <VIcon
              :icon="resolveUserRoleVariant(item.userType).icon"
              :color="resolveUserRoleVariant(item.userType).color"
            />
            <span class="text-capitalize text-high-emphasis">{{ item.userType }}</span>
          </div>
        </template>

        <template #item.user_status="{ item }">
          <div class="d-flex gap-4">
            <VChip
              :color="resolveUserStatusVariant(item.user_status)"
              size="small"
            >
              {{ item.user_status }}
            </VChip>
          </div>
        </template>

        <!-- Actions -->
        <template #item.actions="{ item }">
          <IconBtn
            size="small"
            @click=""
          >
            <VIcon icon="ri-delete-bin-7-line" />
          </IconBtn>

          <IconBtn
            size="small"
            
          >
            <VIcon icon="ri-eye-line" @click="emit('onDetailUser', item.id)"/>
          </IconBtn>

          <IconBtn
            size="small"
            color="medium-emphasis"
          >
            <VIcon
              size="24"
              icon="ri-more-2-line"
            />

          </IconBtn>
        </template>
      </VDataTable>
      <!-- SECTION -->

    </VCard>

  </section>
</template>

<style lang="scss">
.app-user-search-filter {
  inline-size: 24.0625rem;
}

.text-capitalize {
  text-transform: capitalize;
}

.user-list-name:not(:hover) {
  color: rgba(var(--v-theme-on-background), var(--v-high-emphasis-opacity));
}
</style>
