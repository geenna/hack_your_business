import axios from 'axios';
import { useCookie } from '@core/composable/useCookie';
import { startLoading, stopLoading } from '@/shared/state/loading';
import { router } from '@/plugins/1.router';
import { useAlert } from '@/shared/state/alert';
import { breakpoints } from 'vuetify/lib/composables/display.mjs';
const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});


api.interceptors.request.use(
    (config) => {
        startLoading()
        // userCookie returns a Ref. Accessing .value gets the current cookie value.
        const token = useCookie('accessToken').value;
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        stopLoading()
        return Promise.reject(error);
    }
);

api.interceptors.response.use(
    (response) => {
        stopLoading()
        return response;
    },
    async (error) => {
        stopLoading()
        if (error.response && (error.response.status === 401
            || error.response.status === 403)) {
            // Token expired or invalid
            // Clear the cookie
            const token = useCookie('accessToken');
            token.value = null;

            // Optional: Also clear user data
            useCookie('userData').value = null;
            useCookie('userAbilityRules').value = null;
            router.push('/not-authorized')
        }
        else {
            const { show } = useAlert()
            const detail = error.response?.data?.detail
            let message = error.message || 'Si è verificato un errore imprevisto';

            if (detail) {
                if (Array.isArray(detail)) {
                    // Gestione errori di validazione Pydantic (422)
                    message = detail.map((e: any) => e.msg).join('\n')
                } else {
                    // Gestione errori standard HTTP (es. 400)
                    message = detail
                }
            }

            show('Attenzione', message, "error")
        }

        return Promise.reject(error);
    }
);

export default api;
