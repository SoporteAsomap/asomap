import { httpClient } from '../../config/httpClient';
import { ENDPOINTS } from '@/constants';
import { debugLog, errorLog } from '@/utils/environment';
import type {
  IAbandonedAccountsAPIResponse,
  IAbandonedAccountsData,
  IAccountTypeData,
  IYearData,
  IDocumentData
} from '@/interfaces';

export const abandonedAccountsService = {
  getAbandonedAccounts: async (): Promise<IAbandonedAccountsData | null> => {
    try {
      debugLog('[AbandonedAccountsService] Fetching abandoned accounts data');
      
      const response = await httpClient.get<IAbandonedAccountsAPIResponse>(
        ENDPOINTS.COLLECTIONS.USER_SUPPORT.ABANDONED_ACCOUNTS
      );

      if (response.data.results.length === 0) {
        debugLog('[AbandonedAccountsService] No abandoned accounts data found');
        return null;
      }

      const apiData = response.data.results[0]; // Tomamos el primer resultado

      // Transformar account_types
      const accountTypes: IAccountTypeData[] = apiData.account_types.map(type => ({
        id: type.id,
        label: type.label,
        description: type.description
      }));

      // Transformar years y documents
      const years: IYearData[] = apiData.years.map(year => {
        const documents = year.documents;

        // Crear un array de documentos con todos los documentos
        const allDocuments: IDocumentData[] = [];

        // Iterar sobre todas las claves del objeto documents
        Object.entries(documents).forEach(([key, doc]) => {
          // Extraer el tipo del documento desde la clave (formato: accountTypeId_type_docId)
          const parts = key.split('_');
          if (parts.length === 3) {
            const accountTypeId = parseInt(parts[0]);
            const docType = parts[1]; // 'abandoned' o 'inactive'

            allDocuments.push({
              title: doc.title || '',
              url: doc.url || '',
              date: doc.date || '',
              id: doc.id,
              type: docType,
              accountTypeId: accountTypeId
            });
          }
        });

        return {
          year: year.year,
          documents: allDocuments
        };
      });

      const transformedData: IAbandonedAccountsData = {
        id: apiData.id,
        title: apiData.title,
        description: apiData.description,
        accountTypes,
        years
      };

      debugLog('[AbandonedAccountsService] Abandoned accounts data fetched successfully:', transformedData);
      return transformedData;

    } catch (error) {
      errorLog('[AbandonedAccountsService] Error fetching abandoned accounts data:', error);
      throw error;
    }
  }
};
