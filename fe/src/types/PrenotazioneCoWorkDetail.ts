import type { ServiziModel } from "./ServiziModel"
import type { UserDetail } from "./UserProperties"

export interface PrenotazioneCoWorkDetail {
    id: string
    data: string
    flgMattina: boolean
    flgPomeriggio: boolean
    pin: string
    wifiAccess: string
    user: UserDetail
    servizi: ServiziModel[]
}
