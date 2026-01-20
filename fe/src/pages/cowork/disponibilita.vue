<template>

<AggiungiDisponibilitaDialog v-model:is-dialog-visible="isAddDisponibilitaDialogVisible" @submit="onSubmit" />

</template>


<script setup lang="ts">
import AggiungiDisponibilitaDialog from '@/views/pages/cowork/AggiungiDisponibilitaDialog.vue';

const isAddDisponibilitaDialogVisible = ref(true);
const onsubmit = (data: { date: any; value: number; status: string; tipoPagamento: string }) => {
  console.log('Disponibilità aggiunta:', data);
  // Logica per gestire la disponibilità aggiunta
};

</script>
