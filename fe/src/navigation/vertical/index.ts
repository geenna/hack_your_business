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
    icon: { icon: 'ri-file-text-line' },
    to: { name: 'project-main' },
  },
  {
    title: 'CoWork',
    target: '_blank',
    icon: { icon: 'ri-file-text-line' },
    children: [
      {
        title: 'Servizi',
         to: { name: 'cowork-servizi' },
      },{
        title: 'Disponibilità',
         to: { name: 'cowork-disponibilita' },
      },
      {
        title: 'Prenotazioni',
        target: '_blank',
      }
    ],
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
] as any
