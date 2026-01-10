export interface Invoice {
    id: string
    userId: string
    paymentId: string
    value: number
    date: string
    status: string
    tipoPagamento: string
}
