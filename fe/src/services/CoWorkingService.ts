import { DisponibilitaCompletaType } from '@/types/DisponibilitaCompletaType'
import api from './api'
import type { ServiziModel } from '@/types/ServiziModel'
import { NuovaPrenotazioneModel } from '@/types/NuovaPrenotazioneModel'

export default {

    async getServizi() {
        return api.get('/cowork/servizi')
    },

    async upsertServizio(servizio: ServiziModel) {
        return api.post('/cowork/servizi', servizio)
    },

    async deleteServizio(id: string) {
        return api.delete(`/cowork/servizi/${id}`)
    },

    async salvaDisponibilità(data: any) {
        return api.post('/cowork/disponibilita', data)
    },

    async getDisponibilitaCompleta(periodo: string, tipologia: string) {
        return api.get<DisponibilitaCompletaType[]>('/cowork/disponibilita', { params: { periodo, tipologia } })
    },

    async getDisponibilitaPerIlMese(data: string, tipologia: string) {
        return api.get<DisponibilitaCompletaType[]>('/cowork/disponibilita-month', { params: { data, tipologia } })
    },

    async eliminaDisponibilita(id: string, data: string) {
        return api.delete(`/cowork/disponibilita/${id}/${data}`)
    },

    async createPrenotazione(prenotazione: NuovaPrenotazioneModel) {
        return api.post('/cowork/prenotazione', prenotazione)
    },

    async getPrenotazioni(data: string) {
        return api.get<any[]>('/cowork/prenotazioni', { params: { data } })
    },

    async eliminaPrenotazione(id: string) {
        return api.delete(`/cowork/prenotazioni/${id}`)
    },
    async getNextUserCoWorkings(userId?: string) {
        return api.get('/cowork/next-user-co-workings', { params: { userId } })
    }
}
