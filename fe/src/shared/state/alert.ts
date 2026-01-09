export interface AlertState {
    isVisible: boolean;
    title: string;
    message: string;
    type: 'success' | 'error' | 'warning' | 'info';
}

const state = reactive<AlertState>({
    isVisible: false,
    title: '',
    message: '',
    type: 'info',
});

export const useAlert = () => {
    return {
        state: readonly(state),
        show: (title: string, message: string, type: 'success' | 'error' | 'warning' | 'info' = 'info') => {
            state.title = title;
            state.message = message;
            state.type = type;
            state.isVisible = true;
        },
        hide: () => {
            state.isVisible = false;
        }
    };
};
