CREATE FUNCTION common_chaininfo_measure(u common_chaininfo)
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

comment on function common_chaininfo_measure(common_chaininfo) is
  E'@fieldName measure';
comment on column common_chaininfo.measure is E'@name measure_value';