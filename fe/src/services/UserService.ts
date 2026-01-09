import api from './api'

export default {
    async getAllUsers() {
        return api.get('/users')
    },
    async detailUser(id: string) {
        return api.get(`/user-detail/${id}`)
    },
    async createUser(user: any) {
        return api.post('/users', user)
    },
    async suspendUser(id: string) {
        return api.put(`/users/${id}/suspend`)
    },
    async activateUser(id: string) {
        return api.put(`/users/${id}/activate`)
    },
}
