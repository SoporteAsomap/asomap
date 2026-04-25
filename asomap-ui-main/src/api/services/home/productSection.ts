import { httpClient } from '../../config/httpClient';
import { ENDPOINTS } from '@/constants';
import type { IProductSectionResponse } from '@/interfaces';
import { debugLog, errorLog } from '@/utils/environment';
import { normalizeObjectMedia } from '@/utils/media';

export const productSectionService = {
  getProductSection: async (): Promise<IProductSectionResponse['data'] | null> => {
    try {
      debugLog('[ProductSectionService] Fetching from backend');
      const response = await httpClient.get<IProductSectionResponse>(
        ENDPOINTS.COLLECTIONS.HOME.PRODUCT_SECTION
      );

      debugLog('[ProductSectionService] Backend response received successfully:', response.data);

      const data = response.data.data;
      if (!data) return null;

      return normalizeObjectMedia(data);
    } catch (error) {
      errorLog('[ProductSectionService] Error fetching product section data:', error);
      debugLog('[ProductSectionService] API error, returning null');
      return null;
    }
  }
};
