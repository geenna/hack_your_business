<template>
  <v-overlay
    :model-value="loading"
    class="align-center justify-center"
    persistent
    z-index="2000"
    scrim="black"
    style="opacity: 1.0"
  >
    <div class="text-center">
      <v-progress-circular
        color="primary"
        indeterminate
        size="64"
        width="6"
      ></v-progress-circular>
      <div v-if="message" class="text-white mt-4 text-h6 font-weight-bold">
        {{ message }}
      </div>
    </div>
  </v-overlay>
</template>

<script setup lang="ts">
defineProps({
  loading: {
    type: Boolean,
    required: true
  },
  message: {
    type: String,
    default: 'Caricamento...'
  }
});
</script>
