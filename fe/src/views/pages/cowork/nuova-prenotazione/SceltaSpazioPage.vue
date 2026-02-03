<script setup lang="ts">
import emptyCartImg from '@images/pages/empty-cart.png'
import { ref, computed } from 'vue'

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

            <div
              class="d-flex w-100"
              :class="(($vuetify.display.width <= 1280 && $vuetify.display.width >= 960) || $vuetify.display.width <= 700) ? 'flex-column' : 'flex-row'"
            >
              <div>
                <h6 class="text-h6 mb-2">
                 ewqeqwe
                </h6>
                <div class="d-flex align-center text-no-wrap gap-2 text-base">
                  <span class="text-disabled">Sold by:</span>
                  <span class="text-primary">eqweqw</span>
                  <VChip
                    color="success"
                    size="small"
                  >
                   'In Stock'
                  </VChip>
                </div>

                <div class="my-2">
                  <VRating
                    :model-value=4
                    size="24"
                  />
                </div>

                <VTextField
                  type="number"
                  density="compact"
                  style="inline-size: 7.5rem;"
                />
              </div>

              <VSpacer />

              <div
                class="d-flex flex-column mt-5"
                :class="(($vuetify.display.width <= 1280 && $vuetify.display.width >= 960) || $vuetify.display.width <= 700) ? 'text-start' : 'text-end'"
              >
                <p class="text-base">
                  <span class="text-primary">312312</span>
                  <span>/</span>
                  <span class="text-decoration-line-through">321312</span>
                </p>

                <div>
                  <VBtn
                    size="small"
                    variant="outlined"
                  >
                    move to wishlist
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

            <div
              class="d-flex w-100"
              :class="(($vuetify.display.width <= 1280 && $vuetify.display.width >= 960) || $vuetify.display.width <= 700) ? 'flex-column' : 'flex-row'"
            >
              <div>
                <h6 class="text-h6 mb-2">
                 Spazio coworking
                </h6>
                <div class="d-flex align-center text-no-wrap gap-2 text-base">

                  <VChip
                    color="success"
                    size="small"
                  >
                    Wifi incluso
                  </VChip>
                </div>

                <div class="my-2">
                  <VRating
                    :model-value=4
                    size="24"
                  />
                </div>


              </div>

              <VSpacer />

              <div
                class="d-flex flex-column mt-5"
                :class="(($vuetify.display.width <= 1280 && $vuetify.display.width >= 960) || $vuetify.display.width <= 700) ? 'text-start' : 'text-end'"
              >
                <p class="text-base">
                  <span class="text-primary">312312</span>
                  <span>/</span>
                  <span class="text-decoration-line-through">321312</span>
                </p>

                <div>
                  <VBtn
                    size="small"
                    variant="outlined"
                  >
                    move to wishlist
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
