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
    },

    async getAllProjectDocuments(projectId: string, flgDeleted: boolean = false) {
        return api.get(`/repository/get-all-files`, {
            params: {
                prefix: 'project',
                id: projectId,
                flgDeleted: flgDeleted
            }
        })
    },

    async uploadUserDocument(prefix: string, userID: string, formData: FormData) {
        return api.post(`/repository/add-file`, formData, {
            params: {
                type: prefix,
                userId: userID
            },
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
    },

    async deleteDocument(prefix:string, documentID:string){

        return api.delete(`/repository/remove-file`, {
            params: {
                type: prefix,
                fileId: documentID
            }
        })
    }, 

    async downloadDocument(prefix:String, documentID:string){
        return api.get(`/repository/get-file`, {
            params: {
                type: prefix,
                fileId: documentID
            }
        })
    }
}