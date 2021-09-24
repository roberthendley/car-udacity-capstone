export interface Client {
    id: number,
    name: string,
    bus_reg_nbr: string,
    abbreviation: string
}

export interface ClientContact {
    id: number,
    client_id: number,
    name: string,
    position_title: string,
    email_address: string,
    phone: string,
    address_1: string,
    address_2: string,
    address_3: string,
    city: string,
    state: string,
    post_code: string,
}