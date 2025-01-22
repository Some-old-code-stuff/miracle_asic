CREATE OR REPLACE FUNCTION set_alg_type(asic_id INTEGER, type INTEGER)
  RETURNS BOOLEAN AS $$
    UPDATE common_asic SET alg_type = type
    where id = $1
    RETURNING TRUE
  $$ LANGUAGE SQL VOLATILE;