<script setup lang="ts">
import { useConfirm } from '@/shared/state/confirm'

const { state, confirm, cancel } = useConfirm()
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
          color="warning"
          icon="ri-alert-line"
        />
        <h3 class="text-h4 font-weight-bold my-2">
          {{ state.title }}
        </h3>
        <p class="text-body-1 mb-4 text-medium-emphasis">
          {{ state.message }}
        </p>
      </VCardText>
      
      <VCardActions class="justify-center gap-4">
        <VBtn
          variant="outlined"
          color="secondary"
          @click="cancel"
        >
          Annulla
        </VBtn>
        <VBtn
          color="primary"
          variant="elevated"
          @click="confirm"
        >
          Conferma
        </VBtn>
      </VCardActions>
    </VCard>
  </VDialog>
</template>
