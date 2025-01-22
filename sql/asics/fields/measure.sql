CREATE FUNCTION common_asic_measure(u common_asic)
  RETURNS VARCHAR AS $$
SELECT CASE
       WHEN u.measure = 0
         THEN 'MH/S'
       WHEN u.measure = 1
         THEN 'GH/S'
       WHEN u.measure = 2
         THEN 'TH/S'
       END
$$ LANGUAGE SQL STABLE;

comment on function common_asic_measure(common_asic) is
  E'@fieldName measure';
comment on column common_asic.measure is E'@name measure_value';