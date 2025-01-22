CREATE or replace FUNCTION common_chaininfo_rate(u common_chaininfo)
  RETURNS VARCHAR AS $$
  SELECT round(u.rate::NUMERIC, 2) || ' ' || common_chaininfo_measure(u)
$$ LANGUAGE SQL STABLE;

comment on function common_chaininfo_rate(common_chaininfo) is
  E'@fieldName rate';
comment on column common_chaininfo.rate is E'@name rate_value';