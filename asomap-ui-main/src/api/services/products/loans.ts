import { httpClient } from '../../config/httpClient';
import { ENDPOINTS } from '@/constants';
import { debugLog, errorLog } from '@/utils/environment';
import { normalizeObjectMedia } from '@/utils/media';

type LoanApiItem = {
  id: number | string;
  title: string;
  description?: string | null;
  loan_type?: string | number | null;
  details?: any;
  requirements_title?: string | null;
  requirements?: any;
  slug?: string | null;
  bannerImage?: string | null;
  banner_image?: string | null;
  image?: string | null;
  image_url?: string | null;
  is_active?: boolean;
};

type LoansApiResponse = {
  count?: number;
  next?: string | null;
  previous?: string | null;
  results: LoanApiItem[];
};

const slugify = (text: string) =>
  String(text || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');

export const loansService = {
  getAllLoans: async () => {
    try {
      debugLog('[LoansService] Fetching all loans from backend');

      const response = await httpClient.get<LoansApiResponse>(
        ENDPOINTS.COLLECTIONS.PRODUCTS.LOANS
      );

      debugLog('[LoansService] Backend response received successfully:', response.data);

      const results = response.data?.results || [];

      return results
        .filter((item: LoanApiItem) => item.is_active !== false)
        .map((item: LoanApiItem) =>
          normalizeObjectMedia({
            id: item.id,
            title: item.title || '',
            description: item.description || '',
            loanType: item.loan_type || '',
            details: Array.isArray(item.details) ? item.details : item.details ? [item.details] : [],
            requirementsTitle: item.requirements_title || '',
            requirements: Array.isArray(item.requirements)
              ? item.requirements
              : item.requirements
                ? [item.requirements]
                : [],
            slug: item.slug || slugify(item.title),
            bannerImage: item.bannerImage || item.banner_image || '',
            image: item.image || '',
            image_url: item.image_url || '',
          })
        );
    } catch (error) {
      errorLog('[LoansService] Error fetching loans:', error);
      throw error;
    }
  },

  getLoanById: async (id: string | number) => {
    try {
      debugLog(`[LoansService] Fetching loan with ID ${id} from backend`);

      const response = await httpClient.get<LoanApiItem>(
        `${ENDPOINTS.COLLECTIONS.PRODUCTS.LOANS}${id}/`
      );

      debugLog('[LoansService] Loan response received successfully:', response.data);

      const item = response.data;

      return normalizeObjectMedia({
        id: item.id,
        title: item.title || '',
        description: item.description || '',
        loanType: item.loan_type || '',
        details: Array.isArray(item.details) ? item.details : item.details ? [item.details] : [],
        requirementsTitle: item.requirements_title || '',
        requirements: Array.isArray(item.requirements)
          ? item.requirements
          : item.requirements
            ? [item.requirements]
            : [],
        slug: item.slug || slugify(item.title),
        bannerImage: item.bannerImage || item.banner_image || '',
        image: item.image || '',
        image_url: item.image_url || '',
      });
    } catch (error) {
      errorLog(`[LoansService] Error fetching loan with ID ${id}:`, error);
      return null;
    }
  },

  getLoanBySlug: async (slug: string) => {
    try {
      const loans = await loansService.getAllLoans();
      return loans.find((item: { slug: string }) => item.slug === slug) || null;
    } catch (error) {
      errorLog(`[LoansService] Error fetching loan by slug ${slug}:`, error);
      return null;
    }
  },

  getLoansByType: async (loanType: string) => {
    try {
      const loans = await loansService.getAllLoans();
      return loans.filter((item: any) => String(item.loanType) === String(loanType));
    } catch (error) {
      errorLog(`[LoansService] Error fetching loans by type ${loanType}:`, error);
      return [];
    }
  }
};
