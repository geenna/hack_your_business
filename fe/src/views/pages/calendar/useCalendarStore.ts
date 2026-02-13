import type { Event, NewEvent } from '@/types/CalendarEvent'
import CalendarService from '@/services/CalendarService';

export const useCalendarStore = defineStore('calendar', {
  // arrow function recommended for full type inference
  state: () => ({
    availableCalendars: [
      {
        color: 'error',
        label: 'Personale',
      },
      {
        color: 'success',
        label: 'Collaboratori',
      },
      {
        color: 'primary',
        label: 'Pubblico',
      }
    ],
    selectedCalendars: ['Personale', 'Collaboratori', 'Pubblico'],
  }),
  actions: {
    async fetchEvents() {
      const today = new Date();
      const start = new Date(today.getFullYear(), 0, 1).toISOString().split('T')[0]; // Jan 1st
      const end = new Date(today.getFullYear() + 1, 0, 1).toISOString().split('T')[0]; // Jan 1st next year

      const response = await CalendarService.getPrenotazioni(start, end);
      return response.data;
    },
    async addEvent(event: NewEvent) {
      await CalendarService.addEvent(event)
    },
    async updateEvent(event: Event) {
      return await CalendarService.updateEvent(event)
    },
    async removeEvent(eventId: string) {
      return await CalendarService.removeEvent(eventId)
    },

  },
})
