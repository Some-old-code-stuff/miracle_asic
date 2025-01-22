/**
 * Created by mrakolice on 12.09.18.
 */


import {HTTP, PAGE_COUNT, newHTTP} from './common'

export const Asic = {
  dashboard(pageInfo){
    return newHTTP.post('', {
      query: `
        query DashboardAsics {
          dashboardAsicsList {
            id
            type
            algType
            name
            ipAddress
            hostName
            defaultRate
            asicName
            poolStatus
            fullRate
            poolAddress
            poolUsername
            updated
            stopUpdate
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
            fans {
              id
              name
              speed
            }
            errorsList {
              id
              asicId
              level
              status
              fieldName
              objectId
              errorRuleId
              warningRuleId
              message
              levelValue
            }
          }
        }`,
      variables: {}
    }).then(response => {
      return response.data.data.dashboardAsicsList
    })
  },
  search(searchForm){
    let variables = {};
    Object.assign(variables, searchForm)
    variables.asicType = parseInt(variables.asicType)
    variables.algType = parseInt(variables.algType)
    variables.farm = parseInt(variables.farm)
    variables.client = parseInt(variables.client)
    variables.errorLevel = parseInt(variables.errorLevel)

    return newHTTP.post('', {
      query: `
        query SearchAsics(
          $asicType:Int, $algType:Int, $farm:Int, $client:Int, 
          $asicName:String, $ipAddress:String, $poolStatus:String, 
          $farmName:String, $clientName:String,
        	$errorLevel:Int, $fieldName:String,
        	$withDisabledAutoupdate: Boolean,
        	$withConnectionErrors: Boolean,
        	$withErrors: Boolean,
        	$withWarnings: Boolean,
        	$unregisteredAsics: Boolean,
        ){
          searchAsicsList(
            argAsicType:$asicType 
            argAlgType:$algType
            argFarm:$farm
            argClient:$client 
          	argAsicName:$asicName
            argIpAddress:$ipAddress
            argPoolStatus:$poolStatus
          	argFarmName:$farmName
            argClientName:$clientName
        		argErrorLevel:$errorLevel
            argFieldName:$fieldName  
            argWithDisabledAutoUpdate:$withDisabledAutoupdate  
            argWithConnectionErrors:$withConnectionErrors  
            argWithErrors:$withErrors  
            argWithWarnings:$withWarnings  
            argUnregisteredAsics:$unregisteredAsics  
          ){
            id
            asicName
            algType
            ipAddress
            poolStatus
            type
            fullRate
            defaultRate
            poolUsername
            poolAddress
            measure
            updated
            stopUpdate
            clientName
            farmName
            chains {
              id
              temperature
              frequency
              rate
              measure
              wrongChips
              workingChips
              allChips
            }
            fans {
              id
              name
              speed
            }
            errorsList {
              id
              asicId
              level
              status
              fieldName
              objectId
              errorRuleId
              warningRuleId
              message
              levelValue
            }
          }
        }`,
      variables: variables
    }).then(response => response.data.data.searchAsicsList)
  },
  searchNew(searchForm){
    return HTTP.post('', {
      query: `
        query SearchAsics(
          $asicType:Int, $algType:Int, $farm:Int, $client:Int, 
          $asicName:String, $ipAddress:String, $poolStatus:String, 
          $farmName:String, $clientName:String,
        	$errorLevel:Int, $fieldName:String,
        	$first:Int, $after:String
        ){
          searchAsics(
            asicType:$asicType 
            algType:$algType
            farm:$farm
            client:$client 
          	asicName:$asicName
            ipAddress:$ipAddress
            poolStatus:$poolStatus
          	farmName:$farmName
            clientName:$clientName
        		errorLevel:$errorLevel
            fieldName:$fieldName,
            first:$first,
            after:$after
          ){            
            pageInfo {
              hasNextPage
              hasPreviousPage
              startCursor
              endCursor      
            }
            edges {
              cursor
              node {
                id
                type
                algType
                name
                ipAddress
                hostName
                defaultRate
                asicName
                poolStatus
                fullRate
                poolAddress
                poolUsername
                updated
                stopUpdate
                clientName
                farmName
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
                fans {
                  id
                  name
                  speed
                }        
                errors {
                  id
                  asicId
                  level
                  status
                  fieldName
                  objectId
                  errorRuleId
                  warningRuleId
                  message
                  levelValue
                }       
              }
            }
          }
        }`,
      variables: searchForm
    })
  },
  closeErrors(asic_id){
    return newHTTP.post('', {
      query: `
        mutation CloseAsicErrors(
          $id:Int!
        ){
          closeAsicErrors(input:{asicId:$id}){
            boolean
          }
        }`,
      variables: {
        id: asic_id
      }
    }).then(response => response.data.data.closeAsicErrors.boolean)
  },
  stopUpdate(asic_id){
    return newHTTP.post('', {
      query: `
        mutation StopUpdateAsic(
          $id:Int!
        ){
          stopUpdateAsic(input:{asicId:$id}){
            boolean
          }
        }`,
      variables: {
        id: asic_id
      }
    }).then(response => response.data.data.stopUpdateAsic.boolean)
  },
  resumeUpdate(asic_id){
    return newHTTP.post('', {
      query: `
        mutation ResumeUpdateAsic(
          $id:Int!
        ){
          resumeUpdateAsic(input:{asicId:$id}){
            boolean
          }
        }`,
      variables: {
        id: asic_id
      }
    }).then(response => response.data.data.resumeUpdateAsic.boolean)
  },

  setAutoupdateAll(selectedAsics, update){
    const asicIds = selectedAsics.map(elem => elem.id)

    return newHTTP.post('', {
      query: `
        mutation SetAutoupdateAll($asicIds:[Int], $update:Boolean){
          asicGroupSetAutoUpdate(input:{asicIds:$asicIds, update:$update}){
            ok
          }
        }`,
      variables: {
        asicIds,
        update
      }
    }).then(response => response.data.data.asicGroupSetAutoUpdate.boolean)
  },

  updateAsic(asic_id){
    return HTTP.post('', {
      query: `
        mutation UpdateAsic(
          $id:Int!
        ){
          updateAsic(asicId:$id){
            ok
          }
        }`,
      variables: {
        id: asic_id
      }
    }).then(response => response.data.data.updateAsic.ok)
  },
  reboot(asic_id){
    return HTTP.post('', {
      query: `
        mutation RebootAsic(
          $id:Int!
        ){
          rebootAsic(asicId:$id){
            ok
          }
        }`,
      variables: {
        id: asic_id
      }
    }).then(response => response.data.data.rebootAsic.ok)
  },
  setAsicType(asicId, type){
    return newHTTP.post('', {
      query: `
        mutation SetAsicType(
          $id:Int!,
          $type:Int
        ){
          setAsicType(input:{asicId:$id, type:$type}){
            boolean
          }
        }`,
      variables: {
        id: asicId,
        type: type,
      }
    }).then(response => response.data.data.setAsicType.boolean)
  },
  setAlgType(asicId, type){
    return newHTTP.post('', {
      query: `
        mutation SetAlgType(
          $id:Int!,
          $type:Int
        ){
          setAlgType(input:{asicId:$id, type:$type}){
            boolean
          }
        }`,
      variables: {
        id: asicId,
        type: type,
      }
    }).then(response => response.data.data.setAlgType.boolean)
  },
  settings(asic_id){
    return HTTP.post('', {
      query: `
        query AsicSettings(
          $id:Int
        ){
          asicSettings(asicId:$id){
            username
            password
          }
        }`,
      variables: {
        id: asic_id
      }
    }).then(response => response.data.data.asicSettings)
  },
  changePassword(asic_id, password){
    return HTTP.post('', {
      query: `
        mutation SetPassword(
          $id:Int, $password:String
        ){
          asicSetPassword(asicId:$id, password:$password){
            ok
          }
        }`,
      variables: {
        id: asic_id,
        password: password
      }
    }).then(response => response.data.data.asicSetPassword.ok)
  },
  add(asic){
    return newHTTP.post('', {
      query: `
       mutation AddAsic($type:Int, $ipAddress:String, $algType:Int,
          $client:Int, $farm:Int)
          {
            addAsic(input:{type:$type, ipAddress:$ipAddress, algType:$algType, 
              client:$client,farm:$farm})
            {
              commonAsic{
                id
              }
            }
        }`,
      variables: asic
    }).then(response => response.data.data.addAsic.commonAsic != undefined)
  },
};
