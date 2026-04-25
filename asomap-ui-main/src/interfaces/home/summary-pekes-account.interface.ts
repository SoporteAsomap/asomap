export interface PekeAccountSummaryProps {
    title: string;
    description: string;
    buttonText: string;
    imageUrl: string;
    imageAlt: string;
    button_url?: string;
    onButtonClick: () => void;
}

export interface IPekeAccountSummaryData {
    id: number;
    title: string;
    description: string;
    button_text: string;
    image_url: string;
    image_alt: string;
    button_url: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}