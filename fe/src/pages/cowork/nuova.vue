<script setup lang="ts">
import { ref, provide } from 'vue'
import googleHome from '@images/pages/google-home.png'
import iphone11 from '@images/pages/iphone-11.png'
import customAddress from '@images/svg/address.svg'
import customCart from '@images/svg/cart.svg'
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
    icon: customCart,
  },
  {
    title: 'Scegli la data',
    icon: customAddress,
  },
  {
    title: 'User',
    icon: customAddress,
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
  currentStep.value = 1
}

const onSelezionaGiorno = () => {
  console.log(nuovaPrenotazione.value)
  currentStep.value = 2
}
const onAddUser = (user: any) => {
    nuovaPrenotazione.value.userId = user.id
    console.log(nuovaPrenotazione.value)
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
    console.log(nuovaPrenotazione.value)
    CoWorkingService.createPrenotazione(nuovaPrenotazione.value)
      .then((response:any) => {
        if(response.status === 200){
            currentStep.value = 4

        }
    }).catch((error:any) => {
        console.error('Errore salvataggio prenotazione:', error)
    })
}

onMounted(() => {
  loadServizi()
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
        :isActiveStepValid=true
      />
    </VCardText>

    <VDivider />

    <VCardText>
      <!-- 👉 stepper content -->
      <VWindow
        v-model="currentStep"
        class="disable-tab-transition"
        :touch="false"
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
         BBB
        </VWindowItem>
      </VWindow>
    </VCardText>
  </VCard>
</template>
