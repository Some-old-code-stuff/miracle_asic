CREATE OR REPLACE FUNCTION set_asic_type(asic_id INTEGER, type INTEGER)
  RETURNS BOOLEAN AS $$
    UPDATE common_asic SET type = $2, name = convert_asic_type(type)
    where id = $1
    RETURNING TRUE
  $$ LANGUAGE SQL VOLATILE;