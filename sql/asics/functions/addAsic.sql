CREATE OR REPLACE FUNCTION add_asic(type int, ip_address text, farm int, client int, alg_type int)
  RETURNS common_asic AS $$
  insert INTO common_asic(type, ip_address, farm_id, client_id, alg_type, crypt_type, name, default_rate, measure, full_rate, stop_update) VALUES
    ($1, $2, farm, client, $5, 0, convert_asic_type($1), 0, 0, 0, TRUE) RETURNING *;

  $$ LANGUAGE SQL VOLATILE;