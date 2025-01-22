CREATE OR REPLACE FUNCTION convert_error_status(status INTEGER)
  RETURNS VARCHAR AS $$
SELECT CASE
       WHEN status = 1
         THEN 'Открыта'
       WHEN status = 2
         THEN 'Ждет решения'
       WHEN status = 3
         THEN 'Не показывать'
       WHEN status = 4
         THEN 'Закрыта'
       END
$$ LANGUAGE SQL STABLE;