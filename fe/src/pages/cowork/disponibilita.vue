<template>

<AggiungiDisponibilitaDialog v-model:is-dialog-visible="isAddDisponibilitaDialogVisible" @onSubmit="onSubmit" />

 <section>

    <VCard
      title="Filters"
      class="mb-6"
    >

    <template #append>
      <VBtn size="small"
          prepend-icon="ri-add-line"
          class="mb-4" @click="isAddDisponibilitaDialogVisible = true">Aggiungi Disponibilità
      </VBtn>
    </template>

      <VCardText>

        <VRow>
          <!-- 👉 Select Role -->
          <VCol
            cols="6"
            sm="4"
          >
            <VSelect
              v-model="periodoSelezionato"
              label="Seleziona Periodo"
              placeholder="Seleziona Periodo"
              :items="periodo"

            />
          </VCol>

        <VCol
            cols="6"
            sm="4"
          >
           <VSelect
              v-model="tipologiaSelezionata"
              label="Seleziona Tipologia"
              placeholder="Seleziona Tipologia"
              :items="servizi"
              item-title="nome"
              item-value="id"
            />
          </VCol>

          <VCol
            cols="6"
            sm="4"
          >
          <VBtn class = "mt-1"  @click="loadDisponibilita()">
            Aggiorna
          </VBtn></VCol>
        </VRow>
      </VCardText>

      <VDivider />


      <!-- SECTION datatable -->
      <VDataTable
        :items="items"
        :headers="headers"
      >
      <template #item.date="{ item }">
          {{ new Date(item.date).toLocaleDateString() }}
      </template>

      <template #item.dispMattina="{ item }">
          <span>- Totale: {{ item.numMattina }}</span><br>
          <span>- Residua: {{ item.numMattina - item.numPrenotazioniMattina }}</span><br>
          <span>- Num Prenotazioni: {{ item.numPrenotazioniMattina  }}</span>
      </template>

      <template #item.dispPomeriggio="{ item }">
          <span>- Totale: {{ item.numPomeriggio }}</span><br>
          <span>- Residua: {{ item.numPomeriggio - item.numPrenotazioniPomeriggio }}</span><br>
          <span>- Num. Prenotazioni: {{ item.numPrenotazioniPomeriggio  }}</span>
      </template>

      <template #item.azioni="{ item }">
         <IconBtn
            size="small"
            color="error"
            @click="console.log('Elimina disponibilità', item)"
          >
            <VIcon icon="ri-delete-bin-7-line" />
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

<script setup lang="ts">
import AggiungiDisponibilitaDialog from '@/views/pages/cowork/AggiungiDisponibilitaDialog.vue';
import { ref, Ref, onMounted } from 'vue'
import type { ServiziModel } from '@/types/ServiziModel'
import CoWorkingService from '@/services/CoWorkingService'
import type { DisponibilitaCompletaType } from '@/types/DisponibilitaCompletaType'

const isAddDisponibilitaDialogVisible = ref(false);
const onSubmit = (data: {reload:boolean }) => {
  if(data.reload)
    loadDisponibilita();

};
const servizi:Ref<ServiziModel[]> = ref<ServiziModel[]>([])
provide('serviziPresenti', servizi);

const items:Ref<DisponibilitaCompletaType[]> = ref<DisponibilitaCompletaType[]>([])

onMounted(() => {
  loadServiziPresenti()
});

const periodoSelezionato = ref('30_DAYS')
const tipologiaSelezionata = ref('COWORK_BASE')
const periodo = [
  { title: 'Prossimi 30 giorni', value: '30_DAYS' },
  { title: 'Prossimi 60 giorni', value: '60_DAYS' },
  { title: 'Prossimi 90 giorni', value: '90_DAYS' },
  { title: 'Prossimi 6 mesi', value: '6_MONTHS' },
  { title: 'Prossimi 12 mesi', value: '12_MONTHS' },
]

const tipologia = [
  { title: 'Cowork', value: 'COWORK_BASE' },
  { title: 'Ufficio Privato', value: 'UFF_PRIVATO' },
  { title: 'Sala Riunioni', value: 'SALA_RIUNIONI' },
  { title: 'Tutti', value: 'ALL' },
]

const loadDisponibilita = async () => {
  try {
      const response: any = await CoWorkingService.getDisponibilitaCompleta(periodoSelezionato.value, tipologiaSelezionata.value)
      if(response && response.data){
        console.log('Disponibilità caricata:', response.data)
        items.value = response.data
      }

    } catch (error) {
      console.error('Errore caricamento disponibilità:', error)
    }
};

const loadServiziPresenti = async () => {
  try {
      const response = await CoWorkingService.getServizi()
      servizi.value = response.data
      if(servizi.value.length > 0 ){
        let coWorkIndex = servizi.value.findIndex(s => s.key === "COWORK_BASE")
        tipologiaSelezionata.value = servizi.value[coWorkIndex].id
        loadDisponibilita()
      }

    } catch (error) {
      console.error('Errore caricamento servizi:', error)
      servizi.value = []
    }
};

const headers = [
  { title: 'Data', key: 'date' },
  { title: 'Nome Servizio', key: 'nomeServizio' },
  { title: 'Disponibilità mattina', key: 'dispMattina' },
  { title: 'Disponibilità pomeriggio', key: 'dispPomeriggio' },
  { title: 'Azioni', key: 'azioni', width: '150', align: 'center' },
] as any
</script>
