/**
 * Created by mrakolice on 27.09.18.
 */


import {HTTP} from './common'

export const Balance = {
  addCounterRecord(date){
    return HTTP.post('', {
      query: `
        mutation AddCounterRecord(
          $date:Date
        ){
          addCounterRecord(date:$date){
            ok
            id
          }
        }`,
      variables: {
        date
      }
    }).then(response => response.data.data.addCounterRecord)
  },
  addCounter(counter, balanceId){
    counter.recordId = balanceId
    return HTTP.post('', {
      query: `
        mutation AddCounter($recordId:Int!, $name:String, $value:Float, $koefficient:Float, $approvedTariff:Float, $preliminaryTariff:Float){
          addCounter(
            recordId: $recordId,
            name:$name, 
            value: $value,
            koefficient:$koefficient, 
            approvedTariff:$approvedTariff, 
            preliminaryTariff:$preliminaryTariff,
          ){
            ok
            id
          }
        }`,
      variables: counter
    }).then(response => response.data.data.addCounter)
  },
  updateCounter(counter){
    return HTTP.post('', {
      query: `
        mutation UpdateCounter($id:Int, $name:String, $value:Float, $koefficient:Float, $approvedTariff:Float, $preliminaryTariff:Float){
          updateCounter(
            id:$id,
            name:$name, 
            value: $value,
            koefficient:$koefficient, 
            approvedTariff:$approvedTariff, 
            preliminaryTariff:$preliminaryTariff,
          ){
            ok
          }
        }`,
      variables: counter
    }).then(response => response.data.data.updateCounter.ok)
  },
  getBalance(){
    return HTTP.post('', {
      query: `
        query GetBalance{
          getBalance{
            id
            date
            counters{
              id
              name
              value
              preliminaryTariff
              approvedTariff
              testTariff
              koefficient      
            }
          }
        }`,
    }).then(response => response.data.data.getBalance)
  },
  deleteCounterRecord(recordId){
    return HTTP.post('', {
      query: `
        mutation DeleteCounterRecord(
          $recordId:Int!
        ){
          deleteCounterRecord(recordId:$recordId){
            ok
          }
        }`,
      variables: {
        recordId
      }
    }).then(response => response.data.data.deleteCounterRecord.ok)
  },
  deleteCounter(counterId){
    return HTTP.post('', {
      query: `
        mutation DeleteCounter(
          $counterId:Int!
        ){
          deleteCounter(counterId:$counterId){
            ok
          }
        }`,
      variables: {
        counterId
      }
    }).then(response => response.data.data.deleteCounter.ok)
  },
}
