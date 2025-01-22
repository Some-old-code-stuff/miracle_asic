CREATE OR REPLACE FUNCTION asic_errors(asic_id INT, field_name TEXT, object_id INT default null)
  RETURNS SETOF common_error AS $$
SELECT common_error.*
FROM common_error
WHERE common_error.asic_id = $1
      AND common_error.field_name = $2
      AND ($3 ISNULL OR common_error.object_id = $3)
      and common_error.status < 4
$$ LANGUAGE SQL STABLE;