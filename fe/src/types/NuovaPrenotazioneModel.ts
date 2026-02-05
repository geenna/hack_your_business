export interface NuovaPrenotazioneModel {
    id?: string
    idServizioSelezionato: string
    tipologia: string
    date: string[]
    turno: string
    userId: string
    pagamento: any
}