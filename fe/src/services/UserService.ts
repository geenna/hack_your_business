import api from './api'

export default {
    async getAllUsers() {
        return api.get('/users')
    },
    async detailUser(id: string) {
        return api.get(`/user-detail/${id}`)
    },
}
