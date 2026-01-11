import api from './api'

export default {
    async getProjectsByUser(user_id: string) {
        return api.get(`/projects/project-by-user/${user_id}`)
    }
}
