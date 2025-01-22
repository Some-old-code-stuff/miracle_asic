/**
 * Created by mrakolice on 12.09.18.
 */


import {HTTP} from './common'

export const ChainInfo = {
  asicChains(asicId){
    return HTTP.post('', {
      query: `
       query AsicChains($asicId: Int) {
          asicChains(asicId: $asicId) {
            asicId
            chains {
              id
              temperature
              frequency
              rate
              measure
              allChips
              wrongChips
              workingChips
            }
          }
       }`,
      variables: {
        asicId: asicId
      }
    }).then(response => {
      return response.data.data.asicChains
    })
  },
};
