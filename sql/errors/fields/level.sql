CREATE or replace FUNCTION common_error_level(u common_error)
  RETURNS VARCHAR AS $$
SELECT convert_error_level(u.level)
$$ LANGUAGE SQL STABLE;

comment on function common_error_level(common_error) is
  E'@fieldName level';
comment on column common_error.level is E'@name level_value';