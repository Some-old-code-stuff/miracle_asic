/**
 * Created by mrakolice on 26.09.18.
 */

import Vue from 'vue';
import {Asic}from '../../api/asic'
import {Client}from '../../api/client'
import {Farm}from '../../api/farm'

import {getField, updateField} from 'vuex-map-fields'

export const state = {
  groupEditForm: {},
  searchForm: {},
  asics: [],
  selectedAsics: [],
  dashboardAsics: [],
  loading: false,
  modalAsic: {},
  asic: {}
}

function setRowVariant(asic) {
  asic._rowVariant = ''
  if (asic.openErrors.length > 0) {
    asic._rowVariant = 'danger'
  }
  else if (asic.openWarnings.length > 0) {
    asic._rowVariant = 'warning'
  }
}

export const mutations = {
  updateField,
  setModalAsic(state, modalAsic){
    state.modalAsic = modalAsic
  },

  setSearchForm(state, searchForm){
    state.searchForm = searchForm
  },
  setGroupEditForm(state, groupEditForm){
    state.groupEditForm = groupEditForm
  },

  setAsics(state, searchAsics){
    state.asics = searchAsics
    for (const asic of state.asics) {
      asic.errors = asic.errorsList
      const hasConnectError = asic.errors.find(elem => elem.message.includes('Проблемы с соединением') && elem.levelValue == 2)
      const hasConnectWarning = asic.errors.find(elem => elem.message.includes('Проблемы с соединением') && elem.levelValue == 1)
      const openErrors = asic.errors.filter(elem => elem.levelValue == 2)
      const openWarnings = asic.errors.filter(elem => elem.levelValue == 1)
      asic.hasConnectError = hasConnectError
      asic.hasConnectWarning = hasConnectWarning
      asic.openErrors = openErrors
      asic.openWarnings = openWarnings
      setRowVariant(asic)
    }
  },
  setDashboardAsics(state, dashboardAsics){
    for (const asic of dashboardAsics) {
      asic.errors = asic.errorsList
      const hasConnectError = asic.errors.find(elem => elem.message.includes('Проблемы с соединением') && elem.levelValue == 2)
      const hasConnectWarning = asic.errors.find(elem => elem.message.includes('Проблемы с соединением') && elem.levelValue == 1)
      const openErrors = asic.errors.filter(elem => elem.levelValue == 2)
      const openWarnings = asic.errors.filter(elem => elem.levelValue == 1)

      asic.hasConnectError = hasConnectError
      asic.hasConnectWarning = hasConnectWarning
      asic.openErrors = openErrors
      asic.openWarnings = openWarnings
    }
    state.dashboardAsics = dashboardAsics
  },

  closeAsicErrors(state, asic){
    // const hasConnectWarning = false;
    asic.hasConnectError = false;
    // Vue.set(asic, 'hasConnectWarning', false)
    asic.hasConnectWarning = false;
    asic.openErrors = [];
    asic.openWarnings = [];
    asic._rowVariant = '';
    state.asics.splice(state.asics.findIndex(elem => elem.id === asic.id), 1, asic)
  },
  stopUpdateAsic(state, asic){
    asic.stopUpdate = true;
  },
  resumeUpdateAsic(state, asic){
    asic.stopUpdate = false;
  },
  setAsicType(state, {asic, type}){
    asic.type = type;
    asic.asicName = type;
  },
  setAlgType(state, {asic, type}){
    asic.algType = type;
  },

  selectAsic(state, asicObj){
    const asic = state.asics.find(elem => elem.id == asicObj.id)
    state.selectedAsics.push(asic)
  },
  sortSelectedAsics(state){
    state.selectedAsics.sort(function (a, b) {
      if (a.ipAddress < b.ipAddress) {
        return -1
      }
      if (a.ipAddress > b.ipAddress) {
        return 1
      }
      return 0
    })
  },
  deselectAsic(state, asic){
    state.selectedAsics.splice(state.selectedAsics.findIndex(elem => elem.id == asic.id), 1)
  },
  setSelectedAsics(state, selectedAsics){
    state.selectedAsics = selectedAsics
    state.selectedAsics.sort(function (a, b) {
      if (a.ipAddress < b.ipAddress) {
        return -1
      }
      if (a.ipAddress > b.ipAddress) {
        return 1
      }
      return 0
    })
  },

  groupSetClient(state, clientName){
    for (const selected of state.selectedAsics) {
      selected.clientName = clientName
      // const asic = findAsic(state.asics, selected.id)
      // asic.clientName = clientName
    }
  },
  groupSetFarm(state, farmName){
    for (const selected of state.selectedAsics) {
      selected.farmName = farmName
      // const asic = findAsic(state.asics, selected.id)
      // asic.farmName = farmName
    }
  },
  setAutoupdateAll(state, update){
    for (const selected of state.selectedAsics) {
      selected.stopUpdate = !update
    }
  },

  setLoading(state, newValue){
    state.loading = newValue
  },
  setSearchFormField(state, {value, fieldName}){
    state.searchForm[fieldName] = value
  },
  setGroupEditFormField(state, {value, fieldName}){
    state.groupEditForm[fieldName] = value
  },

  setAddAsic(state, data){
    if (data) {
      state.asic = data
    }
    else {
      state.asic = {
        type: null,
        algType: null,
        client:null,
        farm:null,
        ipAddress:null
      }
    }
  },
}

export const actions = {
  init({dispatch}){
    dispatch('initSearchForm')
    dispatch('initGroupEditForm')
  },
  initSearchForm({commit}){
    const searchForm = {
      asicType: null,
      algType: null,
      farm: null,
      client: null,
      errorLevel: null,
      fieldName: null,
      ipAddress: ''
    };

    commit('setSearchForm', searchForm);
  },
  initGroupEditForm({commit}){
    const groupEditForm = {
      farm: null,
      client: null,
    };
    commit('setGroupEditForm', groupEditForm);
  },
  searchAsics({commit, state}){
    Asic.search(state.searchForm).then(response => commit('setAsics', response));
  },

  closeAsicErrors({commit, dispatch}, asic){
    Asic.closeErrors(asic.id).then(response => {
      if (response) {
        commit('closeAsicErrors', asic)
        dispatch('alerts/successAlert', 'Все ошибки по ASIC закрыты!', {root: true})
      }
      else {
        dispatch('alerts/dangerAlert', 'ASIC не найден!', {root: true})
      }
    })
  },
  stopUpdateAsic({commit, dispatch}, asic){
    Asic.stopUpdate(asic.id).then(response => {
      if (response) {
        commit('stopUpdateAsic', asic)
        dispatch('alerts/successAlert', 'Автообновление ASIC успешно отключено!', {root: true})
        // Положительное уведомление
      }
      else {
        dispatch('alerts/dangerAlert', 'ASIC не найден!', {root: true})
        // Отрицательное уведомление
      }
    })
  },
  resumeUpdateAsic({commit, dispatch}, asic){
    Asic.resumeUpdate(asic.id).then(response => {
      if (response) {
        commit('resumeUpdateAsic', asic)
        dispatch('alerts/successAlert', 'Автообновление ASIC успешно включено!', {root: true})
        // Положительное уведомление
      }
      else {
        dispatch('alerts/dangerAlert', 'ASIC не найден!', {root: true})
        // Отрицательное уведомление
      }
    })
  },
  updateAsic({commit, dispatch, state}, asic){
    dispatch('alerts/successAlert', 'ASIC начал обновление!', {root: true})
    Asic.updateAsic(asic.id).then(response => {
      if (response) {
        dispatch('alerts/successAlert', 'ASIC успешно обновлен!', {root: true})
        dispatch('searchAsics')
        // Положительное уведомление
      }
      else {
        dispatch('alerts/dangerAlert', 'Произошли проблемы во время обновления ASIC!', {root: true})
        // Отрицательное уведомление
      }
    })

  },
  rebootAsic({commit, dispatch}, asic){
    Asic.reboot(asic.id).then(response => {
      if (response) {
        dispatch('alerts/successAlert', 'ASIC успешно поставлен в очередь на перезагрузку!', {root: true})
        // Положительное уведомление
      }
      else {
        dispatch('alerts/dangerAlert', 'Произошли проблемы во время постановки ASIC в очередь на перезагрузку!', {root: true})
        // Отрицательное уведомление
      }
    });
  },
  setAsicType({commit, dispatch}, {asic, type}){
    Asic.setAsicType(asic.id, type).then(response => {
      if (response.ok) {
        dispatch('alerts/successAlert', 'Тип ASIC успешно изменен!', {root: true})
        commit('setAsicType', {asic, type: response.result})
      }
      else {
        dispatch('alerts/dangerAlert', 'Произошли проблемы во время изменения типа ASIC!', {root: true})
        // Отрицательное уведомление
      }
    });
  },
  setAlgType({commit, dispatch}, {asic, type}){
    Asic.setAlgType(asic.id, type).then(response => {
      if (response.ok) {
        dispatch('alerts/successAlert', 'Тип алгоритма ASIC успешно изменен!', {root: true})
        commit('setAlgType', {asic, type: response.result})
      }
      else {
        dispatch('alerts/dangerAlert', 'Произошли проблемы во время изменения типа алгоритма ASIC!', {root: true})
        // Отрицательное уведомление
      }
    });
  },

  fetchDashboardAsics({commit}, pageInfo){
    commit('setLoading', true)
    Asic.dashboard(pageInfo).then(response => {
      commit('setDashboardAsics', response)
      commit('setLoading', false)
    });
  },


  selectAsic({commit}, asic){
    commit('selectAsic', asic)
  },
  deselectAsic({commit}, asic){
    commit('deselectAsic', asic)
  },

  groupSetClient({commit, state, getters, dispatch}){
    Client.groupSetClient(state.selectedAsics, state.groupEditForm.client).then(response => {
      if (response) {
        dispatch('alerts/infoAlert', 'Клиент ' + getters.clientName + ' успешно назначен!', {root: true})
        commit('groupSetClient', getters.clientName)
      }
      else {
        dispatch('alerts/dangerAlert', 'Произошла ошибка при назначении клиента ' + getters.clientName + '!', {root: true})
      }
    })
  },
  groupSetFarm({commit, state, getters, dispatch}){
    Farm.groupSetFarm(state.selectedAsics, state.groupEditForm.farm).then(response => {
      if (response) {
        dispatch('alerts/infoAlert', 'Ферма ' + getters.farmName + ' успешно назначена!', {root: true})
        commit('groupSetFarm', getters.farmName)
        // dispatch('clearSelectedAsics')
      }
      else {
        dispatch('alerts/dangerAlert', 'Произошла ошибка при назначении фермы ' + getters.farmName + '!', {root: true})
      }
    })
  },
  enableAutoupdateAll({commit, state, getters, dispatch}){
    Asic.setAutoupdateAll(state.selectedAsics, true).then(response => {
      if (response) {
        dispatch('alerts/infoAlert', 'Автообновление на выделенных асиках успешно включено!', {root: true})
        commit('setAutoupdateAll', true)
      }
      else {
        dispatch('alerts/dangerAlert', 'Произошла ошибка при включении автообновления асиков!', {root: true})
      }
    })
  },
  disableAutoupdateAll({commit, state, getters, dispatch}){
    Asic.setAutoupdateAll(state.selectedAsics, false).then(response => {
      if (response) {
        dispatch('alerts/infoAlert', 'Автообновление на выделенных асиках успешно выключено!', {root: true})
        commit('setAutoupdateAll', false)
      }
      else {
        dispatch('alerts/dangerAlert', 'Произошла ошибка при выключении автообновления асиков!', {root: true})
      }
    })
  },
  setSelectedAsics({commit}, selectedAsics){
    commit('setSelectedAsics', selectedAsics)
  },
  clearSelectedAsics({commit}){
    commit('setSelectedAsics', [])
  },

  setModalAsic({commit}, modalAsic){
    commit('setModalAsic', modalAsic)
  },

  addAsic({commit, state, dispatch}){
    Asic.add(state.asic).then(response => {
      if (response) {
        dispatch('alerts/successAlert', 'ASIC успешно добавлен!', {root: true})
        dispatch('searchAsics')
      }
      else {
        dispatch('alerts/dangerAlert', 'К сожалению, произошла ошибка при добавлении ASIC.', {root: true})
      }
    })
  },
  initAddAsic({commit}){
    commit('setAddAsic')
  }
}

export const getters = {
  clientName(state, getters, rootState){
    const client = rootState.utils.clients.find(elem => elem.value == state.groupEditForm.client);
    return client ? client.text : ''
  },
  farmName(state, getters, rootState){
    const farm = rootState.utils.farms.find(elem => elem.value == state.groupEditForm.farm)
    return farm ? farm.text : ''
  },
  getField
}

export default{
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
