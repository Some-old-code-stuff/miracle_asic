CREATE FUNCTION common_asic_algorithm_type(u common_asic)
  RETURNS VARCHAR AS $$
SELECT CASE
       WHEN u.alg_type = 0
         THEN 'Не определен'
       WHEN u.alg_type = 1
         THEN 'SHA-256'
       WHEN u.alg_type = 2
         THEN 'Scrypt'
       WHEN u.alg_type = 3
         THEN 'X11'
       END
$$ LANGUAGE SQL STABLE;

comment on function common_asic_algorithm_type(common_asic) is
  E'@fieldName algType';
comment on column common_asic.alg_type is E'@name alg_type_value';