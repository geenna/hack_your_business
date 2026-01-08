<script setup lang="ts">

import UserService from '@/services/UserService'
import UserBioPanel from '@/views/pages/users/components/UserBioPanel.vue'
import UserTabOverview from '@/views/pages/users/components/UserTabOverview.vue'
import UserTabSecurity from '@/views/pages/users/components/UserTabSecurity.vue'
import UserTabBillingsPlans from '@/views/pages/users/components/UserTabBillingsPlans.vue'
import UserTabNotifications from '@/views/pages/users/components/UserTabNotifications.vue'
import UserTabConnections from '@/views/pages/users/components/UserTabConnections.vue'

const selectedUserID = inject('selectedUserID') as Ref<string>
const userData = ref()
const userTab = ref(null)

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
    title: 'Billing & Plan',
  },
  {
    icon: 'ri-notification-4-line',
    title: 'Notifications',
  },
  {
    icon: 'ri-link-m',
    title: 'Connections',
  },
]


watch(selectedUserID, async (newId) => {
    if (newId) {
        const response = await UserService.detailUser(newId)
        userData.value = response.data
    }
}, { immediate: true })
</script>

<template>
  <VRow v-if="userData">
    <VCol
      cols="12"
      md="5"
      lg="4"
    >
      <UserBioPanel :user-data="userData" />
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
          <UserTabBillingsPlans />
        </VWindowItem>

        <VWindowItem>
          <UserTabNotifications />
        </VWindowItem>

        <VWindowItem>
          <UserTabConnections />
        </VWindowItem>
      </VWindow>
    </VCol>
  </VRow>
</template>
