import { ProjectFull } from '@/types/UserToProjectSchema'
import api from './api'



export default {
    async getAllProjectsByUser(user_id: string) {
        return api.get(`/projects/all-projects/${user_id}`)
    },
    async getProjectsFull() {
        return api.get<ProjectFull[]>('/projects/user-projects-full/')
    },
    async addCollaborators(projectId: string, userIds: string[]) {
        return api.post(`/projects/${projectId}/collaborators`, { userIds })
    },
    async removeCollaborator(projectId: string, userId: string) {
        return api.delete(`/projects/${projectId}/collaborators/${userId}`)
    },
    async updateProject(projectId: string, projectData: any) {
        return api.put(`/projects/${projectId}`, projectData)
    },
    async deleteProject(projectId: string) {
        return api.delete(`/projects/${projectId}`)
    },
    async createProject(projectData: any) {
        return api.post('/projects/', projectData)
    }
}
