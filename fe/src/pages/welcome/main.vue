<script setup lang="ts">
import { ref } from 'vue'
import { themeConfig } from '@themeConfig'
import { VNodeRenderer } from '@layouts/components/VNodeRenderer'

definePage({
  path: '/welcome',
  meta: {
    layout: 'blank',
  },
})

const showNextStepModal = ref(false)

const onGetSpace = () => {
  showNextStepModal.value = true
}
</script>

<template>
  <div class="welcome-container">
    <!-- Glowing background elements for premium feel -->
    <div class="glow-orb orb-1"></div>
    <div class="glow-orb orb-2"></div>
    <div class="glow-orb orb-3"></div>

    <!-- Header / Custom transparent glassmorphism navbar -->
    <header class="glass-navbar">
      <div class="navbar-content">
        <div class="logo-area">
          <VNodeRenderer :nodes="themeConfig.app.logo" class="logo-icon" />
          <span class="app-title">{{ themeConfig.app.title }}</span>
        </div>
        <div class="nav-links">
          <a href="#features" class="nav-link">Servizi</a>
          <a href="#about" class="nav-link">Chi Siamo</a>
          <VBtn
            variant="tonal"
            color="primary"
            class="nav-cta"
            @click="onGetSpace"
          >
            Prenota Ora
          </VBtn>
          <a href="/login" class="nav-link">Accedi</a>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="hero-section">
      <VContainer>
        <VRow align="center" justify="center" class="text-center py-16">
          <VCol cols="12" md="10" lg="8">
            <div class="badge-container mb-6">
              <span class="badge-text">✨ Il Futuro del Lavoro è Qui</span>
            </div>
            
            <h1 class="hero-title mb-6">
              Lavora in modo intelligente,<br />
              <span class="gradient-text">condividi le tue idee.</span>
            </h1>
            
            <p class="hero-subtitle mb-8">
              Spazi di coworking moderni, tecnologici e stimolanti progettati per freelance, startup e team innovativi. Trova la concentrazione di cui hai bisogno e cresci insieme a una community vivace.
            </p>

            <div class="cta-container">
              <VBtn
                size="x-large"
                color="primary"
                class="cta-button pulse-animation"
                @click="onGetSpace"
              >
                <VIcon start icon="ri-community-line" class="mr-2" />
                Ottieni il tuo spazio
              </VBtn>
            </div>
          </VCol>
        </VRow>
      </VContainer>
    </section>

    <!-- Features Section -->
    <section id="features" class="features-section">
      <VContainer>
        <VRow justify="center" class="mb-12">
          <VCol cols="12" md="8" class="text-center">
            <h2 class="section-title">I Nostri Spazi & Servizi</h2>
            <p class="section-subtitle">
              Scegli la soluzione perfetta per le tue esigenze lavorative giornaliere o a lungo termine.
            </p>
          </VCol>
        </VRow>

        <VRow>
          <!-- Feature 1 -->
          <VCol cols="12" sm="6" md="3">
            <VCard class="feature-card h-100" flat>
              <VCardText class="d-flex flex-column align-center text-center pa-6">
                <div class="icon-wrapper mb-4">
                  <VIcon size="36" color="primary" icon="ri-computer-line" />
                </div>
                <h3 class="feature-title mb-2">Scrivania Condivisa</h3>
                <p class="feature-desc mb-0">
                  Accedi a postazioni flessibili in un ambiente open-space dinamico, ideale per fare networking.
                </p>
              </VCardText>
            </VCard>
          </VCol>

          <!-- Feature 2 -->
          <VCol cols="12" sm="6" md="3">
            <VCard class="feature-card h-100" flat>
              <VCardText class="d-flex flex-column align-center text-center pa-6">
                <div class="icon-wrapper mb-4">
                  <VIcon size="36" color="primary" icon="ri-briefcase-line" />
                </div>
                <h3 class="feature-title mb-2">Ufficio Privato</h3>
                <p class="feature-desc mb-0">
                  Uno spazio riservato e completamente arredato per te e il tuo team, con la massima privacy.
                </p>
              </VCardText>
            </VCard>
          </VCol>

          <!-- Feature 3 -->
          <VCol cols="12" sm="6" md="3">
            <VCard class="feature-card h-100" flat>
              <VCardText class="d-flex flex-column align-center text-center pa-6">
                <div class="icon-wrapper mb-4">
                  <VIcon size="36" color="primary" icon="ri-slideshow-line" />
                </div>
                <h3 class="feature-title mb-2">Sale Riunioni</h3>
                <p class="feature-desc mb-0">
                  Sale tecnologicamente avanzate per presentazioni, pitch e meeting di successo con i tuoi clienti.
                </p>
              </VCardText>
            </VCard>
          </VCol>

          <!-- Feature 4 -->
          <VCol cols="12" sm="6" md="3">
            <VCard class="feature-card h-100" flat>
              <VCardText class="d-flex flex-column align-center text-center pa-6">
                <div class="icon-wrapper mb-4">
                  <VIcon size="36" color="primary" icon="ri-wifi-line" />
                </div>
                <h3 class="feature-title mb-2">Super Connessione</h3>
                <p class="feature-desc mb-0">
                  Fibra ultra-veloce da 1Gbps, stampanti laser e caffè illimitato per non fermare mai la tua produttività.
                </p>
              </VCardText>
            </VCard>
          </VCol>
        </VRow>
      </VContainer>
    </section>

    <!-- Footer -->
    <footer class="welcome-footer py-8">
      <VContainer class="text-center">
        <p class="mb-0 text-body-2 text-disabled">
          &copy; {{ new Date().getFullYear() }} {{ themeConfig.app.title }}. Tutti i diritti riservati. Progettato con passione per l'innovazione.
        </p>
      </VContainer>
    </footer>

    <!-- Premium Interactive Modal for Next Steps -->
    <VDialog v-model="showNextStepModal" max-width="500">
      <VCard class="premium-dialog-card">
        <VCardText class="text-center pa-8">
          <div class="dialog-icon-wrapper mb-6">
            <VIcon size="64" color="primary" icon="ri-compass-3-line" />
          </div>
          <h3 class="text-h4 mb-4 font-weight-bold dialog-title">Pronto a Partire!</h3>
          <p class="text-body-1 text-secondary mb-6 leading-relaxed">
            La navigazione e il wizard per la prenotazione dello spazio di coworking (per utenti registrati e ospiti) verranno attivati nel prossimo step di sviluppo!
          </p>
          <VBtn color="primary" block size="large" @click="showNextStepModal = false">
            Fantastico, andiamo avanti!
          </VBtn>
        </VCardText>
      </VCard>
    </VDialog>
  </div>
</template>

<style scoped lang="scss">
.welcome-container {
  background-color: #0f172a; /* Slate 900 */
  color: #f8fafc;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  font-family: 'Inter', sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* Glowing decorative background orbs */
.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(150px);
  opacity: 0.15;
  z-index: 0;
  pointer-events: none;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: #6366f1; /* Indigo 500 */
  top: -100px;
  left: -100px;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: #a855f7; /* Purple 500 */
  bottom: 10%;
  right: -150px;
}

.orb-3 {
  width: 300px;
  height: 300px;
  background: #06b6d4; /* Cyan 500 */
  top: 40%;
  left: 20%;
}

/* Glassmorphism navbar */
.glass-navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.navbar-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-baseline: center;
  align-items: center;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  width: 32px;
  height: 32px;
  color: #a855f7;
}

.app-title {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-link {
  color: #94a3b8;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: color 0.2s ease;

  &:hover {
    color: #f8fafc;
  }
}

.nav-cta {
  font-weight: 600;
  text-transform: none;
  letter-spacing: normal;
}

/* Hero Section */
.hero-section {
  position: relative;
  z-index: 1;
  padding-top: 6rem;
  padding-bottom: 3rem;
}

.badge-container {
  display: inline-block;
  background: rgba(168, 85, 247, 0.1);
  border: 1px solid rgba(168, 85, 247, 0.25);
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  backdrop-filter: blur(4px);
}

.badge-text {
  font-size: 0.85rem;
  font-weight: 600;
  color: #d8b4fe;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -0.03em;
  color: #ffffff;

  @media (max-width: 600px) {
    font-size: 2.25rem;
  }
}

.gradient-text {
  background: linear-gradient(135deg, #a855f7 0%, #6366f1 50%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 1.25rem;
  line-height: 1.6;
  color: #94a3b8;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;

  @media (max-width: 600px) {
    font-size: 1rem;
  }
}

.cta-button {
  font-size: 1.1rem !important;
  font-weight: 700 !important;
  text-transform: none !important;
  letter-spacing: normal !important;
  padding: 0 2.5rem !important;
  height: 54px !important;
  border-radius: 12px !important;
  box-shadow: 0 10px 25px -5px rgba(168, 85, 247, 0.4) !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 30px -5px rgba(168, 85, 247, 0.5) !important;
  }
}

/* Pulse animation for CTA button */
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(168, 85, 247, 0.5);
  }
  70% {
    box-shadow: 0 0 0 15px rgba(168, 85, 247, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(168, 85, 247, 0);
  }
}

.pulse-animation {
  animation: pulse 2.5s infinite;
}

/* Features Section */
.features-section {
  position: relative;
  z-index: 1;
  padding-top: 2rem;
  padding-bottom: 4rem;
}

.section-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.section-subtitle {
  font-size: 1.1rem;
  color: #94a3b8;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.feature-card {
  background: rgba(30, 41, 59, 0.4) !important;
  border: 1px solid rgba(255, 255, 255, 0.05) !important;
  border-radius: 16px !important;
  backdrop-filter: blur(8px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;

  &:hover {
    transform: translateY(-5px);
    background: rgba(30, 41, 59, 0.7) !important;
    border-color: rgba(168, 85, 247, 0.3) !important;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2) !important;

    .icon-wrapper {
      background: rgba(168, 85, 247, 0.2);
      transform: scale(1.1);
    }
  }
}

.icon-wrapper {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  background: rgba(168, 85, 247, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.feature-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #f8fafc;
}

.feature-desc {
  font-size: 0.9rem;
  line-height: 1.5;
  color: #94a3b8;
}

/* Welcome Footer */
.welcome-footer {
  position: relative;
  z-index: 1;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(15, 23, 42, 0.8);
}

/* Premium Dialog Card styling */
.premium-dialog-card {
  background: #1e293b !important; /* Slate 800 */
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  border-radius: 24px !important;
  color: #f8fafc !important;
}

.dialog-icon-wrapper {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  background: rgba(168, 85, 247, 0.15);
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed rgba(168, 85, 247, 0.3);
}

.dialog-title {
  background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
