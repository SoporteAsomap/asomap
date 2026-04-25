import { httpClient } from '../../config/httpClient';
import { ENDPOINTS } from '@/constants';
import { debugLog, errorLog } from '@/utils/environment';
import { normalizeObjectMedia } from '@/utils/media';

type AccountApiItem = {
  id: number | string;
  title: string;
  description: string;
  bannerImage?: string | null;
  accountImage?: string | null;
  category: string;
  features: string[];
  requirements: string[];
  benefits: unknown[];
  slug?: string;
  is_active?: boolean;
};

type AccountsApiResponse = {
  count?: number;
  next?: string | null;
  previous?: string | null;
  results: AccountApiItem[];
};

const slugify = (text: string) =>
  text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

export const accountsService = {
  getAllAccounts: async () => {
    try {
      debugLog('[AccountsService] Fetching all accounts from backend');

      const response = await httpClient.get<AccountsApiResponse>(
        ENDPOINTS.COLLECTIONS.PRODUCTS.ACCOUNTS
      );

      debugLog('[AccountsService] Backend response received successfully:', response.data);

      const results = response.data.results || [];

      return results
        .filter((item: AccountApiItem) => item.is_active !== false)
        .map((item: AccountApiItem) =>
          normalizeObjectMedia({
            id: item.id,
            title: item.title,
            description: item.description,
            bannerImage: item.bannerImage,
            accountImage: item.accountImage,
            category: item.category,
            features: item.features,
            requirements: item.requirements,
            benefits: item.benefits,
            slug: item.slug || slugify(item.title),
          })
        );
    } catch (error) {
      errorLog('[AccountsService] Error fetching accounts data:', error);
      throw error;
    }
  },

  getAccountById: async (id: string | number) => {
    try {
      debugLog(`[AccountsService] Fetching account with ID ${id} from backend`);

      const response = await httpClient.get<AccountApiItem>(
        `${ENDPOINTS.COLLECTIONS.PRODUCTS.ACCOUNTS}${id}/`
      );

      debugLog('[AccountsService] Account response received successfully:', response.data);

      const item = response.data;

      return normalizeObjectMedia({
        id: item.id,
        title: item.title,
        description: item.description,
        bannerImage: item.bannerImage,
        accountImage: item.accountImage,
        category: item.category,
        features: item.features,
        requirements: item.requirements,
        benefits: item.benefits,
        slug: item.slug || slugify(item.title),
      });
    } catch (error) {
      errorLog(`[AccountsService] Error fetching account with ID ${id}:`, error);
      return null;
    }
  },

  getAccountBySlug: async (slug: string) => {
    try {
      const accounts = await accountsService.getAllAccounts();
      return accounts.find((item: { slug: string }) => item.slug === slug) || null;
    } catch (error) {
      errorLog(`[AccountsService] Error fetching account by slug ${slug}:`, error);
      return null;
    }
  }
};
