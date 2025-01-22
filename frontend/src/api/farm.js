/**
 * Created by mrakolice on 11.09.18.
 */


import {HTTP} from './common'

export const Farm = {
  all(){
    return HTTP.post('', {
      query: `
        {
          farms{
            id
            name
          }
        }`
    })
  },
  groupSetFarm(selectedAsics, farmId){
    const asicIds = selectedAsics.map(elem=>elem.id)

    return HTTP.post('', {
      query: `
        mutation GroupSetFarm($asicIds:[Int], $farmId:Int){
          groupSetFarm(asicIds:$asicIds, farmId:$farmId){
            ok
          }
        }`,
      variables:{
        asicIds,
        farmId
      }
    }).then(response => response.data.data.groupSetFarm)
  }
};
