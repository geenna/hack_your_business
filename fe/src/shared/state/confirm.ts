export interface ConfirmState {
    isVisible: boolean;
    title: string;
    message: string;
}

const state = reactive<ConfirmState>({
    isVisible: false,
    title: '',
    message: '',
});

let resolvePromise: ((value: boolean) => void) | null = null;

export const useConfirm = () => {
    return {
        state: readonly(state),
        show: (title: string, message: string): Promise<boolean> => {
            state.title = title;
            state.message = message;
            state.isVisible = true;
            return new Promise((resolve) => {
                resolvePromise = resolve;
            });
        },
        confirm: () => {
            state.isVisible = false;
            if (resolvePromise) {
                resolvePromise(true);
                resolvePromise = null;
            }
        },
        cancel: () => {
            state.isVisible = false;
            if (resolvePromise) {
                resolvePromise(false);
                resolvePromise = null;
            }
        }
    };
};
