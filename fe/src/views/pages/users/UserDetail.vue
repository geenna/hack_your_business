<script setup lang="ts">

import UserService from '@/services/UserService'
import UserBioPanel from '@/views/pages/users/components/UserBioPanel.vue'
import UserTabOverview from '@/views/pages/users/components/UserTabOverview.vue'
import UserTabSecurity from '@/views/pages/users/components/UserTabSecurity.vue'
import UserTabBillingsPlans from '@/views/pages/users/components/UserTabBillingsPlans.vue'
import UserTabNotifications from '@/views/pages/users/components/UserTabNotifications.vue'
import UserTabProjects from '@/views/pages/users/components/UserTabProjects.vue'

import type { UserDetail } from '@/types/UserProperties'

const selectedUserID = inject('selectedUserID') as Ref<string>


const userTab = ref(null)

const emit = defineEmits(['onBack'])

const tabs = [
  {
    icon: 'ri-group-line',
    title: 'Overview',
  },
  {
    icon: 'ri-lock-2-line',
    title: 'Security',
  },
  {
    icon: 'ri-bookmark-line',
    title: 'Progetti',
  },
  {
    icon: 'ri-notification-4-line',
    title: 'CoWork',
  },
  {
    icon: 'ri-link-m',
    title: 'Pagamenti',
  },
]

const userData = ref<UserDetail>()
provide('userData', userData)

watch(selectedUserID, async (newId) => {
    if (newId) {
        const response = await UserService.detailUser(newId)
        userData.value = response.data
    }
}, { immediate: true })



</script>

<template>
  <VBtn variant="text" @click="emit('onBack', false)">Indietro</VBtn>
  <VRow v-if="userData" class="mt-6">
    <VCol
      cols="12"
      md="5"
      lg="4"
    >
      <UserBioPanel />
    </VCol>

    <VCol
      cols="12"
      md="7"
      lg="8"
    >
      <VTabs
        v-model="userTab"
        class="v-tabs-pill"
      >
        <VTab
          v-for="tab in tabs"
          :key="tab.icon"
        >
          <VIcon
            start
            :icon="tab.icon"
          />
          <span>{{ tab.title }}</span>
        </VTab>
      </VTabs>

      <VWindow
        v-model="userTab"
        class="mt-6 disable-tab-transition"
        :touch="false"
      >
        <VWindowItem>
          <UserTabOverview />
        </VWindowItem>

        <VWindowItem>
          <UserTabSecurity />
        </VWindowItem>

        <VWindowItem>
           <UserTabProjects />
        </VWindowItem>

        <VWindowItem>
          <UserTabNotifications />
        </VWindowItem>

        <VWindowItem>
          <UserTabBillingsPlans :user-data="userData" />
        </VWindowItem>
      </VWindow>
    </VCol>
  </VRow>
</template>
