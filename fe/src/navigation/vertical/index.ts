export default [
  {
    title: 'Dashboard',
    icon: { icon: 'ri-home-smile-line' },
    to: { name: 'root' },
  },
  {
    title: 'Utenti',
    to: { name: 'users-main' },
    icon: { icon: 'ri-group-line' },
  },
  {
    title: 'Progetti',
    to: { name: 'project-main' },
    icon: { icon: 'ri-file-text-line' },

    children: [{
      title: 'Overview',
      to: { name: 'project-main' },
      action: 'all',
      subject: 'project',
    }, {
      title: 'Nuovo',
      to: { name: 'project-new' },
    }]
  },
  {
    title: 'CoWork',
    target: '_blank',
    icon: { icon: 'ri-file-text-line' },
  },
  {
    title: 'Pagamenti',

    target: '_blank',
  },
  {
    title: 'Agenda',

    icon: { icon: 'ri-file-text-line' },
    target: '_blank',
  }
]
