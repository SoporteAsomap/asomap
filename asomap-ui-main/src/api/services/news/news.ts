import { httpClient } from '../../config/httpClient';
import { ENDPOINTS } from '@/constants';
import { debugLog, errorLog } from '@/utils/environment';
import { normalizeObjectMedia } from '@/utils/media';
import { newsData } from '@/mocks/news/newsData';
import type { INewsData } from '@/interfaces/news.interface';

export const newsService = {
  getNews: async (): Promise<INewsData> => {
    try {
      debugLog('[NewsService] Fetching news from backend');

      const response = await httpClient.get<any>(
        ENDPOINTS.COLLECTIONS.NEWS.ALL
      );

      debugLog('[NewsService] Backend response:', response.data);

      const results = response.data?.results || response.data || [];

      const transformedNews: INewsData = {
        ...newsData,
        slides: Array.isArray(results)
          ? results.map((item: any) => normalizeObjectMedia(item))
          : [],
      };

      debugLog('[NewsService] Transformed news data:', transformedNews);

      return transformedNews;
    } catch (error) {
      errorLog('[NewsService] Error fetching news data:', error);
      return newsData;
    }
  }
};
