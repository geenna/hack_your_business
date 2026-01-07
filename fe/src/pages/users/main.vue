<script setup lang="ts">
import UserList from '@/views/pages/users/UserList.vue'
import UserDetail from '@/views/pages/users/UserDetail.vue'
const currentTab = ref("lista-utenti")

const selectedUserID = ref()
provide('selectedUserID', selectedUserID)

const onDetailUser = (userID: string) => {
    currentTab.value = 'dettaglio-utente'
    selectedUserID.value = userID
}
</script>

<template>
  <VWindow v-model="currentTab">
    <VWindowItem value="lista-utenti">
        <UserList @onDetailUser="onDetailUser" />
    </VWindowItem>

    <VWindowItem value="dettaglio-utente">
        <UserDetail />
    </VWindowItem>
    </VWindow>
</template>
