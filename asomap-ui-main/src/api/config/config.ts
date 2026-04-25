
const ENV = import.meta.env.VITE_ENV || 'development';

// Detect production environment by URL (for 192.168.54.10:8080)
const isProductionByUrl = window.location.hostname === '192.168.54.10' ||
                         window.location.hostname.includes('asomap.com') ||
                         window.location.hostname.includes('production');

export const API_CONFIG = {
    // Environment
    ENV,
    IS_DEVELOPMENT: ENV === 'development' && !isProductionByUrl,
    IS_PRODUCTION: ENV === 'production' || isProductionByUrl,
    IS_STAGING: ENV === 'staging',
    IS_MOCK: ENV === 'mock',

    // API URLs based on environment
    BASE_URL: (ENV === 'development' && !isProductionByUrl)
        ? import.meta.env.VITE_API_BASE_URL || `${import.meta.env.VITE_NGINX_URL || 'http://localhost:8080'}/api`
        : import.meta.env.VITE_API_BASE_URL || `${window.location.origin}/api`,

    // Timeouts
    TIMEOUT: (ENV === 'development' && !isProductionByUrl) ? 10000 : 60000, // Aumentar timeout en producción

    // Headers
    HEADERS: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },

    // External APIs
    GOOGLE_MAPS_API_KEY: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,

    // Feature flags
    FEATURES: {
        DEBUG_LOGS: ENV === 'development' && !isProductionByUrl,
        MOCK_DATA: (ENV === 'development' && !isProductionByUrl) || ENV === 'mock',
        ANALYTICS: ENV === 'production' || isProductionByUrl,
        ERROR_REPORTING: ENV === 'production' || isProductionByUrl
    }
} as const;

// Debug information (always show in production for debugging)
console.log('🚀 ASOMAP API Configuration:', {
    environment: API_CONFIG.ENV,
    baseUrl: API_CONFIG.BASE_URL,
    timeout: API_CONFIG.TIMEOUT,
    features: API_CONFIG.FEATURES,
    googleMapsApiKey: API_CONFIG.GOOGLE_MAPS_API_KEY ? '✅ Configured' : '❌ Missing',
    serverIP: import.meta.env.VITE_SERVER_IP || 'Not set',
    serverPort: import.meta.env.VITE_SERVER_PORT || 'Not set',
    nginxUrl: import.meta.env.VITE_NGINX_URL || 'Not set',
    backendUrl: import.meta.env.VITE_BACKEND_URL || 'Not set',
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'Not set',
    mediaBaseUrl: import.meta.env.VITE_MEDIA_BASE_URL || 'Not set'
});

