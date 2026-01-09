//const emailRouteComponent = () => import('@/pages/apps/email/index.vue')

// 👉 Redirects
export const redirects = [
    // ℹ️ We are redirecting to different pages based on role.
    // NOTE: Role is just for UI purposes. ACL is based on abilities.
    {
        path: '/',
        name: 'index',
        redirect: (to: any) => {
            // TODO: Get type from backend
            const userData = useCookie<any>('userData')
            const userRole = userData.value?.userType
            if (userRole === 'admin')
                return { name: 'dashboard' }
            /*if (userRole === 'client')
                return { name: 'access-control' }*/

            return { name: 'login', query: to.query }
        },
    }, {
        path: '/root',
        name: 'root',
        redirect: (to: any) => {

            const userData = useCookie<any>('userData')
            const userRole = userData.value?.userType
            if (userRole === 'admin')
                return { name: 'dashboard' }
            /*if (userRole === 'client')
                return { name: 'access-control' }*/

            return { name: 'login', query: to.query }
        },
    },
    /*{
      path: '/pages/user-profile',
      name: 'pages-user-profile',
      redirect: () => ({ name: 'pages-user-profile-tab', params: { tab: 'profile' } }),
    },
    {
      path: '/pages/account-settings',
      name: 'pages-account-settings',
      redirect: () => ({ name: 'pages-account-settings-tab', params: { tab: 'account' } }),
    },*/
]
export const routes = [
    // Email filter
    /* {
       path: '/apps/email/filter/:filter',
       name: 'apps-email-filter',
       component: emailRouteComponent,
       meta: {
         navActiveLink: 'apps-email',
         layoutWrapperClasses: 'layout-content-height-fixed',
       },
     }*/
]
