<script setup lang="ts">
import { ref, provide } from 'vue'
import userInfo from '@images/svg/user-info60.svg'
import customAddress from '@images/svg/address.svg'
import cubeSolid from '@images/svg/3d-select-solid60.svg'
import customPayment from '@images/svg/payment.svg'
import customTrending from '@images/svg/trending.svg'
import SceltaSpazioPage from '@/views/pages/cowork/nuova-prenotazione/SceltaSpazioPage.vue'
import { NuovaPrenotazioneModel } from '@/types/NuovaPrenotazioneModel'
import SelezionaGiornoPage from '@/views/pages/cowork/nuova-prenotazione/SelezionaGiornoPage.vue'
import CoWorkingService from '@/services/CoWorkingService'
import { ServiziModel } from '@/types/ServiziModel'
import CercaUtente from '@/views/pages/cowork/nuova-prenotazione/CercaUtente.vue'
import PaymentAdminPage from '@/views/pages/cowork/nuova-prenotazione/PaymentAdminPage.vue'

const checkoutSteps = [
  {
    title: 'Scegli il tuo spazio',
    icon: cubeSolid,
  },
  {
    title: 'Scegli la data',
    icon: customAddress,
  },
  {
    title: 'User',
    icon: userInfo,
  },
  {
    title: 'Payment',
    icon: customPayment,
  },
  {
    title: 'Riepilogo',
    icon: customTrending,
  },
]

const nuovaPrenotazione:Ref<NuovaPrenotazioneModel> = ref<NuovaPrenotazioneModel>({
  idServizioSelezionato: '',
  tipologia: '',
  date: [],
  turno: '',
  userId: '',
  pagamento: {}
})
provide('nuovaPrenotazione', nuovaPrenotazione)


const currentStep = ref(0)

const onSelezionaSpazio = (idServizio: string, keyServizio: string) => {
  nuovaPrenotazione.value.idServizioSelezionato = idServizio
  nuovaPrenotazione.value.tipologia = keyServizio
  maxStepAvailable.value = 1
  currentStep.value = 1
}

const onSelezionaGiorno = () => {
  console.log(nuovaPrenotazione.value)
  maxStepAvailable.value = 2
  currentStep.value = 2
}
const onAddUser = (user: any) => {
    nuovaPrenotazione.value.userId = user.id
    console.log(nuovaPrenotazione.value)
    maxStepAvailable.value = 3
    currentStep.value = 3
}
const servizi:Ref<ServiziModel[]> = ref<ServiziModel[]>([])
const loadServizi = async () => {
  try {
    const response = await CoWorkingService.getServizi()
    servizi.value = response.data
  } catch (error) {
    console.error('Errore caricamento servizi:', error)
    servizi.value = []
  }
}
const onSave = () => {
    
    CoWorkingService.createPrenotazione(nuovaPrenotazione.value)
      .then((response:any) => {
        if(response.status === 200){
            maxStepAvailable.value = 4
            currentStep.value = 4

        }
    }).catch((error:any) => {
        console.error('Errore salvataggio prenotazione:', error)
    })
}

const maxStepAvailable = ref(0)
onMounted(() => {
  loadServizi()
})
const isCurrentStepValid = ref(true)

watch(currentStep, (newStep:number, oldStep:number) => {

  if(maxStepAvailable.value == 4){
   currentStep.value = 4 
  }
  else if(newStep > maxStepAvailable.value){
    currentStep.value = oldStep
  }
})

</script>

<template>
  <VCard>
    <VCardText>
      <!-- 👉 Stepper -->
      <AppStepper
        v-model:current-step="currentStep"
        :items="checkoutSteps"
        :direction="$vuetify.display.mdAndUp ? 'horizontal' : 'vertical'"       
      />
    </VCardText>

    <VDivider />

    <VCardText>
      <!-- 👉 stepper content -->
      <VWindow
        v-model="currentStep"
        class="disable-tab-transition"
        
      >
        <VWindowItem>
         <SceltaSpazioPage @onSelezionaSpazio="onSelezionaSpazio" :servizi="servizi"/>
        </VWindowItem>

        <VWindowItem>
          <SelezionaGiornoPage @onSelezionaGiorno="onSelezionaGiorno" :servizi="servizi"/>
        </VWindowItem>

        <VWindowItem>
          <CercaUtente @onAddUser="onAddUser"/>
        </VWindowItem>

        <VWindowItem>
          <PaymentAdminPage :servizi="servizi" @onSave="onSave"/>
        </VWindowItem>

        <VWindowItem>
          <div class="text-center py-12">
            <VIcon
              size="150"
              color="success"
              icon="ri-checkbox-circle-line"
              class="mb-12"
            />
            <h5 class="text-h5 mb-2">
              Prenotazione completata con successo
            </h5>
            <p class="text-body-1">
              L'utente riceverà una email con i dettagli della prenotazione
            </p>
            <VBtn
              variant="text"
              color="primary"
              @click="$router.push('/cowork/lista')"
            >
             Vai alla lista delle prenotazioni
            </VBtn> 
          </div>
        </VWindowItem>
      </VWindow>
    </VCardText>
  </VCard>
</template>
