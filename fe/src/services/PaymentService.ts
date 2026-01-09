import api from './api'
import { BillingAddress } from '@/types/BillingAddress'

export default {
    async saveBillingAddress(addressData: BillingAddress) {
        return api.put('/payments/address-data', addressData)
    }
}
