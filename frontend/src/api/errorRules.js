/**
 * Created by mrakolice on 04.10.18.
 */


import {HTTP} from './common'

export const ErrorRules = {
  all(asicType){
    return HTTP.post('', {
      query: `
        query ErrorRules($asicType:Int){
          errorRules(asicType:$asicType){
            id
            asicType
            errorLevel
            errorLevelValue
            fieldName
            valueType
            comparisonType
            value
            percent
            message
            shortString
            errorRule{
              id
              asicType
              errorLevel
              fieldName
              valueType
              comparisonType
              value
              percent
              message
              shortString
            }
          }
        }`,
      variables: {
        asicType
      }
    }).then(response => response.data.data.errorRules)
  },
  getById(id){
    return HTTP.post('', {
      query: `
        query GetErrorRule($id:Int){
          errorRule(id:$id){
            id
            asicType
            errorLevel
            fieldName
            valueType
            comparisonType
            value
            percent
            message
            errorRule
          }
        }`,
      variables: {
        id
      }
    }).then(response => response.data.data.errorRule)
  },

  errorRulesShort(){
    return HTTP.post('', {
      query: `
        {
          errorRulesShort{
            value
            text
          }
        }`
    }).then(response => {
      return response.data.data.errorRulesShort || []
    })
  },
  errorLevels(){
    return HTTP.post('', {
      query: `
        {
          errorRuleErrorLevels{
            value
            text
          }
        }`
    }).then(response => {
      return response.data.data.errorRuleErrorLevels || []
    })
  },
  fieldNames(){
    return HTTP.post('', {
      query: `
        {
          errorRuleFieldNames{
            value
            text
          }
        }`
    }).then(response => {
      return response.data.data.errorRuleFieldNames || []
    })
  },
  asicTypes(){
    return HTTP.post('', {
      query: `
        {
          errorRuleAsicTypes{
            value
            text
          }
        }`
    }).then(response => {
      return response.data.data.errorRuleAsicTypes || []
    })
  },
  valueTypes(){
    return HTTP.post('', {
      query: `
        {
          valueTypes{
            value
            text
          }
        }`
    }).then(response => {
      return response.data.data.valueTypes || []
    })
  },
  comparisonTypes(){
    return HTTP.post('', {
      query: `
        {
          comparisonTypes{
            value
            text
          }
        }`
    }).then(response => {
      return response.data.data.comparisonTypes || []
    })
  },
  add(errorRule){
    return HTTP.post('', {
      query: `
       mutation AddErrorRule($asicType:Int, $errorLevel:Int, $fieldName:String,
          $errorRule:Int, $valueType:Int, $comparisonType:Int, $value:String, $percent:Int, $message:String)
          {
            addErrorRule(asicType:$asicType, errorLevel:$errorLevel, fieldName:$fieldName, 
              errorRule:$errorRule,valueType:$valueType, comparisonType:$comparisonType, value:$value,
              percent:$percent, message:$message)
            {
              ok
            }
        }`,
      variables: errorRule
    }).then(response => response.data.data.addErrorRule.ok)
  },
  update(errorRule){
    return HTTP.post('', {
      query: `
       mutation UpdateErrorRule($id:Int, $asicType:Int, $errorLevel:Int, $fieldName:String,
          $errorRule:Int, $valueType:Int, $comparisonType:Int, $value:String, $percent:Int, $message:String)
          {
            updateErrorRule(id:$id, asicType:$asicType, errorLevel:$errorLevel, fieldName:$fieldName, 
              errorRule:$errorRule,valueType:$valueType, comparisonType:$comparisonType, value:$value,
              percent:$percent, message:$message)
            {
              ok
            }
        }`,
      variables: errorRule
    }).then(response => response.data.data.updateErrorRule.ok)
  },
  delete(errorRule){
    return HTTP.post('', {
      query: `
       mutation UpdateErrorRule($id:Int)
          {
            deleteErrorRule(errorRuleId:$id)
            {
              ok
            }
        }`,
      variables: errorRule
    }).then(response => response.data.data.deleteErrorRule.ok)
  }
};
