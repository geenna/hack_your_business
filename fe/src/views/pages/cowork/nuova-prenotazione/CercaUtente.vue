<template>
    <CreateUserDialog
    v-model:is-dialog-visible.capitialize="isUserCreateDialogVisible"
    :user-data="undefined"
  />
    <VCard>
        <VCardText class="d-flex align-center gap-4">
            <VSpacer />
            <VTextField
                style="max-width: 350px;"
                v-model="email"
                label="Email"
                placeholder="Inserisci email"
                density="compact"
            />
            <VBtn
                @click="cercaUtente"
            >
                Cerca
            </VBtn>
            <VBtn @click="isUserCreateDialogVisible = true">
                Aggiungi Utente
            </VBtn>
        </VCardText>
    </VCard>
    <VCard class="mt-6">
        <VCardText>
            <VDataTable
                :items="users"
                :headers="headers"
            >
             <!-- Role -->
                <template #item.userType="{ item }">
                    <div class="d-flex gap-4">
                        <VIcon
                        :icon="resolveUserRoleVariant(item.userType).icon"
                        :color="resolveUserRoleVariant(item.userType).color"
                        />
                        <span class="text-capitalize text-high-emphasis">{{ item.userType }}</span>
                    </div>
                </template>

                <template #item.user_status="{ item }">
                    <div class="d-flex gap-4">
                        <VChip
                        :color="resolveUserStatusVariant(item.user_status)"
                        size="small"
                        >
                        {{ item.user_status }}
                        </VChip>
                    </div>
                </template>

                <!-- Actions -->
                <template #item.actions="{ item }">
                    <VBtn variant="outlined" color="primary" size="small" @click="addUser(item)">
                        Seleziona
                    </VBtn>
                </template>
            </VDataTable>
        </VCardText>
    </VCard>
</template>

<script setup lang="ts">
import CreateUserDialog from '@/views/pages/users/CreateUserDialog.vue'
import UserService from '@/services/UserService'
import { resolveUserRoleVariant, resolveUserStatusVariant } from '@/utils/utility'
import { UserProperties } from '@/types/UserProperties'

const isUserCreateDialogVisible = ref(false)
const email = ref('')
const users = ref<UserProperties[]>([])
const emit = defineEmits(['onAddUser'])
const addUser = (user: any) => {
    emit('onAddUser', user)
}

const headers = [
  { title: 'NOME', key: 'nome' },
  { title: 'COGNOME', key: 'cognome' },
  { title: 'EMAIL', key: 'email' },
  { title: 'TIPO', key: 'userType' },
  { title: 'STATO', key: 'user_status' },
  { title: '', key:'actions'}
]

const cercaUtente = async () => {
    try {
        const response = await UserService.getAllUsersFromEmail(email.value)
        users.value = response.data as UserProperties[]
    } catch (error) {
        console.error(error)
    }
}
</script>