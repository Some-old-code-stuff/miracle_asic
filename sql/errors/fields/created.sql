CREATE or replace FUNCTION common_error_created(u common_error)
  RETURNS VARCHAR AS $$
  SELECT to_char(u.created, 'DD.MM.YYYY HH24:MI:SS')
$$ LANGUAGE SQL STABLE;

comment on function common_error_created(common_error) is
  E'@fieldName created';
comment on column common_error.created is E'@name created_value';