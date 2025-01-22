/**
 * Created by mrakolice on 14.09.18.
 */

import {HTTP} from './common'

export const FanInfo = {
  asicFans(asicId){
    return HTTP.post('', {
      query: `
       query AsicFans($asicId: Int) {
          asicFans(asicId: $asicId) {
            asicId
            fans {
              id
              name
              speed
            }
          }
       }`,
      variables: {
        asicId: asicId
      }
    }).then(response=>response.data.data.asicFans)
  },
};
