/**
 * Created by mrakolice on 11.09.18.
 */

import {HTTP, newHTTP} from './common'

export const Error = {
  all(){
    return HTTP.post('', {
      query: `
        query AllErrors($closed:Boolean) {
          errors(closed:$closed) {
            id
            message
            asic{
              name
              ipAddress
            }
            level
            status
            created
          }
        }`,
      variables: {
        closed: true
      }
    })
  },
  openErrors(asicId){
    return HTTP.post('', {
      query: `
        query OpenErrors($asicId:Int) {
          openErrors(asicId:$asicId) {
            id
            message
            asic{
              name
              ipAddress
            }
            level
            status
            created
          }
        }`,
      variables: {
        asicId: asicId
      }
    })
  },
  openWarnings(asicId){
    return HTTP.post('', {
      query: `
        query OpenWarnings($asicId:Int) {
          openWarnings(asicId:$asicId) {
            id
            message
            asic{
              name
              ipAddress
            }
            level
            status
            created
          }
        }`,
      variables: {
        asicId: asicId
      }
    })
  },
  asicErrors(asicId, fieldName, objectId){
    return newHTTP.post('', {
      query: `
        query AsicErrors($asicId:Int, $fieldName:String, $objectId:Int) {
          asicErrorsList(asicId:$asicId, fieldName:$fieldName, objectId:$objectId){
              id
              message
              level
              levelValue
              status
              statusValue
              objectId
              created
          }
        }`,
      variables: {
        asicId: asicId,
        fieldName: fieldName,
        objectId:objectId
      }
    }).then(response=>response.data.data.asicErrorsList)
  },
  toPending(errorId){
    return newHTTP.post('', {
      query: `
        mutation ToPending($errorId:Int!, $status: Int!) {
          changeErrorStatus(input:{errorId:$errorId, status:$status}){            
            errorStatusResult{
              status
              statusValue
            }
          }
        }`,
      variables:{
        errorId:errorId,
        status: 2
      }
    }).then(response =>{
      return response.data.data.changeErrorStatus.errorStatusResult
    })
  },
  closeError(errorId){
    return newHTTP.post('', {
      query: `
        mutation CloseError($errorId:Int!, $status: Int!) {
          changeErrorStatus(input:{errorId:$errorId, status:$status}){            
            errorStatusResult{
              status
              statusValue
            }
          }
        }`,
      variables:{
        errorId:errorId,
        status: 4
      }
    }).then(response =>{
      return response.data.data.changeErrorStatus.errorStatusResult
    })
  },
  toError(errorId){
    return newHTTP.post('', {
      query: `
        mutation ToError($errorId:Int!, $level: Int!) {
          changeErrorLevel(input:{errorId:$errorId, level: $level}){
            errorLevelResult{
              asicId
            }
          }
        }`,
      variables:{
        errorId:errorId,
        level:2
      }
    }).then(response =>{
      return response.data.data.changeErrorLevel.errorLevelResult
    })
  },
  toWarning(errorId){
    return newHTTP.post('', {
      query: `
        mutation ToWarning($errorId:Int!, $level: Int!) {
          changeErrorLevel(input:{errorId:$errorId, level: $level}){
            errorLevelResult{
              asicId
            }
          }
        }`,
      variables:{
        errorId:errorId,
        level:1
      }
    }).then(response =>{
      return response.data.data.changeErrorLevel.errorLevelResult
    })
  }
};
