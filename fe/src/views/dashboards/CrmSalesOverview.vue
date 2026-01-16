<template>
  <VCard>
    <VCardItem>
      <VCardTitle>Progetti</VCardTitle>

    </VCardItem>

    <VCardText class="pt-5">
      <div class="d-flex gap-6 flex-md-row flex-column">
        <div class="mx-auto">
          <VueApexCharts
            type="donut"
            :options="options"
            :series="[props.numInScadenza, props.numScaduti, props.numInCorso, props.numCompletati]"
            :height="220"
            :width="220"
          />
        </div>

        <div>
          <div class="d-flex align-center">
            <div class="me-3">
              <VAvatar
                rounded
                color="primary"
                variant="tonal"
              >
                <VIcon icon="ri-wallet-line" />
              </VAvatar>
            </div>
            <div>
              <p class="mb-0">
                Tot. Progetti
              </p>
              <h5 class="text-h5">
               {{ props.numInCorso + props.numInScadenza + props.numScaduti + props.numCompletati }}
              </h5>
            </div>
          </div>
          <VDivider class="my-6" />

          <div>
            <VRow>
              <VCol
                cols="6"
              >
                <div class="d-flex align-center mb-1">
                  <VIcon
                    icon="ri-circle-fill"
                    color="primary"
                    size="10"
                    class="me-2"
                  />
                  <div
                    class="text-truncate"
                    style="max-inline-size: 85px;"
                  >
                    Completati
                  </div>
                </div>
                <h6 class="text-h6 text-medium-emphasis">
                  {{ props.numCompletati }}
                </h6>
              </VCol>
              <VCol
                cols="6"
              >
                <div class="d-flex align-center mb-1">
                  <VIcon
                    icon="ri-circle-fill"
                    color="primary"
                    size="10"
                    class="me-2"
                  />
                  <div
                    class="text-truncate"
                    style="max-inline-size: 85px;"
                  >
                    In Scadenza
                  </div>
                </div>
                <h6 class="text-h6 text-medium-emphasis">
                  {{ props.numInScadenza }}
                </h6>
              </VCol>
              <VCol
                cols="6"
              >
                <div class="d-flex align-center mb-1">
                  <VIcon
                    icon="ri-circle-fill"
                    color="primary"
                    size="10"
                    class="me-2"
                  />
                  <div
                    class="text-truncate"
                    style="max-inline-size: 85px;"
                  >
                    Scaduti
                  </div>
                </div>
                <h6 class="text-h6 text-medium-emphasis">
                  {{ props.numScaduti }}
                </h6>
              </VCol>
              <VCol
                cols="6"
              >
                <div class="d-flex align-center mb-1">
                  <VIcon
                    icon="ri-circle-fill"
                    color="primary"
                    size="10"
                    class="me-2"
                  />
                  <div
                    class="text-truncate"
                    style="max-inline-size: 85px;"
                  >
                    In Corso
                  </div>
                </div>
                <h6 class="text-h6 text-medium-emphasis">
                  {{ props.numInCorso }}
                </h6>
              </VCol>
            </VRow>
          </div>
        </div>
      </div>
    </VCardText>
  </VCard>
</template>
<script setup lang="ts">
import { useTheme } from 'vuetify'
import { hexToRgb } from '@core/utils/colorConverter'


interface Props {
  numInCorso: number
  numInScadenza: number
  numScaduti: number
  numCompletati: number
}

const props = withDefaults(defineProps<Props>(), {
  numInCorso: 0 ,
  numInScadenza: 0,
  numScaduti: 0,
  numCompletati: 0
})


const vuetifyTheme = useTheme()

  const options = computed(() => {
  const currentTheme = ref(vuetifyTheme.current.value.colors)
  const variableTheme = ref(vuetifyTheme.current.value.variables)

  const secondaryTextColor = `rgba(${hexToRgb(currentTheme.value['on-surface'])},${variableTheme.value['medium-emphasis-opacity']})`
  const primaryTextColor = `rgba(${hexToRgb(currentTheme.value['on-surface'])},${variableTheme.value['high-emphasis-opacity']})`
  return {
    chart: {
      sparkline: { enabled: true },
    },
    colors: [
      'rgba(var(--v-theme-primary),1)',
      'rgba(var(--v-theme-primary), 0.7)',
      'rgba(var(--v-theme-primary), 0.5)',
      currentTheme.value['track-bg'],
    ],
    stroke: { width: 0 },
    legend: { show: false },
    dataLabels: { enabled: false },
    labels: ['In scadenza', 'Scaduti', 'In Corso', 'Completati'],
    states: {
      hover: {
        filter: { type: 'none' },
      },
      active: {
        filter: { type: 'none' },
      },
    },
    plotOptions: {
      pie: {
        customScale: 0.9,
        donut: {
          size: '70%',
          labels: {
            show: true,
            name: {
              offsetY: 25,
              color: secondaryTextColor,
            },
            value: {
              offsetY: -15,
              fontWeight: 500,
              fontSize: '24px',
              color: primaryTextColor,
              formatter: (value: unknown) => `${value}`,
            },
            total: {
              show: true,
              label: 'Tot. Progetti',
              fontSize: '15px',
              color: secondaryTextColor,

              formatter: (value: number) => `${props.numInScadenza + props.numScaduti + props.numInCorso + props.numCompletati}`,
            },
          },
        },
      },
    },
  }
})

const series = [12, 25, 15, 50]


</script>