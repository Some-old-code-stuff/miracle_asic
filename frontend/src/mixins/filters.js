/**
 * Created by mrakolice on 14.09.18.
 */

export default {
  filters: {
    truncate: function (str, length) {
      if (!str) {
        return ''
      }
      return str.substring(0, length) + '...'
    }
  },
}
