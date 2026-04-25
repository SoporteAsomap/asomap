export const API_BASE = "https://app-asomap-backend-12345.azurewebsites.net";

export const normalizeMediaUrl = (url?: string | null): string => {
  if (!url) return "";

  const cleanUrl = String(url).trim();
  if (!cleanUrl) return "";

  if (cleanUrl.startsWith("http://") || cleanUrl.startsWith("https://")) {
    return cleanUrl;
  }

  if (cleanUrl.startsWith("/")) {
    return `${API_BASE}${cleanUrl}`;
  }

  return `${API_BASE}/${cleanUrl}`;
};

export const normalizeObjectMedia = <T extends Record<string, any>>(obj: T): T => {
  const imageLikeKeys = new Set([
    "image",
    "image_url",
    "bannerImage",
    "banner_image",
    "accountImage",
    "account_image",
    "cardImage",
    "card_image",
    "certificateImage",
    "certificate_image",
    "loanImage",
    "loan_image",
    "desktop_image",
    "mobile_image",
    "thumbnail",
    "pdf_url",
    "file",
    "file_url",
    "imageTablet",
    "imageMobile",
    "imageSrc",
    "image_src",
  ]);

  const clone: Record<string, any> = { ...obj };

  for (const key of Object.keys(clone)) {
    const value = clone[key];

    if (typeof value === "string" && imageLikeKeys.has(key)) {
      clone[key] = normalizeMediaUrl(value);
      continue;
    }

    if (Array.isArray(value)) {
      clone[key] = value.map((item) =>
        item && typeof item === "object" ? normalizeObjectMedia(item) : item
      );
      continue;
    }

    if (value && typeof value === "object") {
      clone[key] = normalizeObjectMedia(value);
    }
  }

  return clone as T;
};
