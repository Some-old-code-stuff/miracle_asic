CREATE or replace FUNCTION common_asic_default_rate(u common_asic)
  RETURNS VARCHAR AS $$
  SELECT round(u.default_rate::NUMERIC, 2) || ' ' || common_asic_measure(u)
$$ LANGUAGE SQL STABLE;

comment on function common_asic_default_rate(common_asic) is
  E'@fieldName defaultRate';
comment on column common_asic.default_rate is E'@name default_rate_value';