import api from './api'
import { BillingAddress } from '@/types/BillingAddress'
import { Invoice } from '@/types/Invoice'

export default {
    async saveBillingAddress(addressData: BillingAddress) {
        return api.put('/payments/address-data', addressData)
    },

    async getUserPayments(userId: string, fromDate: string, toDate: string) {
        return api.get<Invoice[]>('/payments/get-user-payments', {
            params: {
                userId,
                fromDate,
                toDate
            }
        })
    },

    async createPayment(paymentData: Omit<Invoice, 'id' | 'paymentId'>) {
        return api.post<Invoice>('/payments/', paymentData)
    },

    async deletePayment(id: string) {
        return api.delete(`/payments/${id}`)
    }
}
