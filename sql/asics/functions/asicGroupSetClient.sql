CREATE OR REPLACE FUNCTION asic_group_set_client(asic_ids INTEGER[], client_id INTEGER)
  RETURNS BOOLEAN AS $$
    UPDATE common_asic SET client_id = $2 where id IN (select * from unnest(asic_ids))
    RETURNING TRUE
  $$ LANGUAGE SQL VOLATILE;