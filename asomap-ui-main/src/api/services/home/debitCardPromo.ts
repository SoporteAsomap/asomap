import { httpClient } from '../../config/httpClient';
import type { IDebitCardPromoData } from '@/interfaces';
import { ENDPOINTS } from '@/constants';
import { normalizeObjectMedia } from '@/utils/media';

export const debitCardPromoService = {
  getDebitCardPromo: async (): Promise<IDebitCardPromoData> => {
    const response = await httpClient.get<IDebitCardPromoData>(
      ENDPOINTS.COLLECTIONS.HOME.DEBIT_CARD_PROMO
    );

    return normalizeObjectMedia(response.data);
  }
};
