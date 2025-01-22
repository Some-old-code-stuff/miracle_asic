/**
 * Created by mrakolice on 25.09.18.
 */


import {HTTP} from './common'

export const Auth = {
  tokenAuth(phone, sms_token){
    return HTTP.post('', {
        query: `
        mutation TokenAuth($username:String!, $password:String!) {
        	tokenAuth(username:$username, password:$password){
            token
          }
        }`,
        variables: {
          username: phone,
          password: sms_token
        }
      }
    ).then(response => response.data.data.tokenAuth)
  },
  verifyToken(token){
    return HTTP.post('', {
        query: `
        mutation VerifyToken($token:String!) {
        	verifyToken(token:$token){
            payload
          }
        }`,
        variables: {
          token: token
        }
      }
    ).then(response => response.data.data.verifyToken)
  },
  refreshToken(token){
    return HTTP.post('', {
        query: `
        mutation RefreshToken($token:String!) {
        	refreshToken(token:$token){
            payload
            token
          }
        }`,
        variables: {
          token: token
        }
      }
    ).then(response => response.data.data.refreshToken)
  },
  sendSmsToken(phone){
    return HTTP.post('', {
        query: `
        mutation SendSmsToken($phone:String) {
        	sendSmsToken(phone:$phone){
        	  ok
        	  token
          }
        }`,
        variables: {
          phone: phone
        }
      }
    ).then(response => response.data.data.sendSmsToken)
  },
  checkSmsToken(phone, token){
    return HTTP.post('', {
        query: `
        mutation CheckSmsToken($phone:String, $token:String) {
        	checkSmsToken(phone:$phone, token:$token){
        	  ok
        	  tryCount
          }
        }`,
        variables: {
          phone: phone,
          token: token
        }
      }
    ).then(response => response.data.data.checkSmsToken)
  },

};
