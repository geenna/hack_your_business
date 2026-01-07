<script setup lang="ts">

import UserService from '@/services/UserService'

const selectedUserID = inject('selectedUserID') as Ref<string>
const userData = ref()

watch(selectedUserID, async (newId) => {
  debugger
    if (newId) {
        const response = await UserService.detailUser(newId)
        userData.value = response.data
    }
}, { immediate: true })
</script>

<template>
  <VCard v-if="userData">
    <VCardText>
        <pre>{{ userData }}</pre>
    </VCardText>
  </VCard>
</template>
