CREATE FUNCTION common_error_status(u common_error)
  RETURNS VARCHAR AS $$
SELECT convert_error_status(u.status)
$$ LANGUAGE SQL STABLE;

comment on function common_error_status(common_error) is
  E'@fieldName status';
comment on column common_error.status is E'@name status_value';