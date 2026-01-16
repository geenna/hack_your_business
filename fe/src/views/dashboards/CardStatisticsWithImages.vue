<script setup lang="ts">
interface Props {
  title: string
  subtitle: string
  stats: string | number
  image: string
  color?: string
}

const props = withDefaults(defineProps<Props>(), {
  color: 'primary',
})

</script>

<template>
  <VCard class="overflow-visible position-relative">
    <div class="d-flex">
      <VCardText>
        <h6 class="text-h6 mb-5">
          {{ props.title }}
        </h6>
        <div class="d-flex align-center flex-wrap mb-3">
          <h4 class="text-h4 me-2">
            {{ props.stats }}
          </h4>
        </div>

        <VChip
          v-if="props.subtitle"
          :color="props.color"
          size="small"
        >
          {{ props.subtitle }}
        </VChip>
      </VCardText>

      <VSpacer />

      <div class="illustrator-img">
        <VImg
          v-if="props.image"
          :src="props.image"
          :width="110"
        />
      </div>
    </div>
  </VCard>
</template>

<style lang="scss">
.illustrator-img {
  position: absolute;
  inset-block-end: 0;
  inset-inline-end: 5%;
}

@media (max-width: 1200px)  and (min-width: 960px) {
  .illustrator-img {
    inset-block-end: 0;
    inset-inline-end: 0;

  }

}
</style>
