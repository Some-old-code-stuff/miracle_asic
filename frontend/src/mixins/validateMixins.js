/**
 * Created by mrakolice on 14.09.18.
 */

export const FieldName = {
  ASIC_NAME: 'asic_name',
  HOST_NAME: 'host_name',
  POOL_STATUS: 'pool_status',
  FULL_RATE: 'full_rate',

  CHAIN_INFO_TEMPERATURE: 'chain_info_set__temperature',
  CHAIN_INFO_FREQUENCY: 'chain_info_set__frequency',
  CHAIN_INFO_RATE: 'chain_info_set__rate',
  CHAIN_INFO_ALL_CHIPS: 'chain_info_set__all_chips',
  CHAIN_INFO_WRONG_CHIPS: 'chain_info_set__wrong_chips',
  CHAIN_INFO_WORKING_CHIPS: 'chain_info_set__working_chips',

  FAN_INFO_NAME: 'fan_info_set__name',
  FAN_INFO_SPEED: 'fan_info_set__speed',

  ERROR_RULE_COUNT: 'error_rule_count'
}

export default {
  data(){
    return {
      FieldName: FieldName
    }
  },
  methods: {
    haveErrors: function (className, errorData, fieldName, objectId) {
      if (errorData == null) {
        return className + 'success'
      }

      function findError(elem) {
        return elem.fieldName == fieldName && elem.objectId == objectId
      }

      if (errorData.openErrors != null && errorData.openErrors.find(findError)) {
        return className + 'danger'
      }
      if (errorData.openWarnings != null && errorData.openWarnings.find(findError)) {
        return className + 'warning'
      }
      return className + 'success'
    },
    haveErrorsWithWarnings: function (className, errorData, fieldName, objectId) {
      if (errorData == null || errorData.openErrors == null || errorData.openWarnings == null) {
        return className + 'success'
      }
      function findError(elem) {
        return elem.fieldName == fieldName && elem.objectId == objectId
      }

      const warnings = errorData.openWarnings.filter(findError)
      if (warnings.length == 0) {
        return className + 'success'
      }
      const warning = warnings.find(function (elem) {
        return elem.errorRuleId != null
      })
      if (warning == null) {
        return className + 'warning'
      }
      const error = errorData.openErrors.find(function (elem) {
        return elem.fieldName == FieldName.ERROR_RULE_COUNT && elem.warningRuleId == warning.errorRuleId
      });
      return error != null ? className + 'danger' : className + 'warning'
    },
    have_connect_error: function (asic) {
      if (asic.hasConnectError) {
        return 'red-icon'
      }
      if (asic.hasConnectWarning) {
        return 'yellow-icon'
      }
      return ''
    },
    have_connect_error_title: function (asic) {
      if (asic.hasConnectError) {
        return 'ASIC недоступен!'
      }
      if (asic.hasConnectWarning) {
        return 'ASIC был недоступен какое-то время назад!'
      }
      return 'ASIC доступен'
    },
  }
};
