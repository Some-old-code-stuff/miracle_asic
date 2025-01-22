
create or replace function change_error_level(error_id int, level int)
  returns error_level_result as $$
    update common_error set level=$2 where id=error_id
returning convert_error_level(level), level, common_error.asic_id
  $$ LANGUAGE sql VOLATILE;