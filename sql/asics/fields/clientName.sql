CREATE OR REPLACE FUNCTION common_asic_client_name(u common_asic)
  RETURNS VARCHAR AS $$
SELECT CASE
       WHEN u.client_id ISNULL
         THEN 'Не определен'
       ELSE "common_client"."name"
       END
FROM "common_client"
  where common_client.id = nullif(u.client_id, -1)
$$ LANGUAGE SQL STABLE;