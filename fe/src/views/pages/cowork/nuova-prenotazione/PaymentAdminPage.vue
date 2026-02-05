<template>
     <section class="d-flex my-6">
        
        <VRow>
            <!--SEZIONE CALENDARIO-->
            <VCol cols="12" md="8">
                
                <VCard flat variant="outlined">
                   <VCardText>
                        <AddPaymentDialogContent
                           ref="addPaymentForm"
                           @submit="onSubmit"
                           @cancel="onCancel"
                           :showVCard=false
                        />
                    </VCardText>
                </VCard>
            </VCol>

            <!-- SEZIONE RIEPILOGO PRENOTAZIONE-->
            <VCol
            cols="12"
            md="4"
            >
            <VCard
                flat
                variant="outlined"
            >


                <!-- 👉 Price details -->
                <VCardText>
                <h6 class="text-h6 mb-4">
                    Dettaglio
                </h6>

                <div class="text-sm text-high-emphasis">
                    <div class="d-flex justify-space-between mb-2">
                    <div class="text-body-1 text-high-emphasis">
                        Ingressi prenotati
                    </div>
                    <div class="text-body-1">
                        {{ nuovaPrenotazione.date.length }}
                    </div>
                    </div>

                    <div class="d-flex justify-space-between mb-2">
                    <div class="text-body-1 text-high-emphasis">
                        Servizi Selezionati
                    </div>
                    <div class="text-body-1">
                        {{ costoServizi }}€
                    </div>
                    </div>
                    <div class="d-flex justify-space-between mb-2">
                    <div class="text-body-1 text-high-emphasis">
                        Sconto coupon
                    </div>
                    <div class="d-flex gap-x-2">
                            <div class="text-body-1 text-disabled">
                            12€
                            </div>
                        </div>
                    </div>

                    <div class="d-flex justify-space-between mb-2">
                        <div class="text-body-1 text-high-emphasis">
                            Sconto
                        </div>

                        <div class="d-flex gap-x-2">
                            <div class="text-body-1 text-disabled">
                            {{ sconto }}%
                            </div>
                        </div>
                    </div>

                    <div class="d-flex justify-space-between mb-2">
                    <div class="text-body-1 text-high-emphasis">
                        Totale provvisorio
                    </div>
                    <div class="text-body-1">
                        {{ costoTotale + costoServizi}}€
                    </div>
                    </div>
                </div>
                </VCardText>

                <VDivider />

                <VCardText class="d-flex justify-space-between py-4">
                <h6 class="text-h6">
                    Totale
                </h6>
                <h6 class="text-h6">
                     {{ costoTotale + costoServizi - (sconto / 100 * costoTotale) }}€
                </h6>
                </VCardText>
            </VCard>

            <VBtn
                block
                class="mt-4"
                @click="addPaymentForm?.validateAndGetPayload()"
            >
                Concludi Prenotazione
            </VBtn>
            </VCol>
        </VRow>
    </section>
</template>
<script lang="ts" setup>
import { NuovaPrenotazioneModel } from '@/types/NuovaPrenotazioneModel';
import { inject, type Ref } from 'vue';
import AddPaymentDialogContent from '@/views/pages/payments/components/AddPaymentDialogContent.vue'
import type { ServiziModel } from '@/types/ServiziModel';

const emit = defineEmits(['onSave'])

const props = defineProps<{
  servizi: ServiziModel[]
}>()

const nuovaPrenotazione = inject('nuovaPrenotazione') as Ref<NuovaPrenotazioneModel>
const tipologia = computed(() => {
    return nuovaPrenotazione.value.tipologia
})
const turno = computed(() => {
    return nuovaPrenotazione.value.turno
})
const costoTotale = computed(() => {
    if(tipologia.value === "COWORK_BASE"){
        if(turno.value === "INTERO_GIORNO"){
            return nuovaPrenotazione.value.date.length * (props.servizi.find(s => s.key === "COWORK_BASE")?.costoIntero ?? 1)
        }
        if(turno.value === "MATTINA"){
            return nuovaPrenotazione.value.date.length * (props.servizi.find(s => s.key === "COWORK_BASE")?.costoRidotto ?? 1)
        }
        if(turno.value === "POMERIGGIO"){
            return nuovaPrenotazione.value.date.length * (props.servizi.find(s => s.key === "COWORK_BASE")?.costoRidotto ?? 1)
        }
    }
    if(tipologia.value === "UFF_PRIVATO"){
        return nuovaPrenotazione.value.date.length * (props.servizi.find(s => s.key === "UFF_PRIVATO")?.costoIntero ?? 1)
    }
    if(tipologia.value === "SALA_RIUNIONI"){
        return nuovaPrenotazione.value.date.length * (props.servizi.find(s => s.key === "SALA_RIUNIONI")?.costoIntero ?? 1)
    }
    return 0
})
const costoServizi = computed(() => {
    return 10
})
const sconto = computed(() => {
    if(nuovaPrenotazione.value.date.length >= 5 && nuovaPrenotazione.value.date.length < 10){
        return 5
    }
    if(nuovaPrenotazione.value.date.length >= 10){
        return 10
    }
    return 0
})
const onSubmit = (data: { date: any; value: number; status: string; tipoPagamento: string }) => {
  nuovaPrenotazione.value.pagamento = {...data, userId: nuovaPrenotazione.value.userId}
  emit('onSave')
}

const onCancel = () => {
  console.log('cancel')
}

const addPaymentForm = ref()

</script>