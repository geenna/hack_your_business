import api from './api'

export default {
    async getAllProjectsByUser(user_id: string) {
        return api.get(`/projects/all-projects/${user_id}`)
    }
}
