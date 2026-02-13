<script setup lang="ts">
import { onMounted, inject, ref } from 'vue'
import CoWorkingService from '@/services/CoWorkingService'
import { useAlert} from '@/shared/state/alert'

const selectedUserID = inject('selectedUserID') as any

onMounted(() => {
  loadDati()
})  

const items = ref([]) as any

const loadDati = async () => {
  const response = await CoWorkingService.getNextUserCoWorkings(selectedUserID?.value)
  if(response.status == 200){
    items.value = response.data
  }
}

const headers = [
  {
    title: 'Data',
    key: 'data',
  },
  {
    title: 'Spazio',
    key: 'spazio',
  },
  {
    title: 'Turno',
    key: 'turno',
    value: (item: any) => {
        if (item.flgMattina && item.flgPomeriggio) return 'Giornata Intera'
        if (item.flgMattina) return 'Mattina'
        if (item.flgPomeriggio) return 'Pomeriggio'
        return ''
    }
  },{
    title: 'Servizi aggiuntivi',
    key: 'servizi',
    align:'center',
    value: (item: any) => {
        if(item.servizi.length >0){
          let serviziAggiuntivi:string = item.servizi.filter((s: any) => s.key !== 'COWORK_BASE' && s.key !== 'UFF_PRIVATO' && s.key !== 'SALA_RIUNIONI').map((s: any) => s.nome).join(', ')
          return serviziAggiuntivi.length > 0 ? serviziAggiuntivi : 'No'
        }
        return 'No'
    }
  },
  {
    title: 'Azioni',
    key: 'azioni',
    align:'center'
  }
] as any
const { show: showAlert } = useAlert()
const dettaglioPrenotazione = (item: any) => {
    showAlert('Informazioni di Accesso', 'Password wifi: ' + item.wifiAccess + ' - Pin Accesso: ' + item.pin,'info' )
}

</script>

<template>
  <VCard title="Prossime Prenotazioni">
    <VDataTable
      :headers="headers"
      :items="items"
      :items-per-page="5"
      class="text-no-wrap rounded-0"
    >
        <template #item.data="{ item }">
            {{ new Date((item as any).data).toLocaleDateString() }}
        </template>
        <template #item.spazio="{ item }">
            <VChip v-if="(item as any).servizi.find((s: any) => s.key === 'COWORK_BASE') !== undefined" label size="small" color="primary" >
                COWORK
            </VChip>
            <VChip v-if="(item as any).servizi.find((s: any) => s.key === 'UFF_PRIVATO') !== undefined" label size="small" color="secondary" >
                UFFICIO PRIVATO
            </VChip>
            <VChip v-if="(item as any).servizi.find((s: any) => s.key === 'SALA_RIUNIONI') !== undefined" label size="small" color="success" >
                SALA RIUNIONI
            </VChip>
          </template>  
          <template #item.azioni="{ item }">
      
            
            <IconBtn size="small" color="primary" @click="dettaglioPrenotazione(item)">
                <VIcon icon="ri-search-ai-2-line" />
            </IconBtn>
          </template>
  </VDataTable>

    
  </VCard>
</template>
