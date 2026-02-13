import api from './api'
import type { Event, NewEvent } from '@/types/CalendarEvent'

export default {
    async getPrenotazioni(start: string, end: string) {
        return api.get<Event[]>('/calendar/lista', { params: { start, end } })
    },
    async addEvent(event: NewEvent) {
        return api.post<Event>('/calendar/crea', event)
    },
    async updateEvent(event: Event) {
        return api.put<Event>(`/calendar/modifica/${event.id}`, event)
    },
    async removeEvent(eventId: string) {
        return api.delete(`/calendar/elimina/${eventId}`)
    },

}
