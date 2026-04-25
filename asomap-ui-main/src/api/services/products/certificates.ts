import { httpClient } from '../../config/httpClient';
import { ENDPOINTS } from '@/constants';
import { debugLog, errorLog } from '@/utils/environment';
import { normalizeObjectMedia } from '@/utils/media';

type CertificateApiItem = {
  id: number | string;
  title: string;
  subtitle?: string | null;
  description?: string | null;
  bannerImage?: string | null;
  banner_image?: string | null;
  certificateImage?: string | null;
  certificate_image?: string | null;
  image?: string | null;
  image_url?: string | null;
  certificate_type?: string | null;
  cta_apply?: string | null;
  cta_rates?: string | null;
  benefits?: any;
  investment?: any;
  rates?: any;
  requirements?: any;
  depositRates?: any;
  deposit_rates?: any;
  faq?: any;
  slug?: string | null;
  is_active?: boolean;
};

type CertificatesApiResponse = {
  count?: number;
  next?: string | null;
  previous?: string | null;
  results: CertificateApiItem[];
};

const slugify = (text: string) =>
  String(text || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');

export const certificatesService = {
  getAllCertificates: async () => {
    try {
      debugLog('[CertificatesService] Fetching all certificates from backend');

      const response = await httpClient.get<CertificatesApiResponse>(
        ENDPOINTS.COLLECTIONS.PRODUCTS.CERTIFICATES
      );

      debugLog('[CertificatesService] Backend response received successfully:', response.data);

      const results = response.data?.results || [];

      return results
        .filter((item: CertificateApiItem) => item.is_active !== false)
        .map((item: CertificateApiItem) =>
          normalizeObjectMedia({
            id: item.id,
            title: item.title || '',
            subtitle: item.subtitle || '',
            description: item.description || '',
            bannerImage: item.bannerImage || item.banner_image || '',
            certificateImage: item.certificateImage || item.certificate_image || '',
            image: item.image || '',
            image_url: item.image_url || '',
            certificateType: item.certificate_type || '',
            ctaApply: item.cta_apply || '',
            ctaRates: item.cta_rates || '',
            benefits: item.benefits || { title: '', items: [] },
            investment: item.investment || { title: '', subtitle: '', details: [], imageUrl: '' },
            rates: item.rates || { title: '', items: [] },
            requirements: item.requirements || { title: '', items: [] },
            depositRates: item.depositRates || item.deposit_rates || { title: '', items: [], validFrom: '' },
            faq: item.faq || { title: '', items: [] },
            slug: item.slug || slugify(item.title),
          })
        );
    } catch (error) {
      errorLog('[CertificatesService] Error fetching certificates:', error);
      throw error;
    }
  },

  getCertificateById: async (id: string | number) => {
    try {
      debugLog(`[CertificatesService] Fetching certificate with ID ${id} from backend`);

      const response = await httpClient.get<CertificateApiItem>(
        `${ENDPOINTS.COLLECTIONS.PRODUCTS.CERTIFICATES}${id}/`
      );

      debugLog('[CertificatesService] Certificate response received successfully:', response.data);

      const item = response.data;

      return normalizeObjectMedia({
        id: item.id,
        title: item.title || '',
        subtitle: item.subtitle || '',
        description: item.description || '',
        bannerImage: item.bannerImage || item.banner_image || '',
        certificateImage: item.certificateImage || item.certificate_image || '',
        image: item.image || '',
        image_url: item.image_url || '',
        certificateType: item.certificate_type || '',
        ctaApply: item.cta_apply || '',
        ctaRates: item.cta_rates || '',
        benefits: item.benefits || { title: '', items: [] },
        investment: item.investment || { title: '', subtitle: '', details: [], imageUrl: '' },
        rates: item.rates || { title: '', items: [] },
        requirements: item.requirements || { title: '', items: [] },
        depositRates: item.depositRates || item.deposit_rates || { title: '', items: [], validFrom: '' },
        faq: item.faq || { title: '', items: [] },
        slug: item.slug || slugify(item.title),
      });
    } catch (error) {
      errorLog(`[CertificatesService] Error fetching certificate with ID ${id}:`, error);
      return null;
    }
  },

  getCertificateBySlug: async (slug: string) => {
    try {
      const certificates = await certificatesService.getAllCertificates();
      return certificates.find((item: { slug: string }) => item.slug === slug) || null;
    } catch (error) {
      errorLog(`[CertificatesService] Error fetching certificate by slug ${slug}:`, error);
      return null;
    }
  }
};
