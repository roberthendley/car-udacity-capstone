
export interface Contact {
    id: number,
    name: string,
    position_title: string,
    email_address: string,
    mobile_phone: string,
    contact_type: 'consultant'|'clientmanager'|'other'
}