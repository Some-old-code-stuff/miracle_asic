/**
 * Created by mrakolice on 26.09.18.
 */

import {Utils} from '../../api/utils'


export const state = {
  errorLevels: [],
  asicTypes: [],
  algTypes: [],
  farms: [],
  clients: [],
  fieldNames: [],
  menuInfo: {},
}


export const mutations = {
  setErrorLevels(state, errorLevels) {
    state.errorLevels = errorLevels;
  },
  setFieldNames(state, fieldNames) {
    state.fieldNames = fieldNames;
  },
  setAsicTypes(state, asicTypes) {
    state.asicTypes = asicTypes;
  },
  setAlgTypes(state, algTypes) {
    state.algTypes = algTypes;
  },
  setFarms(state, farms) {
    state.farms = farms;
  },
  setClients(state, clients) {
    state.clients = clients;
  },
  setMenuInfo(state, menuInfo){
    state.menuInfo = menuInfo
  },
}

export const actions = {
  init({dispatch}){
    dispatch('fetchErrorLevels')
    dispatch('fetchFieldNames')
    dispatch('fetchAsicTypes')
    dispatch('fetchAsicTypes')
    dispatch('fetchAlgTypes')
    dispatch('fetchFarms')
    dispatch('fetchClients')
    dispatch('fetchMenuInfo')
  },
  fetchErrorLevels({commit}){
    Utils.errorLevels().then(response => {
      commit('setErrorLevels', response);
    });
  },
  fetchFieldNames({commit}){
    Utils.fieldNames().then(response => {
      commit('setFieldNames', response);
    });
  },
  fetchAsicTypes({commit}){
    Utils.asicTypes().then(response => {
      commit('setAsicTypes', response);
    });
  },
  fetchAlgTypes({commit}){
    Utils.algTypes().then(response => {
      commit('setAlgTypes', response);
    });
  },
  fetchFarms({commit}){
    Utils.farms().then(response => {
      commit('setFarms', response);
    });
  },
  fetchClients({commit}){
    Utils.clients().then(response => {
      commit('setClients', response);
    });
  },
  fetchMenuInfo({commit}){
    Utils.menuInfo().then(response => {
      commit('setMenuInfo', response)
    })
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
