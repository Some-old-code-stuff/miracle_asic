
create or replace function change_error_status(error_id int, status int)
  returns error_status_result as $$
    update common_error set status=$2 where id=error_id
returning convert_error_status(status), status
  $$ LANGUAGE sql VOLATILE;