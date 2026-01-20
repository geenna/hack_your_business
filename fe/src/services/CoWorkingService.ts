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
}
