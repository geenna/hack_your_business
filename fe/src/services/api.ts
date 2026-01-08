import axios from 'axios';
import { useCookie } from '@core/composable/useCookie';
import { startLoading, stopLoading } from '@/shared/state/loading';
import { router } from '@/plugins/1.router';

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
        return Promise.reject(error);
    }
);

export default api;
