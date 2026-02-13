<script setup lang="ts">
import type { Options } from 'flatpickr/dist/types/options'
import { PerfectScrollbar } from 'vue3-perfect-scrollbar'
import { VForm } from 'vuetify/components/VForm'

import type { Event, NewEvent } from '@/types/CalendarEvent'
import { useCalendarStore } from './useCalendarStore'
import UserService from '@/services/UserService'

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'update:isDrawerOpen', val: boolean): void
  (e: 'addEvent', val: NewEvent): void
  (e: 'updateEvent', val: Event): void
  (e: 'removeEvent', eventId: string): void
}>()

interface Props {
  isDrawerOpen: boolean
  event: (Event | NewEvent)
}

// 👉 store
const store = useCalendarStore()
const refForm = ref<VForm>()

// 👉 Event
const event = ref<Event>(JSON.parse(JSON.stringify(props.event)))

const resetEvent = () => {
  event.value = JSON.parse(JSON.stringify(props.event))
  nextTick(() => {
    refForm.value?.resetValidation()
  })
}

watch(() => props.isDrawerOpen, resetEvent)

const removeEvent = () => {
  emit('removeEvent', String((event.value as Event).id))

  // Close drawer
  emit('update:isDrawerOpen', false)
}

const handleSubmit = () => {
  refForm.value?.validate()
    .then(({ valid }) => {
      if (valid) {
        // If id exist on id => Update event
        if ('id' in event.value)
          emit('updateEvent', event.value)

        // Else => add new event
        else emit('addEvent', event.value)

        // Close drawer
        emit('update:isDrawerOpen', false)
      }
    })
}
const guestsOptions = ref<Array<{
  name: string
  idUtente: string
}>>([])

onMounted(() => {
  UserService.getCollaborators()
    .then(response => {
      if(response.status === 200){
        response.data.forEach((user: any) => {
          guestsOptions.value.push({
            name: user.nome[0].toUpperCase() + '. ' + user.cognome,
            idUtente: user.id,
          })
        })
      }
    })
})




// 👉 Form

const onCancel = () => {
  emit('update:isDrawerOpen', false)

  nextTick(() => {
    refForm.value?.reset()
    resetEvent()
    refForm.value?.resetValidation()
  })
}

const startDateTimePickerConfig = computed(() => {
  const config: Options = { enableTime: !event.value.allDay, dateFormat: `Y-m-d${event.value.allDay ? '' : ' H:i'}` }

  if (event.value.end)
    config.maxDate = event.value.end

  return config
})

const endDateTimePickerConfig = computed(() => {
  const config: Options = { enableTime: !event.value.allDay, dateFormat: `Y-m-d${event.value.allDay ? '' : ' H:i'}` }

  if (event.value.start)
    config.minDate = event.value.start

  return config
})

const dialogModelValueUpdate = (val: boolean) => {
  emit('update:isDrawerOpen', val)
}
</script>

<template>
  <VNavigationDrawer
    data-allow-mismatch
    temporary
    location="end"
    :model-value="props.isDrawerOpen"
    width="420"
    class="scrollable-content"
    @update:model-value="dialogModelValueUpdate"
  >
    <!-- 👉 Header -->
    <AppDrawerHeaderSection
      :title="event.id ? 'Aggiorna Evanto' : 'Crea Evento'"
      @cancel="$emit('update:isDrawerOpen', false)"
    >
      <template #beforeClose>
        <IconBtn
          v-show="event.id"
          @click="removeEvent"
        >
          <VIcon
            size="18"
            icon="ri-delete-bin-7-line"
          />
        </IconBtn>
      </template>
    </AppDrawerHeaderSection>

    <VDivider />

    <PerfectScrollbar :options="{ wheelPropagation: false }">
      <VCard flat>
        <VCardText>
          <!-- SECTION Form -->
          <VForm
            ref="refForm"
            @submit.prevent="handleSubmit"
          >
            <VRow>
              <!-- 👉 Title -->
              <VCol cols="12">
                <VTextField
                  id="event-title"
                  v-model="event.title"
                  label="Titolo"
                  placeholder="Incontro evento"
                  :rules="[requiredValidator]"
                />
              </VCol>

              <!-- 👉 Calendar -->
              <VCol cols="12">
                <VSelect
                  id="event-label"
                  v-model="event.extendedProps.calendar"
                  label="Destinatari"
                  :rules="[requiredValidator]"
                  :items="store.availableCalendars"
                  :item-title="item => item.label"
                  :item-value="item => item.label"
                >
                  <template #selection="{ item }">
                    <div
                      v-show="event.extendedProps.calendar"
                      class="align-center"
                      :class="event.extendedProps.calendar ? 'd-flex' : ''"
                    >
                      <VIcon
                        size="8"
                        icon="ri-circle-fill"
                        :color="item.raw.color"
                        class="me-2"
                      />
                      <span>{{ item.raw.label }}</span>
                    </div>
                  </template>

                  <template #item="{ item, props: itemProps }">
                    <VListItem v-bind="itemProps">
                      <template #prepend>
                        <VIcon
                          size="8"
                          icon="ri-circle-fill"
                          :color="item.raw.color"
                        />
                      </template>
                    </VListItem>
                  </template>
                </VSelect>
              </VCol>
              <!-- 👉 Guests -->
              <VCol cols="12">
                <VSelect
                  id="event-guests"
                  v-if="event.extendedProps.calendar === 'Collaboratori'"
                  v-model="event.extendedProps.guests"
                  label="Invitati"
                  placeholder="Seleziona invitati"
                  :items="guestsOptions"
                  :item-title="item => item.name"
                  :item-value="item => item.idUtente"
                  chips
                  multiple
                  eager
                />
              </VCol>

              <!-- 👉 All day -->
              <VCol cols="12">
                <VSwitch
                  id="event-all-day"

                  v-model="event.allDay"
                  label="Tutto il giorno"
                />
              </VCol>

              <!-- 👉 Start date -->
              <VCol cols="12">
                <AppDateTimePicker
                  id="event-start-date"
                  :key="JSON.stringify(startDateTimePickerConfig)"
                  v-model="event.start"
                  :rules="[requiredValidator]"
                  label="Data inizio"
                  placeholder="Seleziona data"
                  :config="startDateTimePickerConfig"
                />
              </VCol>

              <!-- 👉 End date -->
              <VCol cols="12">
                <AppDateTimePicker
                  id="event-end-date"
                  :key="JSON.stringify(endDateTimePickerConfig)"
                  v-model="event.end"
                  :rules="[requiredValidator]"
                  label="Data fine"
                  placeholder="Seleziona data fine"
                  :config="endDateTimePickerConfig"
                />
              </VCol>



              <!-- 👉 Event URL -->
              <VCol cols="12">
                <VTextField
                  id="event-url"

                  v-model="event.url"
                  label="Link evento"
                  placeholder="https://meet.google.com/xyz"
                  :rules="[urlValidator]"
                  type="url"
                />
              </VCol>

             
              <!-- 👉 Location -->
              <VCol cols="12">
                <VTextField
                  id="event-location"
                  v-model="event.extendedProps.location"
                  label="Luogo"
                  placeholder="Sala riunioni"
                />
              </VCol>

              <!-- 👉 Description -->
              <VCol cols="12">
                <VTextarea
                  id="event-description"
                  v-model="event.extendedProps.description"
                  label="Descrizione"
                  placeholder="Descrizione evento"
                />
              </VCol>

              <!-- 👉 Form buttons -->
              <VCol cols="12">
                <VBtn
                  type="submit"
                  class="me-3"
                >
                  Salva
                </VBtn>
                <VBtn
                  variant="outlined"
                  color="secondary"
                  @click="onCancel"
                >
                  Annulla
                </VBtn>
              </VCol>
            </VRow>
          </VForm>
        <!-- !SECTION -->
        </VCardText>
      </VCard>
    </PerfectScrollbar>
  </VNavigationDrawer>
</template>
