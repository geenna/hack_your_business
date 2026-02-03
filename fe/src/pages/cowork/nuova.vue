<script setup lang="ts">
import { ref } from 'vue'
import googleHome from '@images/pages/google-home.png'
import iphone11 from '@images/pages/iphone-11.png'
import customAddress from '@images/svg/address.svg'
import customCart from '@images/svg/cart.svg'
import customPayment from '@images/svg/payment.svg'
import customTrending from '@images/svg/trending.svg'
import SceltaSpazioPage from '@/views/pages/cowork/nuova-prenotazione/SceltaSpazioPage.vue'

const checkoutSteps = [
  {
    title: 'Scegli il tuo spazio',
    icon: customCart,
  },
  {
    title: 'Scelta la data',
    icon: customAddress,
  },
  {
    title: 'Scegli l\'utente',
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



const currentStep = ref(0)
</script>

<template>
  <VCard>
    <VCardText>
      <!-- 👉 Stepper -->
      <AppStepper
        v-model:current-step="currentStep"
        :items="checkoutSteps"
        :direction="$vuetify.display.mdAndUp ? 'horizontal' : 'vertical'"
        :isActiveStepValid="false"
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
         <SceltaSpazioPage />
        </VWindowItem>

        <VWindowItem>

        </VWindowItem>

        <VWindowItem>
BB
        </VWindowItem>

        <VWindowItem>
          <PaymentContent
            v-model:current-step="currentStep"
          />
        </VWindowItem>

        <VWindowItem>
         BBB
        </VWindowItem>
      </VWindow>
    </VCardText>
  </VCard>
</template>
