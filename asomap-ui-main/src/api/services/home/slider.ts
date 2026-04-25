import { httpClient } from '../../config/httpClient';
import { ENDPOINTS } from '@/constants';
import type { SliderItemAPI } from '@/interfaces';
import { debugLog, errorLog } from '@/utils/environment';
import { normalizeObjectMedia } from '@/utils/media';

export const sliderService = {
  getSlider: async (): Promise<SliderItemAPI[]> => {
    try {
      debugLog('[SliderService] Fetching from backend');
      const response = await httpClient.get<SliderItemAPI[]>(
        ENDPOINTS.COLLECTIONS.HOME.SLIDER
      );

      debugLog('[SliderService] Backend response received successfully:', response.data);

      if (!Array.isArray(response.data)) {
        debugLog('[SliderService] Response is not an array');
        return [];
      }

      return response.data.map((item: any) => normalizeObjectMedia(item));
    } catch (error) {
      errorLog('[SliderService] Error fetching slider data:', error);
      throw error;
    }
  }
};
