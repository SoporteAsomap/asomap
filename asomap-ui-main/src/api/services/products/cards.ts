import { httpClient } from '../../config/httpClient';
import { ENDPOINTS } from '@/constants';
import { debugLog, errorLog } from '@/utils/environment';
import { normalizeObjectMedia } from '@/utils/media';

type CardApiItem = {
  id: number | string;
  title: string;
  description: string;
  bannerImage?: string | null;
  cardImage?: string | null;
  image?: string | null;
  image_url?: string | null;
  card_type?: string;
  features?: string[];
  requirements?: string[];
  benefits?: unknown[];
  slug?: string;
  is_active?: boolean;
};

type CardsApiResponse = {
  count?: number;
  next?: string | null;
  previous?: string | null;
  results: CardApiItem[];
};

const slugify = (text: string) =>
  text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

export const cardsService = {
  getAllCards: async () => {
    try {
      debugLog('[CardsService] Fetching all cards from backend');

      const response = await httpClient.get<CardsApiResponse>(
        ENDPOINTS.COLLECTIONS.PRODUCTS.CARDS
      );

      debugLog('[CardsService] Backend response received successfully:', response.data);

      const results = response.data?.results || [];

      return results
        .filter((item: CardApiItem) => item.is_active !== false)
        .map((item: CardApiItem) =>
          normalizeObjectMedia({
            id: item.id,
            title: item.title,
            description: item.description,
            bannerImage: item.bannerImage,
            cardImage: item.cardImage,
            image: item.image,
            image_url: item.image_url,
            cardType: item.card_type || '',
            features: item.features || [],
            requirements: item.requirements || [],
            benefits: item.benefits || [],
            slug: item.slug || slugify(item.title),
          })
        );
    } catch (error) {
      errorLog('[CardsService] Error fetching cards:', error);
      throw error;
    }
  },

  getCardById: async (id: string | number) => {
    try {
      debugLog(`[CardsService] Fetching card with ID ${id} from backend`);

      const response = await httpClient.get<CardApiItem>(
        `${ENDPOINTS.COLLECTIONS.PRODUCTS.CARDS}${id}/`
      );

      debugLog('[CardsService] Card response received successfully:', response.data);

      const item = response.data;

      return normalizeObjectMedia({
        id: item.id,
        title: item.title,
        description: item.description,
        bannerImage: item.bannerImage,
        cardImage: item.cardImage,
        image: item.image,
        image_url: item.image_url,
        cardType: item.card_type || '',
        features: item.features || [],
        requirements: item.requirements || [],
        benefits: item.benefits || [],
        slug: item.slug || slugify(item.title),
      });
    } catch (error) {
      errorLog(`[CardsService] Error fetching card with ID ${id}:`, error);
      return null;
    }
  },

  getCardBySlug: async (slug: string) => {
    try {
      const cards = await cardsService.getAllCards();
      return cards.find((item: { slug: string }) => item.slug === slug) || null;
    } catch (error) {
      errorLog(`[CardsService] Error fetching card by slug ${slug}:`, error);
      return null;
    }
  }
};
