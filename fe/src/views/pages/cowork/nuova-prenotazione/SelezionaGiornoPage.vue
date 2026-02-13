<template>

    <!--SEZIONE SCELTA SLOT TEMPORALE-->
    <section class="d-flex mb-12">
      <VRow>
           
        <VCol cols="4">
            <VCard>
              <VCardText>
                <div class="d-flex justify-space-between">
                  <div class="d-flex flex-column gap-y-1">
                    <span class="text-base text-high-emphasis">{{tipologiaDescrizione}} - Giornata intera</span>
                    <p class="text-sm mb-0">
                     Accesso consentito dalle alle
                    </p>
                  </div>
                  <VBtn :variant="turno === 'INTERO_GIORNO' ? 'elevated' : 'outlined'" @click="selezionaTurno('INTERO_GIORNO')">
                    {{ turno === 'INTERO_GIORNO' ? 'Selezionato' : 'Seleziona' }}
                  </VBtn>
                </div>
              </VCardText>
            </VCard>
          </VCol>
        <VCol
           cols="4"
          >
            <VCard>
              <VCardText>
                <div class="d-flex justify-space-between">
                  <div class="d-flex flex-column gap-y-1">
                    <span class="text-base text-high-emphasis">{{tipologiaDescrizione}}  - Turno mattina</span>
                    <p class="text-sm mb-0">
                     Accesso consentito solo dalle alle
                    </p>
                  </div>
                  <VBtn :variant="turno === 'MATTINA' ? 'elevated' : 'outlined'" @click="selezionaTurno('MATTINA')">
                    {{ turno === 'MATTINA' ? 'Selezionato' : 'Seleziona' }}
                  </VBtn>
                </div>
              </VCardText>
            </VCard>
          </VCol><VCol
            cols="4"
          >
            <VCard>
              <VCardText>
                <div class="d-flex justify-space-between">
                  <div class="d-flex flex-column gap-y-1">
                    <span class="text-base text-high-emphasis">{{tipologiaDescrizione}} - Turno pomeriggio</span>
                    <p class="text-sm mb-0">
                     Accesso consentito solo dalle alle
                    </p>
                  </div>
                  <VBtn :variant="turno === 'POMERIGGIO' ? 'elevated' : 'outlined'" @click="selezionaTurno('POMERIGGIO')">  
                    {{ turno === 'POMERIGGIO' ? 'Selezionato' : 'Seleziona' }}
                  </VBtn>
                </div>
              </VCardText>
            </VCard>
          </VCol>
      </VRow>
    </section>

    <!-- CALENDARIO E SEZIONE RIEPILOGO PRENOTAZIONE-->
    <section class="d-flex my-6">
        
        <VRow>
            <!--SEZIONE CALENDARIO-->
            <VCol cols="12" md="8">
                
                <VCard flat variant="outlined">
                   <VCardText>
                        <VSheet height="700">
                            <VToolbar color="transparent" flat>
                                <VBtn class="ma-2" variant="text" icon @click="prev">
                                    <v-icon>ri-arrow-left-s-line</v-icon>
                                </VBtn>
                                <v-toolbar-title class="text-h6 text-center">{{ refCalendar.title  }}</v-toolbar-title>
                                <VBtn class="ma-2" variant="text" icon @click="next"  >
                                    <v-icon>ri-arrow-right-s-line</v-icon>
                                </VBtn>
                            </VToolbar>
                            <v-calendar
                                v-model="calendarModel"
                                ref="refCalendar"
                                :now="new Date().toISOString()"
                                color="primary"
                                locale="it"
                                type="month"
                                @click:day="setDay"
                            >
                                <template v-slot:day="{past, date }">
                                    <template v-if="!past && (getCalendarLabel(date) === 'Non disponibile' || giorniAggiunti.find((d:string) => d === date))" >
                                        <VSheet class="pa-1" style="background-color: rgba(255, 255, 255, 0) !important">
                                            <VChip 
                                                label
                                                size="x-small"
                                                :color="getCalendarColor(date)"
                                                rounded="sm"
                                                >
                                                {{ getCalendarLabel(date) }}
                                            </VChip>   
                                        </VSheet>
                                           
                                    </template>
                                          
                                </template>
                               
                            </v-calendar>  
                         </VSheet>
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
                <!-- 👉 payment offer -->
                <VCardText>
                <h6 class="text-h6 mb-4">
                    Dettaglio Prenotazione
                </h6>

                <div class="d-flex align-center gap-4">
                    <VTextField
                    
                    placeholder="Inserisci coupon"
                    density="compact"
                    />

                    <VBtn
                    variant="outlined"
                    >
                    Applica
                    </VBtn>
                </div>

                <!-- 👉 Gift wrap banner -->
                <div class="bg-var-theme-background rounded pa-5 mt-4">
                    <h6 class="text-h6">
                    Vuoi aggiungere dei servizi alla prenotazione?
                    </h6>

                    <p class="my-2 text-body-1">
                    Monitor 23" 1080p, Tastiera comfort, ecc
                    </p>

                    <a
                    href="javascript:void(0)"
                    class="font-weight-medium d-inline-block"
                    >Seleziona Servizio</a>
                </div>
                </VCardText>

                <VDivider />

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
                        {{ giorniAggiunti.length }}
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
                @click="submit"
            >
                Continua
            </VBtn>
            </VCol>
        </VRow>
    </section>

</template>

<script lang="ts" setup>
import CoWorkingService from '@/services/CoWorkingService'
import { NuovaPrenotazioneModel } from '@/types/NuovaPrenotazioneModel'
import { DisponibilitaCompletaType } from '@/types/DisponibilitaCompletaType'
import { ref, inject, computed, type Ref } from 'vue'
import { useAlert } from '@/shared/state/alert'
import { useConfirm } from '@/shared/state/confirm'
import { ServiziModel } from '@/types/ServiziModel'

const { show: showAlert } = useAlert()
const { show: showConfirm } = useConfirm()
const nuovaPrenotazione = inject('nuovaPrenotazione') as Ref<NuovaPrenotazioneModel>
const props = defineProps<{
  servizi: ServiziModel[]
}>()
const tipologiaDescrizione = computed(() => {
    if(nuovaPrenotazione.value.tipologia === 'COWORK_BASE'){
        return 'Cowork'
    }
    if(nuovaPrenotazione.value.tipologia === 'UFF_PRIVATO'){
        return 'Ufficio Privato'
    }
    if(nuovaPrenotazione.value.tipologia === 'SALA_RIUNIONI'){
        return 'Sala Riunioni'
    }
    return ""
})
const emit = defineEmits(['onSelezionaGiorno'])
const refCalendar = ref("refCalendar") as Ref<any>
const calendarModel = ref('')
const tipologia = computed(() => {
    return nuovaPrenotazione.value.tipologia
})
const costoTotale = computed(() => {
    if(tipologia.value === "COWORK_BASE"){
        if(turno.value === "INTERO_GIORNO"){
            return giorniAggiunti.value.length * (props.servizi.find(s => s.key === "COWORK_BASE")?.costoIntero ?? 1)
        }
        if(turno.value === "MATTINA"){
            return giorniAggiunti.value.length * (props.servizi.find(s => s.key === "COWORK_BASE")?.costoRidotto ?? 1)
        }
        if(turno.value === "POMERIGGIO"){
            return giorniAggiunti.value.length * (props.servizi.find(s => s.key === "COWORK_BASE")?.costoRidotto ?? 1)
        }
    }
    if(tipologia.value === "UFF_PRIVATO"){
        return giorniAggiunti.value.length * (props.servizi.find(s => s.key === "UFF_PRIVATO")?.costoIntero ?? 1)
    }
    if(tipologia.value === "SALA_RIUNIONI"){
        return giorniAggiunti.value.length * (props.servizi.find(s => s.key === "SALA_RIUNIONI")?.costoIntero ?? 1)
    }
    return 0
})
const costoServizi = computed(() => {
    return 10
})
const sconto = computed(() => {
    if(giorniAggiunti.value.length >= 5 && giorniAggiunti.value.length < 10){
        return 5
    }
    if(giorniAggiunti.value.length >= 10){
        return 10
    }
    return 0
})
const turno = ref("INTERO_GIORNO")
const prev = () => {
    
    refCalendar.value.prev()
}
const next = () => {
    refCalendar.value.next()
    loadDisponibilita()
}


const giorniAggiunti:Ref<string[]> = ref([])
const setDay = (nativeEvent:Event, { date }: { date: string }) => {
    if(new Date(date) < new Date()){
        return
    }
    if(!getDisponibilitaGiorno(date)){
        return
    }

    if(giorniAggiunti.value.includes(date)){
        giorniAggiunti.value.splice(giorniAggiunti.value.indexOf(date), 1)
    }
    else{
        giorniAggiunti.value.push(date)
    }
}

const getDisponibilitaGiorno = (date:string) => {
    const monthYear = `${new Date(date).getFullYear()}-${String(new Date(date).getMonth() + 1).padStart(2, '0')}`
    const disponibilita:DisponibilitaCompletaType[] | undefined = disponibilitaMesi.value.get(monthYear)
    
    if(disponibilita){
        const disponibilitaGiorno = disponibilita.find((d:DisponibilitaCompletaType) => d.date === date )
        if(disponibilitaGiorno){
            if(turno.value === "INTERO_GIORNO"){
                return (disponibilitaGiorno.numMattina - disponibilitaGiorno.numPrenotazioniMattina) > 0 &&
                (disponibilitaGiorno.numPomeriggio - disponibilitaGiorno.numPrenotazioniPomeriggio) > 0
               
            }else if(turno.value === "MATTINA"){
                return (disponibilitaGiorno.numMattina - disponibilitaGiorno.numPrenotazioniMattina) > 0
                
            }else if(turno.value === "POMERIGGIO"){
                return (disponibilitaGiorno.numPomeriggio - disponibilitaGiorno.numPrenotazioniPomeriggio) > 0
               
            }  
        }
    }
    return false
}

const getCalendarLabel = (item: string) => {
    if(giorniAggiunti.value.find((d:string) => d === item )){
        return 'Selezionato'
    }
    if(!getDisponibilitaGiorno(item)){
        return 'Non disponibile'
    }
    return ''
}

const getCalendarColor = (item: string) => {
     if(giorniAggiunti.value.find((d:string) => d === item )){
        return 'success'
    }
    if(!getDisponibilitaGiorno(item)){
        return 'primary'
    }
    return ''
}

const disponibilitaMesi:Ref<Map<string, DisponibilitaCompletaType[]>> = ref(new Map())
const loadDisponibilita = () => {
    let fromDate = new Date()
    if(calendarModel.value){
        fromDate = new Date(calendarModel.value)
    }
    CoWorkingService.getDisponibilitaPerIlMese(toDateOnlyISO(fromDate), tipologia.value)
        .then((res) => {
            if(res.status === 200){
                const monthYear = `${fromDate.getFullYear()}-${String(fromDate.getMonth() + 1).padStart(2, '0')}`;
                disponibilitaMesi.value.set(monthYear, res.data)
            }
        })
}

watch(tipologia, (val) => {
    calendarModel.value = ''
    giorniAggiunti.value = []
    disponibilitaMesi.value = new Map()
    loadDisponibilita()
}, { immediate: true })

const selezionaTurno = async (newTurn:string) => {
    if(giorniAggiunti.value.length > 0){
    const confirmed = await showConfirm(
        'Cambiando il turno, si cancellano le prenotazioni esistenti. Continui?',
        ''
    )
        if (confirmed) {
            giorniAggiunti.value = []
            turno.value = newTurn
        }
    }
    else{
        giorniAggiunti.value = []
        turno.value = newTurn
    }
}

const onSelected = () => {
    emit('onSelezionaGiorno')
}

const submit = () => {
    if(giorniAggiunti.value.length === 0){
        showAlert( 'Attenzione', 'Devi selezionare almeno un giorno')
        return
    }

    nuovaPrenotazione.value.date = giorniAggiunti.value
    nuovaPrenotazione.value.turno = turno.value
    
    emit('onSelezionaGiorno')
}
</script>