/**
 * Created by mrakolice on 17.09.18.
 */

export default {
  methods: {
    closeErrors: function (asic) {
      this.$store.dispatch('asics/closeAsicErrors', asic)
    },
    update: function (asic) {
      this.$store.dispatch('asics/updateAsic', asic)
    },
    reboot: function (asic) {
      this.$store.dispatch('asics/rebootAsic', asic)
    },
    stopUpdate: function (asic) {
      this.$store.dispatch('asics/stopUpdateAsic', asic)
    },
    resumeUpdate: function (asic) {
      this.$store.dispatch('asics/resumeUpdateAsic', asic)
    },
  }
}
