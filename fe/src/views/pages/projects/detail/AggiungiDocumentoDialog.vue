<script setup lang="ts">
const isVisible = defineModel<boolean>('isDrawerOpen', { required: true })
</script>

<template>
  <VDialog
    v-model="isVisible"
    max-width="600"
  >
    <VCard title="Aggiungi Documento">
      <VCardText>
        <!-- TODO: Add content -->
      </VCardText>
      <VCardActions>
        <VSpacer />
        <VBtn
          color="error"
          variant="outlined"
          @click="isVisible = false"
        >
          Annulla
        </VBtn>
        <VBtn
          color="success"
          variant="elevated"
          @click="isVisible = false"
        >
          Salva
        </VBtn>
      </VCardActions>
    </VCard>
  </VDialog>
</template>
