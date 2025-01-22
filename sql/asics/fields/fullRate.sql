CREATE or replace FUNCTION common_asic_full_rate(u common_asic)
  RETURNS VARCHAR AS $$
  SELECT round(u.full_rate::NUMERIC, 2) || ' ' || common_asic_measure(u)
$$ LANGUAGE SQL STABLE;

comment on function common_asic_full_rate(common_asic) is
  E'@fieldName fullRate';
comment on column common_asic.full_rate is E'@name full_rate_value';