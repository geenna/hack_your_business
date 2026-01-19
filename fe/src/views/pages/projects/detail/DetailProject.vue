<template>

    <VRow>
        <VCol>
            <h4>{{ projectSelected.descrizioneProgetto }}</h4>
        </VCol>

        <VCol style="min-width: 400px; max-width: 400px; flex: 0 0 400px;">
            <AvanzamentoRadialGraph :avanzamento="projectSelected?.avanzamento ?? 0" />
        </VCol>
    </VRow>
    
        <VCard class="mt-4">
            <VCardTitle>
                Utenti Progetto
            </VCardTitle>
            <VCardText>
                
            </VCardText>
        </VCard>
  
</template>

<script setup lang="ts">
import { inject } from 'vue'
import AvanzamentoRadialGraph from './AvanzamentoRadialGraph.vue'
import { ProjectFull } from '@/types/UserToProjectSchema';
const projectSelected = inject('projectSelected') as Ref<ProjectFull>


</script>
