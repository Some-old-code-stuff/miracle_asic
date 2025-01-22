/**
 * Created by mrakolice on 25.09.18.
 */
import {Auth} from '../../api/auth'
import axios from 'axios'
import {DEBUG} from './settings'

const state = {
  currentUser: getSavedState('auth.currentUser'),
  phone: null,
  isSendSmsToken: null,
  smsToken: null,
  tryCount: null,
}

const mutations = {
  SET_CURRENT_USER(state, newValue) {
    state.currentUser = newValue
    console.log(state.currentUser, 'setuser')
    saveState('auth.currentUser', newValue)
    setDefaultAuthHeaders(state)
  },
  SET_IS_SEND_SMS_TOKEN(state, newValue){
    state.isSendSmsToken = newValue
  },
  SET_SMS_TOKEN(state, newValue){
    state.smsToken = newValue
  },
  SET_PHONE(state, newValue){
    state.phone = newValue
  },
  setTryCount(state, newValue){
    state.tryCount = newValue
  },
}

const getters = {
  // Whether the user is currently logged in.
  loggedIn(state) {
    return !!state.currentUser
  },
}

const actions = {
  // This is automatically run in `src/state/store.js` when the app
  // starts, along with any other actions named `init` in other modules.
  init({state, dispatch}) {
    setDefaultAuthHeaders(state)
    dispatch('validate')
    dispatch('showPhone')
  },

  // Logs in the current user.
  login({commit, dispatch, getters, state}) {
    if (getters.loggedIn) return dispatch('validate')

    return Auth.tokenAuth(state.phone, state.smsToken).then(response => {
      if (response) {
        commit('SET_CURRENT_USER', response)
        commit('SET_SMS_TOKEN', '')
        commit('SET_IS_SEND_SMS_TOKEN', false)
        commit('SET_PHONE', '')
      }
      else {
        dispatch('alerts/dangerAlert', 'Введен неверный токен! Попытайтесь еще раз или переотправьте токен', {root: true})
      }


      return response
    })
  },

  // Logs out the current user.
  logout({commit}) {
    commit('SET_CURRENT_USER', null)
  },

  // Validates the current user's token and refreshes it
  // with new data from the API.
  validate({commit, state}) {
    console.log('validate')
    if (!state.currentUser) return Promise.resolve(null)

    return Auth.verifyToken(state.currentUser.token).then(response => {
      if (!response.payload) {
        commit('SET_CURRENT_USER', null)
        return false
      }
      return true
    })
  },
  sendSmsToken({commit, state, root}){
    Auth.sendSmsToken(state.phone).then(response => {
      if (response.ok) {
        commit('SET_IS_SEND_SMS_TOKEN', true)
        if (DEBUG) {
          commit('SET_SMS_TOKEN', response.token)
        }
      }
    })
  },
  checkSmsToken({commit, state, dispatch}, {actionName, params}){
    return Auth.checkSmsToken(state.phone, state.smsToken).then(response=>{
      if (response.ok){
        dispatch(actionName, params, {root:true})
        dispatch('showPhone')
      }
      else{
        commit('setTryCount', response.tryCount)
      }
      return response
    })
  },
  showPhone({commit}){
    commit('SET_IS_SEND_SMS_TOKEN', false)
  },
  updatePhone({commit}, newValue){
    commit('SET_PHONE', newValue)
  },
  updateSmsToken({commit}, newValue){
    commit('SET_SMS_TOKEN', newValue)
  }
}

// ===
// Private helpers
// ===

function getSavedState(key) {
  return JSON.parse(window.localStorage.getItem(key))
}

function saveState(key, state) {
  window.localStorage.setItem(key, JSON.stringify(state))
}

function setDefaultAuthHeaders(state) {
  axios.defaults.headers.common.Authorization = state.currentUser
    ? 'JWT ' + state.currentUser.token
    : ''
}

export default {
  namespaced: true,
  state,
  mutations,
  getters,
  actions
}
