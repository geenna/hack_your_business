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
    action: 'all',
    subject: 'Project_Manager',
  }, {
    title: 'CoWork',
    target: '_blank',
    icon: { icon: 'ri-organization-chart' },
    children: [{
      title: 'Servizi',
      to: { name: 'cowork-servizi' },
      action: 'all',
      subject: 'CoWorking',
    }, {
      title: 'Disponibilità',
      to: { name: 'cowork-disponibilita' },
      action: 'all',
      subject: 'CoWorking',
    }, {
      title: 'Lista Prenotazioni',
      to: { name: 'cowork-lista' },
      action: 'all',
      subject: 'CoWorking',
    }, {
      title: 'Nuova Prenotazione',
      to: { name: 'cowork-nuova' },
      action: 'all',
      subject: 'CoWorking',
    }
    ],
  },
  {
    title: 'Pagamenti',
    icon: { icon: 'ri-wallet-3-line' },
  },
  {
    title: 'Agenda',
    icon: { icon: 'ri-calendar-todo-line' },
    to: { name: 'calendar-main' },
  }
] as any
