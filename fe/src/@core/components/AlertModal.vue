<script setup lang="ts">
import { useAlert } from '@/shared/state/alert'

const { state, hide } = useAlert()
</script>

<template>
  <VDialog
    v-model="state.isVisible"
    max-width="500"
    persistent
  >
    <VCard class="text-center pa-4">
      <VCardText class="d-flex flex-column align-center justify-center gap-2">
        <VIcon
          size="64"
          :color="state.type"
          :icon="state.type === 'success' ? 'ri-checkbox-circle-line' : state.type === 'error' ? 'ri-error-warning-line' : state.type === 'warning' ? 'ri-error-warning-line' : 'ri-checkbox-circle-line'"
        />
        <h3 class="text-h4 font-weight-bold my-2">
          {{ state.title }}
        </h3>
        <p class="text-body-1 mb-4 text-medium-emphasis">
          {{ state.message }}
        </p>
      </VCardText>
      
      <VCardActions class="justify-center">
        <VBtn
          :color="state.type"
          variant="elevated"
          min-width="120"
          @click="hide"
        >
          OK
        </VBtn>
      </VCardActions>
    </VCard>
  </VDialog>
</template>
