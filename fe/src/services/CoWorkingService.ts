import { DisponibilitaCompletaType } from '@/types/DisponibilitaCompletaType'
import api from './api'
import type { ServiziModel } from '@/types/ServiziModel'

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
    }
}
