/**
 * Created by mrakolice on 04.10.18.
 */

import {ErrorRules} from '../../api/errorRules'
import {getField, updateField} from 'vuex-map-fields'

export const state = {
  errorRules: [],
  errorRule: {},

  errorLevels: [],
  asicTypes: [],
  algTypes: [],
  valueTypes: [],
  comparisonTypes: [],
  errorRulesShort: [],
}

export const mutations = {
  updateField,
  setErrorRules(state, data){
    state.errorRules = data
  },
  setErrorRule(state, data){
    if (data){
      state.errorRule = data
    }
    else{
      state.errorRule = {
          asicType: 0,
          errorLevel: 1,
          fieldName: 'full_rate',
          valueType: 0,
          comparisonType: 0,
          errorRule: null
        }
    }


  },
  setValueTypes(state, data) {
    state.valueTypes = data;
  },
  setComparisonTypes(state, data) {
    state.comparisonTypes = data;
  },
  setErrorRulesShort(state, data) {
    state.errorRulesShort = data;
  },
  setErrorLevels(state, errorLevels) {
    state.errorLevels = errorLevels;
  },
  setFieldNames(state, fieldNames) {
    state.fieldNames = fieldNames;
  },
  setAsicTypes(state, asicTypes) {
    state.asicTypes = asicTypes;
  },
  deleteErrorRule(state, errorRule){
    state.errorRules.splice(state.errorRules.findIndex(el => el.id == errorRule.id), 1)
  }
}
export const actions = {
  init({dispatch}){
    dispatch('fetchErrorLevels')
    dispatch('fetchFieldNames')
    dispatch('fetchAsicTypes')
    dispatch('fetchValueTypes')
    dispatch('fetchComparisonTypes')
    dispatch('fetchErrorRulesShort')
  },
  fetchErrorRules({commit}, asicType){
    ErrorRules.all(asicType).then(response => {
      commit('setErrorRules', response)
    })
  },
  fetchErrorRule({commit}, errorRuleId){
    ErrorRules.getById(errorRuleId).then(response => {
      commit('setErrorRule', response)
    })
  },
  fetchErrorLevels({commit}){
    ErrorRules.errorLevels().then(response => {
      commit('setErrorLevels', response);
    });
  },
  fetchFieldNames({commit}){
    ErrorRules.fieldNames().then(response => {
      commit('setFieldNames', response);
    });
  },
  fetchAsicTypes({commit}){
    ErrorRules.asicTypes().then(response => {
      commit('setAsicTypes', response);
    });
  },

  fetchValueTypes({commit}){
    ErrorRules.valueTypes().then(response => {
      commit('setValueTypes', response);
    });
  },
  fetchComparisonTypes({commit}){
    ErrorRules.comparisonTypes().then(response => {
      commit('setComparisonTypes', response);
    });
  },
  fetchErrorRulesShort({commit}){
    ErrorRules.errorRulesShort().then(response => {
      commit('setErrorRulesShort', response);
    });
  },
  addOrUpdateErrorRule({dispatch, state}){
    if (state.errorRule.id){
      dispatch('updateErrorRule')
    }
    else{
      dispatch('addErrorRule')
    }
  },
  updateErrorRule({dispatch, state}){
    ErrorRules.update(state.errorRule).then(response => {
      if (response) {
        dispatch('alerts/successAlert', 'Валидационное правило успешно обновлено!', {root: true})
        dispatch('fetchErrorRules')
      }
      else {
        dispatch('alerts/dangerAlert', 'К сожалению, произошла ошибка при обновлении валидационного правила.', {root: true})
      }
    })
  },
  addErrorRule({dispatch, state}){
    ErrorRules.add(state.errorRule).then(response => {
      if (response) {
        dispatch('alerts/successAlert', 'Валидационное правило успешно добавлено!', {root: true})
        dispatch('fetchErrorRules')
      }
      else {
        dispatch('alerts/dangerAlert', 'К сожалению, произошла ошибка при добавлении валидационного правила.', {root: true})
      }
    })
  },
  deleteErrorRule({dispatch, commit}, errorRule){
    ErrorRules.delete(errorRule).then(response => {
      if (response) {
        dispatch('alerts/successAlert', 'Валидационное правило успешно удалено!', {root: true})
        commit('deleteErrorRule', errorRule)
      }
      else {
        dispatch('alerts/dangerAlert', 'К сожалению, произошла ошибка при удалении валидационного правила.', {root: true})
      }
    })
  }
}

export const getters = {
  getField
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
