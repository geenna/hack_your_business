<template>
  <VRow>
    <VCol cols="12">
      <VCard title="Prenotazioni">
        <template #append>  
            <AppDateTimePicker
              width="200px"
              v-model="date"
              label="Data"
              placeholder="Seleziona la data"
             :config="{ mode: 'single', format: 'dd/MM/yyyy' }"

            />
            <VBtn class="ml-4" color="primary" @click="cerca">Cerca</VBtn>

        </template>
     
        <!-- SECTION Datatable -->
        <VDataTable
          
          :headers="headers"
          :items="prenotazioni"
          item-value="name"
          class="rounded-0"
        >
          <template #item.data="{ item }">
            {{ new Date(item.data).toLocaleDateString() }}
          </template>
          <template #item.spazio="{ item }">
            <VChip v-if="item.servizi.find((s: any) => s.key === 'COWORK_BASE') !== undefined" label size="small" color="primary" >
                COWORK
            </VChip>
            <VChip v-if="item.servizi.find((s: any) => s.key === 'UFF_PRIVATO') !== undefined" label size="small" color="secondary" >
                UFFICIO PRIVATO
            </VChip>
            <VChip v-if="item.servizi.find((s: any) => s.key === 'SALA_RIUNIONI') !== undefined" label size="small" color="success" >
                SALA RIUNIONI
            </VChip>
          </template>
          <template #item.dettagli="{ item }">
            <IconBtn @click="eliminaPrenotazione(item)" size="x-small" color="error">
                <VIcon
                    icon="ri-delete-bin-line"
                    size="20"
                />
            </IconBtn>
            <IconBtn @click="detailPrenotazione(item)" size="x-small" color="primary" class="ml-2">
               <VIcon
                icon="ri-search-ai-2-line"
                size="20"
              />
            </IconBtn>
          </template>
          <template #bottom />
        </VDataTable>
        <!-- !SECTION -->
      </VCard>
    </VCol>
</VRow>
</template>

<style lang="scss" scoped>
.card-list {
  --v-card-list-gap: 16px;
}
</style>


<script setup lang="ts">
import CoWorkingService from '@/services/CoWorkingService';
import { useAlert} from '@/shared/state/alert';
import { useConfirm } from '@/shared/state/confirm';
import type { PrenotazioneCoWorkDetail } from '@/types/PrenotazioneCoWorkDetail';
import { toDateOnlyISO } from '@/utils/utility';

const prenotazioni = ref<PrenotazioneCoWorkDetail[]>([])
const date = ref(new Date())
const { show: showAlert } = useAlert()
const { show: showConfirm } = useConfirm()

const eliminaPrenotazione = async (item: PrenotazioneCoWorkDetail) => {
  const confirmed = await showConfirm('Conferma eliminazione', 'Sei sicuro di voler eliminare questa prenotazione?')
  if (confirmed) {
      CoWorkingService.eliminaPrenotazione(item.id).then(() => {
          cerca()
      })
  }
}

const detailPrenotazione = (item: PrenotazioneCoWorkDetail) => {
  showAlert('Informazioni di Accesso', 'Password wifi: ' + item.wifiAccess + ' - Pin Accesso: ' + item.pin,'info' )
}

onMounted(() => {
  cerca()
})

const cerca = () => {
  const params = toDateOnlyISO(new Date(date.value))
  CoWorkingService.getPrenotazioni(params).then(response => {
    prenotazioni.value = response.data
  })
}

const headers = [
  {
    title: 'Data',
    key: 'data',
    width: '150px',
  },
    {
    title: 'Nome',
    key: 'user.nome',
  },
  {
    title: 'Cognome',
    key: 'user.cognome',
  },{
    title: 'Email',
    key: 'user.email',
  },

  {
    title: 'Turno',
    key: 'turno',
    value: (item: PrenotazioneCoWorkDetail) => {
        if (item.flgMattina && item.flgPomeriggio) return 'Giornata Intera'
        if (item.flgMattina) return 'Mattina'
        if (item.flgPomeriggio) return 'Pomeriggio'
        return ''
    }
  },
  {
    title: 'Spazio',
    key: 'spazio',
    align: 'center'
    
  },
  {
    title: 'Dettagli',
    key: 'dettagli',
    width: '150px',
    
  },
] as any

</script>
