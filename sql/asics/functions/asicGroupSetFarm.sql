CREATE OR REPLACE FUNCTION asic_group_set_farm(asic_ids INTEGER[], farm_id INTEGER)
  RETURNS BOOLEAN AS $$
    UPDATE common_asic SET farm_id = $2 where id IN (select * from unnest(asic_ids))
    RETURNING TRUE
  $$ LANGUAGE SQL VOLATILE;