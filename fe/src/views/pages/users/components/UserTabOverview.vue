<script setup lang="ts">
import { useTheme } from 'vuetify'
//import UserInvoiceTable from './UserInvoiceTable.vue'
  import pdf from '@images/icons/project-icons/pdf.png'
import avatar2 from '@images/avatars/avatar-2.png'
import avatar3 from '@images/avatars/avatar-3.png'
import avatar4 from '@images/avatars/avatar-4.png'
import avatar5 from '@images/avatars/avatar-5.png'



const { name } = useTheme()



const search = ref('')
</script>

<template>
  <VRow>
    <VCol cols="12">
      <!-- 👉 Activity timeline -->
      <VCard title="Attività utente">
        <VCardText>
          <VTimeline
            density="compact"
            align="start"
            truncate-line="both"
            :line-inset="8"
            class="v-timeline-density-compact"
          >
            <VTimelineItem
              dot-color="error"
              size="x-small"
            >
              <div class="d-flex justify-space-between align-center flex-wrap gap-2 mb-3">
                <span class="app-timeline-title">
                  12 Invoices have been paid
                </span>
                <span class="app-timeline-meta">12 min ago</span>
              </div>

              <p class="app-timeline-text mb-2">
                Invoices have been paid to the company
              </p>
              <div class="d-inline-flex align-center timeline-chip">
                <img
                  :src="pdf"
                  height="20"
                  class="me-2"
                  alt="img"
                >

                <span class="app-timeline-text font-weight-medium">
                  invoice.pdf
                </span>
              </div>
            </VTimelineItem>

            <VTimelineItem
              dot-color="primary"
              size="x-small"
            >
              <div class="d-flex justify-space-between align-center flex-wrap gap-2 mb-3">
                <span class="app-timeline-title">
                  Client Meeting
                </span>
                <span class="app-timeline-meta">45 min ago</span>
              </div>

              <p class="app-timeline-text mb-2">
                React Project meeting with john @10:15am
              </p>

              <div class="d-flex align-center mt-3">
                <VAvatar
                  size="32"
                  class="me-2"
                  :image="avatar2"
                />
                <div>
                  <p class="text-sm font-weight-medium mb-0">
                    Lester McCarthy (Client)
                  </p>
                  <span class="text-sm">CEO of Kelly Group</span>
                </div>
              </div>
            </VTimelineItem>

            <VTimelineItem
              dot-color="info"
              size="x-small"
            >
              <div class="d-flex justify-space-between align-center flex-wrap gap-2 mb-3">
                <span class="app-timeline-title">
                  Create a new project for client
                </span>
                <span class="app-timeline-meta">2 day ago</span>
              </div>

              <p class="app-timeline-text mb-2">
                6 team members in a project
              </p>

              <div class="v-avatar-group">
                <VAvatar
                  v-for="avatar in [avatar2, avatar3, avatar4, avatar5]"
                  :key="avatar"
                  :image="avatar"
                />
                <VAvatar :color="name === 'light' ? '#F0EFF0' : '#3F3B59'">
                  <span class="text-high-emphasis">+3</span>
                </VAvatar>
              </div>
            </VTimelineItem>
          </VTimeline>
        </VCardText>
      </VCard>
    </VCol>

    <VCol cols="12">
      
    </VCol>
  </VRow>
</template>
