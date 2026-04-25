import { ENDPOINTS } from '@/constants';
import { AboutResponse } from '@/interfaces';
import { errorLog, getApiUrl } from '@/utils/environment';
import { normalizeMediaUrl } from '@/utils/media';

const extractData = (response: any): any => {
  if (response && typeof response === 'object' && 'results' in response) {
    if (Array.isArray(response.results)) {
      return response.results;
    }
    return response.results;
  }
  return response;
};

const safeFetchJson = async (url: string): Promise<any | null> => {
  try {
    const response: Response = await fetch(url);

    if (!response.ok) {
      return null;
    }

    const data: any = await response.json();
    return data;
  } catch {
    return null;
  }
};

export const aboutService = {
  getAbout: async (): Promise<AboutResponse> => {
    try {
      const [
        heroRaw,
        quienesSomosRaw,
        historiaRaw,
        misionRaw,
        visionRaw,
        valoresRaw,
      ] = await Promise.all([
        safeFetchJson(getApiUrl(ENDPOINTS.COLLECTIONS.ABOUT.HERO)),
        safeFetchJson(getApiUrl(ENDPOINTS.COLLECTIONS.ABOUT.ABOUT_US)),
        safeFetchJson(getApiUrl(ENDPOINTS.COLLECTIONS.ABOUT.OUR_HISTORY)),
        safeFetchJson(getApiUrl(ENDPOINTS.COLLECTIONS.ABOUT.MISION)),
        safeFetchJson(getApiUrl(ENDPOINTS.COLLECTIONS.ABOUT.VISION)),
        safeFetchJson(getApiUrl(ENDPOINTS.COLLECTIONS.ABOUT.VALUES)),
      ]);

      const getAllConsejoDirectores = async (): Promise<any[]> => {
        const allDirectores: any[] = [];
        let nextUrl: string | null = getApiUrl(ENDPOINTS.COLLECTIONS.ABOUT.DIRECTOR_BOARD);

        while (nextUrl) {
          try {
            const response: Response = await fetch(nextUrl);

            if (!response.ok) {
              break;
            }

            const data: any = await response.json();

            if (data.results && Array.isArray(data.results)) {
              allDirectores.push(...data.results);
            }

            nextUrl = data.next || null;
          } catch {
            break;
          }
        }

        return allDirectores.sort((a, b) => a.id - b.id);
      };

      const consejo = await getAllConsejoDirectores();

      const hero = extractData(heroRaw);
      const quienesSomos = extractData(quienesSomosRaw);
      const historia = extractData(historiaRaw);
      const mision = extractData(misionRaw);
      const vision = extractData(visionRaw);
      const valores = extractData(valoresRaw);

      const heroData = Array.isArray(hero) ? hero[0] : hero;
      const quienesSomosData = Array.isArray(quienesSomos) ? quienesSomos[0] : quienesSomos;
      const historiaData = Array.isArray(historia) ? historia[0] : historia;
      const misionData = Array.isArray(mision) ? mision[0] : mision;
      const visionData = Array.isArray(vision) ? vision[0] : vision;
      const valoresData = valores;

      return {
        hero: {
          title: heroData?.title || heroData?.Title || 'Sobre Nosotros',
          description: heroData?.description || heroData?.Description || '',
        },

        quienesSomos: {
          title: quienesSomosData?.title || quienesSomosData?.Title || 'Quiénes Somos',
          paragraphs: quienesSomosData?.paragraphs || quienesSomosData?.Paragraphs || '',
          imageSrc: normalizeMediaUrl(quienesSomosData?.image_src || quienesSomosData?.ImageSrc || ''),
          imageAlt: quienesSomosData?.image_alt || quienesSomosData?.ImageAlt || 'Quiénes Somos',
        },

        nuestraHistoria: {
          title: historiaData?.title || historiaData?.Title || 'Nuestra Historia',
          paragraphs: historiaData?.paragraphs || historiaData?.Paragraphs || '',
          imageSrc: normalizeMediaUrl(historiaData?.image_src || historiaData?.ImageSrc || ''),
          imageAlt: historiaData?.image_alt || historiaData?.ImageAlt || 'Nuestra Historia',
        },

        mision: {
          title: misionData?.title || misionData?.Title || 'Nuestra Misión',
          description: misionData?.description || misionData?.Description || '',
        },

        vision: {
          title: visionData?.title || visionData?.Title || 'Nuestra Visión',
          description: visionData?.description || visionData?.Description || '',
        },

        valores: {
          title: 'Nuestros Valores',
          items: Array.isArray(valoresData)
            ? valoresData.map((valor: any) => ({
                title: valor.title || valor.Title || '',
                description: valor.description || valor.Description || '',
                icon: 'FaPeopleArrows',
              }))
            : [],
        },

        consejoDirectores: Array.isArray(consejo)
          ? consejo.map((director: any) => ({
              name: director.name || director.Name || '',
              position: director.position || director.Position || '',
              imageSrc: normalizeMediaUrl(director.image_src || director.ImageSrc || ''),
              imageAlt: director.image_alt || director.ImageAlt || '',
            }))
          : [],
      };
    } catch (error) {
      errorLog('[AboutService] Error fetching about data:', error);
      throw new Error('Failed to fetch about data');
    }
  },
};
