/**
 * Created by mrakolice on 27.09.18.
 */

import {Balance} from '../../api/balance'
import fecha from 'fecha'


export const state = {
  balanceData: [],
  balanceId: null,
  modalCounter: {},
  dates: []
}

export const mutations = {
  setBalanceData(state, newValue){
    state.balanceData = newValue
  },
  updateDates(state){
    state.dates = [...new Set(state.balanceData.map(elem => elem.date.split('-')[0]))].map(elem => {
      return {value: elem, text: elem}
    })
  },
  setBalanceId(state, newValue){
    state.balanceId = newValue
  },
  deleteCounterRecord(state, recordId){
    state.balanceData.splice(state.balanceData.findIndex(elem => elem.id == recordId), 1)
  },
  deleteCounter(state, {recordId, counterId}){
    const balance = state.balanceData.find(elem => elem.id == recordId)
    balance.counters.splice(balance.counters.findIndex(elem => elem.id == counterId), 1)
  },
  setModalCounter(state, counter){
    state.modalCounter = counter
  },
  setModalCounterField(state, {value, fieldName}){
    state.modalCounter[fieldName] = value
  },
  resetModalCounter(state){
    state.modalCounter = {
      approvedTariff: null,
      koefficient: null,
      name: null,
      value: null,
      preliminaryTariff: null,
      testTariff: null
    }
  },
  canEditCounterRecord(state, record){
    record.canEdit = true
    state.balanceData.splice(state.balanceData.findIndex(elem => elem.id == record.id), 1, record)
  }
}

export const actions = {
  addCounterRecord({commit, dispatch}, date){
    console.log(date, fecha.format(date, 'YYYY-MM-DD'))
    Balance.addCounterRecord(fecha.format(date, 'YYYY-MM-DD')).then(response => {
      if (response.ok) {
        dispatch('alerts/successAlert', 'Запись успешно добавлена!', {root: true})
        dispatch('fetchBalance')
      }
      else {
        dispatch('alerts/dangerAlert', 'К сожалению, произошла ошибка при добавлении записи.', {root: true})
      }
    })
  },
  fetchBalance({commit}){
    return Balance.getBalance().then(response => {
      commit('setBalanceData', response)
      commit('updateDates')
    })
  },
  setBalanceId({commit, state}, id){
    commit('setBalanceId', id)
    console.log(state.balanceId, id)
  },
  addOrUpdateCounter({commit, dispatch}, counter){
    if (counter.id) {
      dispatch('updateCounter', counter)
    }
    else {
      dispatch('addCounter', counter)
    }
    commit('resetModalCounter')
  },
  updateCounter({commit, dispatch}, counter){
    Balance.updateCounter(counter).then(response => {
      if (response) {
        dispatch('alerts/successAlert', 'Счетчик успешно обновлен!', {root: true})
      }
      else {
        dispatch('alerts/dangerAlert', 'К сожалению, произошла ошибка при обновлении счетчика.', {root: true})
      }
    })
  },
  addCounter({commit, dispatch, state}, newCounter){
    Balance.addCounter(newCounter, state.balanceId).then(response => {
      if (response.ok) {
        dispatch('alerts/successAlert', 'Счетчик успешно добавлен!', {root: true})
        dispatch('fetchBalance')
      }
      else {
        dispatch('alerts/dangerAlert', 'К сожалению, произошла ошибка при добавлении счетчика.', {root: true})
      }
    })
  },
  deleteCounterRecord({commit, dispatch}, recordId){
    Balance.deleteCounterRecord(recordId).then(response => {
      if (response) {
        dispatch('alerts/successAlert', 'Запись успешно удалена!', {root: true})
        commit('deleteCounterRecord', recordId)
        commit('updateDates')
      }
      else {
        dispatch('alerts/dangerAlert', 'К сожалению, произошла ошибка при удалении записи.', {root: true})
      }
    })
  },
  deleteCounter({commit, dispatch}, {counterId, recordId}){
    Balance.deleteCounter(counterId).then(response => {
      if (response) {
        dispatch('alerts/successAlert', 'Счетчик успешно удален!', {root: true})
        commit('deleteCounter', {counterId, recordId})
      }
      else {
        dispatch('alerts/dangerAlert', 'К сожалению, произошла ошибка при удалении счетчика.', {root: true})
      }
    })
  },
  canEdit({commit}, record){
    commit('canEditCounterRecord', record)
  }
}

export const getters = {}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}

