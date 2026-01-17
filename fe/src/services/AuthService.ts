import api from './api'

export default {
    async login(credentials: any) {
        const params = new URLSearchParams()
        params.append('username', credentials.email)
        params.append('password', credentials.password)
        params.append('grant_type', 'password')
        
        return api.post('/token', params, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
    },
}
