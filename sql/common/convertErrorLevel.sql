CREATE OR REPLACE FUNCTION convert_error_level(level INTEGER)
  RETURNS VARCHAR AS $$
SELECT CASE
      WHEN level = 1
         THEN 'Предупреждение'
       WHEN level = 2
         THEN 'Ошибка'
       END
$$ LANGUAGE SQL STABLE;