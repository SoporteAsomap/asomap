
export interface INewsBanner {
    title: string;
    imageUrl: string;
}

export interface INewsMedia {
    type: 'image' | 'video';
    url: string;
    caption?: string;
}

export interface INewsContent {
    type: 'paragraph' | 'subtitle' | 'quote' | 'list';
    content: string | string[];
}

export interface INewsLink {
    title: string;
    url: string;
    description?: string;
}

export interface INewsSlide {
    id: number;
    image: string;
    title: string;
    description: string;        // Para listas/previews
    date: string;
    author?: string;
    category?: string;
    tags?: string[];

    // Solo para detalle (opcional)
    fullContent?: INewsContent[];  // Contenido completo
    media?: INewsMedia[];          // Galería de imágenes/videos
    relatedLinks?: string[];       // Enlaces externos (URLs)
}

export interface INewsData {
    banner: INewsBanner;
    slides: INewsSlide[];
}

// Interfaces para la API
export interface INewsSlideAPI {
    id: number;
    image: string;
    title: string;
    description: string;
    date: string;
    author?: string;
    category?: string;
    tags?: string[];
    full_content?: INewsContent[];
    media?: INewsMedia[];
    related_links?: string[];
}

export interface INewsAPIResponse {
    count: number;
    next: string | null;
    previous: string | null;
    results: INewsSlideAPI[];
}
