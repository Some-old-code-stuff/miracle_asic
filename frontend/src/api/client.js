/**
 * Created by mrakolice on 11.09.18.
 */

import {HTTP} from './common'


export const Client = {
  all(){
    return HTTP.post('', {
      query: `
        {
          clients{
            id
            name
          }
        }`
    })
  },
  groupSetClient(selectedAsics, clientId){
    const asicIds = selectedAsics.map(elem=>elem.id)

    return HTTP.post('', {
      query: `
        mutation GroupSetClient($asicIds:[Int], $clientId:Int){
          groupSetClient(asicIds:$asicIds, clientId:$clientId){
            ok
          }
        }`,
      variables:{
        asicIds,
        clientId
      }
    }).then(response => response.data.data.groupSetClient)
  }
};
