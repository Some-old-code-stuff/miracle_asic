CREATE or replace FUNCTION common_asic_farm_name(u common_asic)
  RETURNS VARCHAR AS $$
  SELECT CASE
       WHEN u.farm_id ISNULL
         THEN 'Не определена'
       ELSE "common_farm"."name"
       END AS "farm_name"
FROM "common_farm"
  where common_farm.id = nullif(u.farm_id, -1)
$$ LANGUAGE SQL STABLE;