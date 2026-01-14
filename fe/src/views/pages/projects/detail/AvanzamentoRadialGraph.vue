<script setup lang="ts">
import { useTheme } from 'vuetify'
import { hexToRgb } from '@core/utils/colorConverter'

const vuetifyTheme = useTheme()



const props = withDefaults(defineProps<{
  avanzamento: number
}>(), {
  avanzamento: 0,
})
const series = [props.avanzamento]


const chartOptions = computed(() => {
  const currentTheme = vuetifyTheme.current.value.colors
  const variableTheme = vuetifyTheme.current.value.variables

  return {
    chart: {
      sparkline: {
        enabled: true,
      },
    },
    colors: [currentTheme.info],
    plotOptions: {
      radialBar: {
        startAngle: -90,
        endAngle: 90,
        hollow: {
          size: '65%',
        },
        dataLabels: {
          name: {
            show: false,
          },
          value: {
            fontSize: '1.125rem',
            fontWeight: '500',
            offsetY: 0,
            color: `rgba(${hexToRgb(currentTheme['on-surface'])},${variableTheme['medium-emphasis-opacity']})`,
          },
        },
        track: {
          background: currentTheme['track-bg'],
        },
      },
    },
    stroke: {
      lineCap: 'round',
    },
    responsive: [
      {
        breakpoint: 450,
        options: {
          plotOptions: {
            radialBar: {
              hollow: {
                size: '52%',
              },
            },
          },
        },
      },
    ],
  }
})
</script>

<template>
  <div class="text-center">
      <h5 class="text-h5">
        Percentuale completamento progetto
      </h5>
      <VueApexCharts
        id="stats-radial-bar-chart"
        :options="chartOptions"
        :series="series"
        type="radialBar"
        :height="150"
      />
  </div>
</template>
