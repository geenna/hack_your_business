export const isLoading = ref(false);
const requestCount = ref(0);
export const startLoading = () => {
    requestCount.value++;
    isLoading.value = true;
};

export const stopLoading = () => {
    if (requestCount.value > 0) {
        requestCount.value--;
    }
    if (requestCount.value === 0) {
        isLoading.value = false;
    }
};
