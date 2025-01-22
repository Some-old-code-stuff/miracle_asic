/**
 * Created by mrakolice on 26.09.18.
 */
export const state = {
  alerts: []
}

export const mutations = {

  addAlert(state, {message, variant}){
    state.alerts.push({message: message, variant: variant})
  },
  deleteAlert(state, alert){
    state.alerts.splice(state.alerts.findIndex(function (elem) {
      return elem.message == alert.message && elem.variant == alert.variant
    }), 1)
  },
}

export const actions = {
  deleteAlert({commit}, alert){
    commit('deleteAlert', alert)
  },

  infoAlert({commit}, message){
    commit('addAlert', {message, variant:'info'})
  },
  successAlert({commit}, message){
    commit('addAlert', {message, variant:'success'})
  },
  dangerAlert({commit}, message){
    commit('addAlert', {message, variant:'danger'})
  },
  warningAlert({commit}, message){
    commit('addAlert', {message, variant:'warning'})
  },
}

export const getters = {

}

export default{
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
