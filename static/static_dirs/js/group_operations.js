/**
 * Created by mrakolice on 28.08.18.
 */

$(document).ready(() => {
    $('#check_all').click(function () {
        if (this.checked) {
            $('input.asic_id').prop('checked', true)
        } else {
            $('input.asic_id').prop('checked', false)
        }
        ids = $('.asic_id:checked').map(function(){
            return this.name
        }).get();
        $('#id_asic_ids').val(ids.join(','))
    });

    $('#asic_table .asic_id').change(function(){
        ids = $('.asic_id:checked').map(function(){
            return this.name
        }).get();
        $('#id_asic_ids').val(ids.join(','))
    });
})