/**
 * Created by mrakolice on 26.09.18.
 */

import {Asic} from '../../api/asic'

const state = {
  showSettingsForm: null,
  settingsForm:{

  }
}

const mutations = {
  setShowSettingsForm(state, newValue){
    state.showSettingsForm = newValue
  },
  setSettingsForm(state, newValue){
    state.settingsForm = newValue
  }
}

const actions = {
  fetchSettings({commit}, asic_id){
    Asic.settings(asic_id).then(response => {
      commit('setSettingsForm', {currentUsername:response.username, currentPassword:response.password})
    })
  },
  showSettingsForm({commit, dispatch}){
    commit('setShowSettingsForm', true)
  },
  hideSettingsForm({commit}){
    commit('setShowSettingsForm', false)
  },
  changePassword({commit, state}){
    Asic.changePassword(state.settingsForm.password).then(response => {
      if (response){
        commit('setSettingsForm', {currentUsername:state.settingsForm.username, currentPassword:state.settingsForm.password})
      }
    })
  }
}

const getters = {

}

export default {
  namespaced:true,
  state,
  mutations,
  actions,
  getters
}
