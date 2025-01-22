CREATE OR REPLACE FUNCTION close_asic_errors(asic_id INTEGER)
  RETURNS BOOLEAN AS $$
    UPDATE common_error SET status = 4 where common_error.asic_id = $1
    RETURNING TRUE
  $$ LANGUAGE SQL VOLATILE;