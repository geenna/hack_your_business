<script setup lang="ts">
import UserList from '@/views/pages/users/UserList.vue'
import UserDetail from '@/views/pages/users/UserDetail.vue'
import { UserProperties } from '@/types/UserProperties'
import UserService from '@/services/UserService'
const currentTab = ref("lista-utenti")

const selectedUserID = ref()
provide('selectedUserID', selectedUserID)

const onDetailUser = (userID: string) => {
    currentTab.value = 'dettaglio-utente'
    selectedUserID.value = userID
}

onMounted(() => {
    getUser()
})

const getUser = async () => {
    const response = await UserService.getAllUsers()
    users.value = response.data
}

const users: Ref<UserProperties[]> = ref<UserProperties[]>([])
provide('users', users)

const onBack = (refresh: boolean | undefined) => {
    currentTab.value = 'lista-utenti'
    selectedUserID.value = null
    if(refresh){
        getUser()
    }
}
</script>

<template>
  <VWindow v-model="currentTab">
    <VWindowItem value="lista-utenti">
        <UserList @onDetailUser="onDetailUser" />
    </VWindowItem>

    <VWindowItem value="dettaglio-utente">
        <UserDetail @onBack="onBack"/>
    </VWindowItem>
    </VWindow>
</template>
