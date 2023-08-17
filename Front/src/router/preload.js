import { log } from '../communs/LogError'
import { useSessionStore } from '../stores/session'

const domain = `${window.location.protocol}//${window.location.host}`

// charge un évènement
export async function event (to) {
  // console.log(`Près chargement d'un évènement !`)
  const { setLoadingValue, initFormEvent } = useSessionStore()
  try {
    setLoadingValue(true)
    const urlApi = `/api/eventslug/${to.params.slug}`
    const response = await fetch(domain + urlApi)
    if (response.status !== 200) {
      throw new Error(`${response.status} - ${response.statusText}`)
    }
    const retour = await response.json()
    setLoadingValue(false)
    initFormEvent(retour)
    // Une fois le chargement de l'évènement fait, aller à la page event.
    return true
  } catch (error) {
    setLoadingValue(false)
    log({ message: `loadEvent, /api/eventslug/${to.params.slug}, error: `, error })
    emitter.emit('modalMessage', {
      titre: 'Erreur',
      contenu: `Chargement de l'évènement '${to.params.slug}' -- erreur: ${error.message}`
    })
    return false
  }
}

// Charge tous les évènements
export async function events () {
  // console.log('Près chargement des évènements !')
  const { setLoadingValue, initFormEvent } = useSessionStore()
  try {
    setLoadingValue(true)
    const apiEvents = `/api/events/`
    const response = await fetch(domain + apiEvents)
    if (response.status !== 200) {
      throw new Error(`${response.status} - ${response.statusText}`)
    }
    return await response.json()
  } catch (error) {
    setLoadingValue(true)
    emitter.emit('modalMessage', {
      titre: 'Erreur',
      contenu: `Chargement des évènements  -- erreur: ${error.message}`
    })
    log({ message: 'load events: ' + error.message })
    return false
  }
}