<script setup lang="ts">
import { ref } from 'vue'
import { ServiziModel } from '@/types/ServiziModel'
import { useAlert } from '@/shared/state/alert'
import { useConfirm } from '@/shared/state/confirm'
import CoWorkingService from '@/services/CoWorkingService'
import { inject, Ref } from 'vue'

const { show: showAlert } = useAlert()
const { show: showConfirm } = useConfirm()

interface Props {
  isDialogVisible: boolean
}

interface Emits {
  (e: 'update:isDialogVisible', val: boolean): void
  (e: 'submit', data: { reload:boolean }): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const serviziPresenti:Ref<ServiziModel[]> = inject('serviziPresenti') as Ref<ServiziModel[]>;
const servizioScelto:Ref<string | null> = ref(null);


const onSubmit =  async () => {
  if(!servizioScelto.value){
    showAlert('Errore', 'Il servizio scelto è obbligatorio', 'error');
    return;
  }
  if(giorniSettimanaValues.value.length === 0){
    showAlert('Errore', 'Devi selezionare almeno un giorno della settimana', 'error');
    return;
  }
  if(!dateRange.value){
    showAlert('Errore', 'Devi selezionare un intervallo di date valido', 'error');
    return;
  }
  if(mattinaValue.value <=0 && pomeriggioValue.value <=0){
    showAlert('Errore', 'Devi inserire almeno una disponibilità per mattina o pomeriggio', 'error');
    return;
  }

  try {

        const confirmed = await showConfirm(
        'Confermi l\'inserimento della disponibilità per il servizio scelto?',
        `Per le date selezionate eventuali dati presenti saranno sovrascritti?`
    )

        if (confirmed) {
            try {

              let resData = await CoWorkingService.salvaDisponibilità({
                idServizio: servizioScelto.value,
                date: dateRange.value.split(" to "),
                giorniSettimana: giorniSettimanaValues.value,
                numMattina: mattinaValue.value,
                numPomeriggio: pomeriggioValue.value,
              });
              if (resData.status === 200) {
                showAlert('Successo', 'Disponibilità salvata con successo', 'success');
                emit('submit', {
                  reload:true
                });
                closeDialog();
              } else {
                showAlert('Errore', 'Si è verificato un errore durante il salvataggio della disponibilità', 'error');
              }

            } catch (error) {
                console.error('Failed to delete document:', error)
            }
        }

    } catch (error) {

    }

  /*refForm.value?.validate().then(({ valid: isValid }) => {
    if (isValid && value.value !== null) {
      emit('submit', {
        date: date.value,
        value: value.value,
        status: status.value,
        tipoPagamento: tipoPagamento.value,
      })
      closeDialog()
    }
  })*/
}



const closeDialog = () => {
  //emit('update:isDialogVisible', false)
}


const dateRange = ref()
const giorniSettimana = [{value:0, title:'Lunedi'}, {value:1, title:'Martedi'}, {value:2, title:'Mercoledi'}, {value:3, title:'Giovedi'}, {value:4, title:'Venerdi'}, {value:5, title:'Sabato'}, {value:6, title:'Domenica'}];
const giorniSettimanaValues = ref<string[]>([]);
const mattinaValue = ref<number>(1);
const pomeriggioValue = ref<number>(1);
const onlyInt = (e: KeyboardEvent) => {
  if (!/[0-9]/.test(e.key) && e.key !== 'Backspace' && e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') {
    e.preventDefault();
  }
};
const date = ref('')
</script>

<template>
  <VDialog
    width=600
    :model-value="props.isDialogVisible"

    @update:model-value="emit('update:isDialogVisible', $event)"
  >
    <VCard class="pa-sm-11 pa-3">
      <VCardTitle class="text-h5">
        Inserisci Disponibilità
      </VCardTitle>
      <VCardText class="pt-5">
        <VRow>
          <VCol cols="12">

              <AppDateTimePicker
                class="my-6"
                v-model="dateRange"
                label="Periodo"
                placeholder="Seleziona periodo"
                :config="{ mode: 'range', format: 'd/m/Y' }"
            />
            <VSelect
              class="my-6"
              :multiple="true"
              :items="giorniSettimana"
              label="Giorni della settimana"
              v-model="giorniSettimanaValues"
              >
            </VSelect>
            <VSelect
              class="my-6"
              :items="serviziPresenti"
              label="Seleziona il servizio"
              v-model="servizioScelto"
              item-title="nome"
              item-value="id"
              >
            </VSelect>

             <VTextField
                class="my-6"
                v-model="mattinaValue"
                label="Numero disponibilità mattina"
                step="1"
                type="number"
                placeholder="1"
                @keydown="onlyInt"

              />
              <VTextField
                class="my-6"
                v-model="pomeriggioValue"
                label="Numero disponibilità pomeriggio"
                step="1"
                type="number"
                placeholder="1"
                @keydown="onlyInt"

              />

          </VCol>

        </VRow>


      </VCardText>

      <VCardActions>
        <VSpacer />
        <VBtn
          color="secondary"
          variant="tonal"
          @click="closeDialog"
        >
          Annulla
        </VBtn>
        <VBtn
          color="primary"
          variant="elevated"
          @click="onSubmit"
        >
          Salva
        </VBtn>
      </VCardActions>
    </VCard>
  </VDialog>
</template>
