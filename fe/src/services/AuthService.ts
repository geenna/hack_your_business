import api from './api'

export default {
    async login(credentials: any) {
        return api.post('/token', {
            username: credentials.email,
            password: credentials.password
        })
    },
}
