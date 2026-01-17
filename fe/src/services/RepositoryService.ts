import api from './api'

export default {
    async getAllUserDocuments(userID: string, flgDeleted: boolean = false) {
        return api.get(`/repository/get-all-files`, {
            params: {
                prefix: 'user',
                id: userID,
                flgDeleted: flgDeleted
            }
        })
    }
}