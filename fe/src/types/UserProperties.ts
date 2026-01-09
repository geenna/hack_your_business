import { BillingAddress } from "./BillingAddress"

export interface Role {
  action: string
  subject: string
}



export interface UserDetail {
  id: string
  email: string
  userType: string
  roles: Role[]
  nome: string
  cognome: string
  cf: string
  indirizzoResidenza: string
  citta: string
  cap: string
  prov: string
  regioneSociale: string
  piva: string
  telefono: string
  avatar: string
  stato: string
  user_status: string
  billing_address?: BillingAddress
}

// Keep UserProperties for backward compatibility if needed, or alias it
export type UserProperties = UserDetail
