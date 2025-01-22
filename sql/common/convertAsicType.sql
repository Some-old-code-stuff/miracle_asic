CREATE OR REPLACE FUNCTION convert_asic_type(type INTEGER)
  RETURNS VARCHAR AS $$
SELECT CASE
       WHEN type = 0
         THEN 'Не определен'
       WHEN type = 1
         THEN 'S9'
       WHEN type = 2
         THEN 'L3+'
       WHEN type = 3
         THEN 'DR100'
       WHEN type = 4
         THEN 'A4+'
       WHEN type = 5
         THEN 'L21'
       WHEN type = 6
         THEN 'D3'
       END
$$ LANGUAGE SQL STABLE;