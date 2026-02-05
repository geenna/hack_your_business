<script setup lang="ts">
import emptyCartImg from '@images/pages/empty-cart.png'
import { ServiziModel } from '@/types/ServiziModel'

const props = defineProps<{
  servizi: ServiziModel[]
}>()

const emit = defineEmits(['onSelezionaSpazio'])

const selectSpace = (idServizio: string, keyServizio: string) => {
  emit('onSelezionaSpazio', idServizio, keyServizio)
}
</script>

<template>
  <VRow>
    <VCol
      cols="12"
      md="12"
    >
      <!-- 👉 Offers alert -->
      <VAlert
        color="success"
        variant="tonal"
        icon="ri-percent-line"
        closable
      >
        <VAlertTitle class="text-success mb-1">
          Promozioni
        </VAlertTitle>

        <p class="mb-0">
          - 5% Se prenoti per più di 5 giorni.
        </p>
        <p class="mb-0">
          - 15% Se prenoti per più di 15 giorni.
        </p>
      </VAlert>

      <h5 class="text-h5 my-4">
        Seleziona lo spazio preferito
      </h5>

      <!-- 👉 Cart items -->
      <div class="border rounded">
          <div 
            v-for="servizio in props.servizi.filter((servizio) => servizio.key === 'COWORK_BASE' || servizio.key === 'UFF_PRIVATO' || servizio.key === 'SALA_RIUNIONI')">
             
            <div  class="d-flex align-center gap-3 pa-5 position-relative flex-column flex-sm-row" :class="0 ? 'border-t' : ''" v-if="servizio.key === 'COWORK_BASE'">
                  <div>
                    <VImg
                      width="140"
                      height="140"
                      :src="emptyCartImg"
                      alt="Product Image"
                    />
                  </div>

                  <div class="d-flex w-100">
                    <div>
                      <h6 class="text-h6 mb-2">
                      Postazione singola coworking
                      </h6>
                      <div class="d-flex align-center text-no-wrap gap-2 text-base">
                        <span class="text-disabled">Servizi inclusi</span>
                        <VChip
                          color="primary"
                          size="small"
                        >
                        Wifi
                        </VChip>
                      </div>

                      <div class="my-2">
                      Descrizione spazio
                      </div>
                    </div>

                    <VSpacer />

                    <div
                      class="d-flex flex-column mt-5"
                    >
                      <p class="text-base" style="width: 140px;">
                        <span class="text-primary">{{ servizio.costoIntero }}€ al giorno</span>
                        <br>
                        <span class="text-primary">{{ servizio.costoRidotto }}€ mezza giornata</span>
                      </p>

                      <div>
                        <VBtn
                          size="small"
                          variant="outlined"
                          @click="selectSpace(servizio.id, servizio.key)"
                        >
                          Seleziona
                        </VBtn>
                      </div>
                    </div>
                  </div>
            </div>



                <div  class="d-flex align-center gap-3 pa-5 position-relative flex-column flex-sm-row" :class="0 ? 'border-t' : ''" v-if="servizio.key === 'UFF_PRIVATO'">
                  <div>
                    <VImg
                      width="140"
                      height="140"
                      :src="emptyCartImg"
                      alt="Product Image"
                    />
                  </div>

                  <div class="d-flex w-100">
                    <div>
                      <h6 class="text-h6 mb-2">
                      Ufficio privato
                      </h6>
                      <div class="d-flex align-center text-no-wrap gap-2 text-base">
                        <span class="text-disabled">Servizi inclusi</span>
                        <VChip
                          color="primary"
                          size="small"
                        >
                        Wifi
                        </VChip>
                        <VChip
                          color="primary"
                          size="small"
                        >
                        Stanza singola
                        </VChip>
                      </div>

                      <div class="my-2">
                      Descrizione spazio
                      </div>
                    </div>

                    <VSpacer />

                    <div
                      class="d-flex flex-column mt-5"
                    >
                      <p class="text-base" style="width: 140px;">
                        <span class="text-primary">{{ servizio.costoIntero }}€ al giorno</span>
                      </p>

                      <div>
                        <VBtn
                          size="small"
                          variant="outlined"
                          @click="selectSpace(servizio.id, servizio.key)"  
                        >
                          Seleziona
                        </VBtn>
                      </div>
                    </div>
                  </div>
                </div>

                <div  class="d-flex align-center gap-3 pa-5 position-relative flex-column flex-sm-row" :class="0 ? 'border-t' : ''" v-if="servizio.key === 'SALA_RIUNIONI'">
                  <div>
                    <VImg
                      width="140"
                      height="140"
                      :src="emptyCartImg"
                      alt="Product Image"
                    />
                  </div>

                  <div class="d-flex w-100">
                    <div>
                      <h6 class="text-h6 mb-2">
                      Sala Riunioni
                      </h6>
                      <div class="d-flex align-center text-no-wrap gap-2 text-base">
                        <span class="text-disabled">Servizi inclusi</span>
                        <VChip
                          color="primary"
                          size="small"
                        >
                        Wifi
                        </VChip>
                        <VChip
                          color="primary"
                          size="small"
                        >
                        Stanza singola
                        </VChip> <VChip
                          color="primary"
                          size="small"
                        >
                        Fino a 12 persone
                        </VChip>
                      </div>

                      <div class="my-2">
                      Descrizione spazio
                      </div>
                    </div>

                    <VSpacer />

                    <div
                      class="d-flex flex-column mt-5"
                    >
                      <p class="text-base" style="width: 140px;">
                        <span class="text-primary">{{ servizio.costoIntero }}€ al giorno</span>
                      </p>

                      <div>
                        <VBtn
                          size="small"
                          variant="outlined"
                          @click="selectSpace(servizio.id, servizio.key)"
                        >
                          Seleziona
                        </VBtn>
                      </div>
                    </div>
                  </div>
                </div>
          
          
       

        
          </div>
        
      </div>


    </VCol>


  </VRow>
</template>

<style lang="scss">
.checkout-item-remove-btn {
  position: absolute;
  inset-block-start: 10px;
  inset-inline-end: 10px;
}
</style>
