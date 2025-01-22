/**
 * Created by mrakolice on 26.09.18.
 */
import {Error} from '../../api/error'

export const state = {
  modalErrors: [],
}

export const mutations = {
  setModalErrors(state, modalErrors){
    state.modalErrors = modalErrors
  },
  deleteModalError(state, error){
    state.modalErrors.splice(state.modalErrors.findIndex(elem => elem.id == error.id), 1)
  },
  setErrorStatus(state, {error, statusObj}){
    error.statusValue = statusObj.statusValue
    error.status = statusObj.status
  }
}

export const actions = {
  fetchAsicErrors({commit}, {asicId, fieldName, objectId}){
    Error.asicErrors(asicId, fieldName, objectId).then(response => {
      commit('setModalErrors', response)
    })
  },

  setModalErrors({commit}, modalErrors){
    commit('setModalErrors', modalErrors)
  },

  toPending({commit, dispatch}, error){
    Error.toPending(error.id).then(response => {
      console.log(response)
      if (response != undefined) {
        commit('setErrorStatus', {error, statusObj: response})
        dispatch('alerts/successAlert', 'Ошибка успешно переведена в работу!', {root: true})
      } else {
        dispatch('alerts/dangerAlert', 'Произошли непредвиденные проблемы во время выполнения этого действия! Обратитесь к систмному администратору!', {root: true})
      }
    })
  },
  closeError({commit, dispatch}, error){
    Error.closeError(error.id).then(response => {
      console.log(response)
      if (response != undefined) {
        commit('setErrorStatus', {error, statusObj: response})
        dispatch('alerts/successAlert', 'Ошибка успешно решена!', {root: true})
      } else {
        dispatch('alerts/dangerAlert', 'Произошли непредвиденные проблемы во время выполнения этого действия! Обратитесь к систмному администратору!', {root: true})
      }
    })
  },
  toError({commit, dispatch}, error){
    Error.toError(error.id).then(response => {
      console.log(response)
      if (response != undefined) {
        dispatch('alerts/successAlert', 'Уровень уведомления успешно повышен!', {root: true})
        commit('deleteModalError', error)
      } else {
        dispatch('alerts/dangerAlert', 'Произошли непредвиденные проблемы во время выполнения этого действия! Обратитесь к системному администратору!', {root: true})
      }
    })
  },
  toWarning({commit, dispatch}, error){
    Error.toWarning(error.id).then(response => {
      console.log(response)
      if (response != undefined) {
        dispatch('alerts/successAlert', 'Уровень ошибки успешно понижен!', {root: true})
        commit('deleteModalError', error)
      } else {
        dispatch('alerts/dangerAlert', 'Произошли непредвиденные проблемы во время выполнения этого действия! Обратитесь к систмному администратору!', {root: true})
      }
    })
  },
}

export const getters = {}

export default{
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
