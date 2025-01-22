CREATE OR REPLACE FUNCTION resume_update_asic(asic_id INTEGER)
  RETURNS BOOLEAN AS $$
    UPDATE common_asic SET stop_update = FALSE where id = $1
    RETURNING TRUE
  $$ LANGUAGE SQL VOLATILE;