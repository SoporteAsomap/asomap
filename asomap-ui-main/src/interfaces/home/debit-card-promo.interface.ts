
export interface IDebitCardPromoData {
    id: number;
    title: string;
    highlighted_title: string;
    description: string;
    primary_button_text: string;
    secondary_button_text: string;
    primary_button_url: string;
    secondary_button_url: string;
    image_url: string;
    image_alt: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface IDebitCardPromoProps {
    data: IDebitCardPromoData;
}