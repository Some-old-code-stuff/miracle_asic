/**
 * Created by mrakolice on 11.09.18.
 */

import {HTTP} from './common'

export const Utils = {
  errorLevels(){
    return HTTP.post('', {
      query: `
        {
          errorLevels{
            value
            text
          }
        }`
    }).then(response => {
      return response.data.data.errorLevels || []
    })
  },
  fieldNames(){
    return HTTP.post('', {
      query: `
        {
          fieldNames{
            value
            text
          }
        }`
    }).then(response => {
      return response.data.data.fieldNames || []
    })
  },
  asicTypes(){
    return HTTP.post('', {
      query: `
        {
          asicTypes{
            value
            text
          }
        }`
    }).then(response => {
      return response.data.data.asicTypes || []
    })
  },
  algTypes(){
    return HTTP.post('', {
      query: `
        {
          algTypes{
            value
            text
          }
        }`
    }).then(response => {
      return response.data.data.algTypes || []
    })
  },

  clients(){
    return HTTP.post('', {
      query: `
        {
          clients{
            value
            text
          }
        }`
    }).then(response => {
      return response.data.data.clients || []
    })
  },
  farms(){
    return HTTP.post('', {
      query: `
        {
          farms{
            value
            text
          }
        }`
    }).then(response => {
      return response.data.data.farms || []
    })
  },
  menuInfo(){
    return HTTP.post('', {
      query: `
        {
          menuInfo{
            asicCount
            errorAsicCount
            errorCount
            warningCount
            flowerUrl
            adminUrl
          }
        }`
    }).then(response => {return response.data.data.menuInfo || {}})
  }
};
