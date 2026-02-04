<script setup lang="ts">
import emptyCartImg from '@images/pages/empty-cart.png'
import { ref, computed } from 'vue'

const emit = defineEmits(['onSelezionaSpazio'])

const selectSpace = (space: string) => {
  emit('onSelezionaSpazio', space)
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
          - 5% Se prenoti per più di 5 giorni consecutivi.
        </p>
        <p class="mb-0">
          - 15% Se prenoti per più di 15 giorni consecutivi.
        </p>
      </VAlert>

      <h5 class="text-h5 my-4">
        Seleziona lo spazio preferito
      </h5>

      <!-- 👉 Cart items -->
      <div class="border rounded">
          <div
            class="d-flex align-center gap-3 pa-5 position-relative flex-column flex-sm-row"
            :class="0 ? 'border-t' : ''"
          >
            <IconBtn
              size="x-small"
              class="checkout-item-remove-btn"
              color="disabled"
            >
              <VIcon
                size="18"
                icon="ri-close-line"
              />
            </IconBtn>

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
                  <span class="text-primary">10€ al giorno</span>
                  <br>
                  <span class="text-primary">9€ mezza giornata</span>
                </p>

                <div>
                  <VBtn
                    size="small"
                    variant="outlined"
                     @click="selectSpace('postazione-singola')"
                  >
                    Seleziona
                  </VBtn>
                </div>
              </div>
            </div>
          </div>
             <div
            class="d-flex align-center gap-3 pa-5 position-relative flex-column flex-sm-row"
            :class="0 ? 'border-t' : ''"
          >
            <IconBtn
              size="x-small"
              class="checkout-item-remove-btn"
              color="disabled"
            >
              <VIcon
                size="18"
                icon="ri-close-line"
              />
            </IconBtn>

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
                  <span class="text-primary">40€ al giorno</span>
                </p>

                <div>
                  <VBtn
                    size="small"
                    variant="outlined"
                    @click="selectSpace('ufficio-privato')"  
                  >
                    Seleziona
                  </VBtn>
                </div>
              </div>
            </div>
          </div>
              <div
            class="d-flex align-center gap-3 pa-5 position-relative flex-column flex-sm-row"
            :class="0 ? 'border-t' : ''"
          >
            <IconBtn
              size="x-small"
              class="checkout-item-remove-btn"
              color="disabled"
            >
              <VIcon
                size="18"
                icon="ri-close-line"
              />
            </IconBtn>

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
                  <span class="text-primary">140€ al giorno</span>
                </p>

                <div>
                  <VBtn
                    size="small"
                    variant="outlined"
                    @click="selectSpace('sala-riunioni')"
                  >
                    Seleziona
                  </VBtn>
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
