CREATE OR REPLACE FUNCTION asic_group_set_auto_update(asic_ids INTEGER [], update BOOLEAN)
  RETURNS BOOLEAN AS $$
UPDATE common_asic
SET stop_update = NOT $2
WHERE id IN (SELECT *
             FROM unnest(asic_ids))
RETURNING TRUE
$$ LANGUAGE SQL VOLATILE;